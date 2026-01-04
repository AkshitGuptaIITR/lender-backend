from hatchet_sdk import Hatchet, Context
from pydantic import BaseModel
from app.utils.pdf_utils import extract_text_from_pdf

hatchet = Hatchet()


class InputModel(BaseModel):
    lender_id: int
    lender_policy_id: int
    file_path: str


class PDFOutputModel(BaseModel):
    raw_text: str


policy_rules_wf = hatchet.workflow(
    name="policy_rules_wf",
    input_validator=InputModel,
    on_events=["policy_rules:create"],
)


@policy_rules_wf.task(
    name="pdf_extraction", execution_timeout=300, schedule_timeout=300
)
def pdf_extraction(input: InputModel, context: Context) -> PDFOutputModel:
    extracted_text = extract_text_from_pdf(input.file_path)
    return PDFOutputModel(raw_text=extracted_text)
