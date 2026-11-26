
from typing import Literal
from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    company: str

    mentioned: bool

    sentiment: Literal[
        "positive",
        "negative",
        "neutral",
        "not_applicable"
    ]

    relevant_context: list[str] = Field(
        description="Original relevant sentences extracted from the answer."
    )

    explanation: str = Field(
        description="Concise explanation supporting the sentiment classification."
    )
