from hatchet_sdk import Hatchet, Context
from pydantic import BaseModel
from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.ai_agent_utils import extract_guaranted_rules, LoanRule
from typing import List

hatchet = Hatchet()


class InputModel(BaseModel):
    lender_id: int
    lender_policy_id: int
    file_path: str


class PDFOutputModel(BaseModel):
    raw_text: str
    lender_id: int
    lender_policy_id: int


class PolicyRulesOutputModel(BaseModel):
    policy_rules: List[LoanRule]
    lender_id: int
    lender_policy_id: int


policy_rules_wf = hatchet.workflow(
    name="policy_rules_wf",
    on_events=["policy_rules:create"],
)


@policy_rules_wf.task(
    name="pdf_extraction", execution_timeout=300, schedule_timeout=300
)
def pdf_extraction(input: InputModel, context: Context) -> PDFOutputModel:
    extracted_text = extract_text_from_pdf(input.file_path)
    return PDFOutputModel(
        raw_text=extracted_text,
        lender_id=input.lender_id,
        lender_policy_id=input.lender_policy_id,
    )


@policy_rules_wf.task(
    name="policy_rules_generation",
    execution_timeout=300,
    schedule_timeout=300,
    parents=[pdf_extraction],
)
def policy_rules_generation(
    input: PDFOutputModel, context: Context
) -> PolicyRulesOutputModel:
    policy_rules = extract_guaranted_rules(input.raw_text)
    return PolicyRulesOutputModel(
        policy_rules=policy_rules.rules,
        lender_id=input.lender_id,
        lender_policy_id=input.lender_policy_id,
    )


@policy_rules_wf.task(
    name="policy_rules_save",
    execution_timeout=300,
    schedule_timeout=300,
    parents=[policy_rules_generation],
)
def policy_rules_save(input: PolicyRulesOutputModel, context: Context) -> None:
    print("policy_rules_save", input)
    pass
