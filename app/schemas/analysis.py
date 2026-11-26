
from typing import Literal

from pydantic import BaseModel, Field, model_validator


OpinionPolarity = Literal["positive", "negative"]

SentimentLabel = Literal[
    "positive",
    "negative",
    "neutral",
    "neutral_mixed",
    "not_applicable"
]



class Opinion(BaseModel):
    opinion: str = Field(
        description="A concise, target-specific evaluative opinion."
    )
    polarity: OpinionPolarity = Field(
        description="Whether the opinion is favourable or unfavourable."
    )
    intensity: int = Field(
        ge=1,
        le=2,
        description="Opinion intensity: 1 for moderate, 2 for strong."
    )



# This is the structure Gemini is allowed to return.
# Notice that it does NOT contain a sentiment field.
class GeminiAnalysisResult(BaseModel):
    company: str
    mentioned: bool
    relevant_context: list[str] = Field(default_factory=list)
    opinions: list[Opinion] = Field(default_factory=list)
    explanation: str

    @model_validator(mode="after")
    def validate_mention_consistency(self):
        if not self.mentioned:
            if self.opinions or self.relevant_context:
                raise ValueError(
                    "Unmentioned companies cannot have opinions or context."
                )
        return self


# This is the final structure returned by our application.
class AnalysisResult(BaseModel):
    company: str
    mentioned: bool
    sentiment: SentimentLabel
    sentiment_score: float | None = None
    relevant_context: list[str] = Field(default_factory=list)
    opinions: list[Opinion] = Field(default_factory=list)
    explanation: str

    @model_validator(mode="after")
    def validate_mention_consistency(self):
        if not self.mentioned:
            if self.opinions or self.relevant_context:
                raise ValueError(
                    "Unmentioned companies cannot have opinions or context."
                )
            if self.sentiment != "not_applicable":
                raise ValueError(
                    "Unmentioned companies must have not_applicable sentiment."
                )
            if self.sentiment_score is not None:
                raise ValueError(
                    "Unmentioned companies cannot have a sentiment score."
                )
        else:
            if self.sentiment == "not_applicable":
                raise ValueError(
                    "Mentioned companies cannot have not_applicable sentiment."
                )
        return self


class AnalysisRequest(BaseModel):
    company: str = Field(
        min_length=1,
        max_length=100,
        description="Name of the company or brand to analyze."
    )
    answer: str = Field(
        min_length=1,
        max_length=20000,
        description="AI-generated answer to analyze."
    )

    @model_validator(mode="after")
    def validate_non_empty_values(self):
        if not self.company.strip():
            raise ValueError("Company name cannot be empty.")

        if not self.answer.strip():
            raise ValueError("Answer cannot be empty.")

        return self
