from typing import Literal

from pydantic import BaseModel, Field, model_validator


Topic = Literal[
    "Policy / Contract",
    "Claims / Damage",
    "Billing / Payment",
    "Technical / Online Access",
    "Other",
]

Urgency = Literal["Low", "Medium", "High"]


class ClassificationResult(BaseModel):
    topic: Topic = Field(
        description="The primary insurance support topic."
    )

    urgency: Urgency = Field(
        description="The operational urgency of the ticket."
    )

    notes: str = Field(
        description="A short factual explanation without invented details."
    )

class InformationAssessment(BaseModel):

    needs_more_information: bool = Field(

        description=(

            "True if the ticket is too vague or incomplete to identify "

            "the customer's main issue and route it."

        )

    )

    missing_information: list[str] = Field(default_factory=list)

    clarification_question: str | None = None

    @model_validator(mode="after")

    def ensure_consistent_output(self):

        if self.needs_more_information:

            if not self.missing_information:

                self.missing_information = [

                    "A clearer description of the customer's issue"

                ]

            if not self.clarification_question:

                self.clarification_question = (

                    "Could you please describe what you need help with?"

                )

        else:

            self.missing_information = []

            self.clarification_question = None

        return self


class TicketInput(BaseModel):
    ticket_id: str
    text: str


class TriageResult(BaseModel):
    ticket_id: str
    topic: Topic
    urgency: Urgency
    needs_more_information: bool
    missing_information: list[str]
    clarification_question: str | None
    next_action: str
    notes: str
    processing_status: Literal["success", "fallback"]