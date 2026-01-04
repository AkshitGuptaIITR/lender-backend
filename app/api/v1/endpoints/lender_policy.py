from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.lender_policy import LenderPolicy
from app.schemas.response import APIResponse
from app.schemas.lender_policy import LenderPolicyResponse
from app.models.lender import Lender
from app.core.config import settings
import os
import uuid
import shutil
from sqlalchemy import select
from app.schemas.lender_policy import LenderPolicyCreate
from hatchet_sdk import Hatchet
from app.workflows.policy_rules_generation import InputModel, policy_rules_wf

router = APIRouter()
hatchet = Hatchet()


@router.post("/", response_model=APIResponse[LenderPolicyResponse])
async def create_lender_policy(
    name: str = Form(...),
    lender_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400, detail="Invalid file type. Only PDF files are allowed."
            )

        # Check if lender exists
        result = await db.execute(select(Lender).where(Lender.id == lender_id))
        lender = result.scalar_one_or_none()
        if not lender:
            raise HTTPException(status_code=404, detail="Lender not found")

        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create policy record
        policy = LenderPolicy(name=name, lender_id=lender_id, file_path=file_path)
        db.add(policy)
        await db.commit()
        await db.refresh(policy)

        workflow_input = InputModel(
            lender_id=lender_id, lender_policy_id=policy.id, file_path=file_path
        )

        hatchet.event.push("policy_rules:create", workflow_input.__dict__)

        return APIResponse(data=policy)

    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        return APIResponse(status="error", message=str(e))


@router.get("/", response_model=APIResponse[list[LenderPolicyResponse]])
async def get_lender_policies(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(LenderPolicy))
        lender_policies = result.scalars().all()
        return APIResponse(data=lender_policies)
    except Exception as e:
        return APIResponse(status="error", message=str(e))


@router.get("/{lender_policy_id}", response_model=APIResponse[LenderPolicyResponse])
async def get_lender_policy(lender_policy_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(LenderPolicy).where(LenderPolicy.id == lender_policy_id)
        )
        lender_policy = result.scalar_one_or_none()
        if not lender_policy:
            raise HTTPException(status_code=404, detail="Lender policy not found")
        return APIResponse(data=lender_policy)
    except Exception as e:
        return APIResponse(status="error", message=str(e))


@router.get(
    "/lender/{lender_id}", response_model=APIResponse[list[LenderPolicyResponse]]
)
async def get_lender_policies_by_lender(
    lender_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(LenderPolicy).where(LenderPolicy.lender_id == lender_id)
        )
        lender_policies = result.scalars().all()
        return APIResponse(data=lender_policies)
    except Exception as e:
        return APIResponse(status="error", message=str(e))
