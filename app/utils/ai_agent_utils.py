import instructor
from pydantic import BaseModel, Field
from typing import List
from app.models.policy_rule import RequirementType, Operator
from app.core.config import settings
from vertexai.generative_models import GenerativeModel
import vertexai
import os
from google import genai

os.environ["GOOGLE_CLOUD_PROJECT"] = settings.GOOGLE_PROJECT_ID

genai_client = genai.Client(
    vertexai=True,
    project=settings.GOOGLE_PROJECT_ID,
    location=settings.GOOGLE_PROJECT_LOCATION,
)

# Patch it using from_genai
client = instructor.from_genai(genai_client)


class LoanRule(BaseModel):
    field_key: str = Field(
        description="The internal key like 'fico_score' or 'paynet_score' or 'business_duration' or 'loan_amount' or 'equipment_type' or 'geographic_location' or 'indrustry' or 'other'"
    )
    operator: str = Field(
        description="Logical operator: " + ", ".join([op.value for op in Operator])
    )
    requirement_type: str = Field(
        description="Requirement type: "
        + ", ".join([rt.value for rt in RequirementType])
    )
    target_value: str = Field(description="The actual value from the PDF")
    error_message: str = Field(description="User-friendly rejection reason")


class LenderPolicy(BaseModel):
    rules: List[LoanRule]


def extract_guaranted_rules(text: str):
    return client.chat.completions.create(
        response_model=LenderPolicy,
        model="gemini-2.5-pro",
        messages=[
            {
                "role": "user",
                "content": (
                    "SYSTEM INSTRUCTIONS:\n"
                    "You are a Senior Equipment Finance Underwriter. Convert the following "
                    "unstructured lender guidelines into a structured rules engine schema.\n\n"
                    "MAPPING RULES:\n"
                    "- FICO -> 'fico_score'\n"
                    "- PayNet -> 'paynet_score'\n"
                    "- Time in Business -> 'business_duration' (convert to months)\n"
                    "- Excluded States -> 'geographic_location' (operator: 'NOT_IN')\n"
                    "- Excluded Industries -> 'industry' (operator: 'NOT_IN')\n"
                    "- Amounts -> 'loan_amount'\n\n"
                    "LOGIC:\n"
                    "- Mandatory = 'HARD_STOP', Preferred = 'SOFT_MATCH'.\n"
                    f"INPUT TEXT:\n\n{text}"
                ),
            },
        ],
        max_retries=3,
    )
