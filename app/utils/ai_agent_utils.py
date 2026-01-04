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
        description="Must be one of: fico_score, paynet_score, business_duration, "
        "loan_amount, geographic_location, industry_type, equipment_type, revenue, other"
    )
    operator: str = Field(
        description="Logical operator: " + ", ".join([op.value for op in Operator])
    )
    requirement_type: str = Field(
        description="Requirement type: "
        + ", ".join([rt.value for rt in RequirementType])
    )
    target_value: Union[int, float, List[str], str] = Field(
        description="The extracted value. Integers for scores/months, "
        "numeric for amounts, list of strings for states/industries."
    )
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
                    "Extract lender credit guidelines into the following specific schema.\n\n"
                    "MAPPING DICTIONARY:\n"
                    "- 'fico_score' (int): Extract minimum/maximum credit scores.\n"
                    "- 'paynet_score' (int): Extract business credit requirements.\n"
                    "- 'business_duration' (int): MUST CONVERT years to months (e.g., '2 years' -> 24).\n"
                    "- 'loan_amount' (numeric): Extract the loan amount.\n"
                    "- 'geographic_location' (list[str]): Use for excluded/restricted states (operator: NOT_IN).\n"
                    "- 'revenue' (numeric): Extract the revenue requirement of business.\n"
                    "- 'industry_type' (list[str]): Use for prohibited industries (operator: NOT_IN).\n"
                    "- 'equipment_type' (str): Use for specific asset restrictions.\n\n"
                    "LOGIC RULES:\n"
                    "1. Use 'HARD_STOP' for mandatory requirements.\n"
                    "2. Use 'SOFT_MATCH' for preferred or tiered guidelines.\n"
                    f"TEXT TO PARSE:\n\n{text}"
                ),
            },
        ],
        max_retries=3,
    )
