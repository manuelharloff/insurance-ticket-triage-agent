from typing import Literal

from pydantic import BaseModel, Field, model_validator


# Supported ticket topics returned by the classification chain
Topic = Literal[
    "Policy / Contract",
    "Claims / Damage",
    "Billing / Payment",
    "Technical / Online Access",
    "Other",
]

# Supported urgency levels returned by the classification chain
Urgency = Literal["Low", "Medium", "High"]


class ClassificationResult(BaseModel):
    """Structured output of the topic and urgency classification chain."""

    # Primary support category assigned to the ticket
    topic: Topic = Field(
        description="The primary insurance support topic."
    )

    # Operational priority assigned to the ticket
    urgency: Urgency = Field(
        description="The operational urgency of the ticket."
    )

    # Short factual explanation for the classification result
    notes: str = Field(
        description="A short factual explanation without invented details."
    )


class InformationAssessment(BaseModel):
    """Structured output of the ticket completeness assessment."""

    # Indicates whether the ticket is too vague for an initial routing decision
    needs_more_information: bool = Field(
        description=(
            "True if the ticket is too vague or incomplete to identify "
            "the customer's main issue and route it."
        )
    )

    # Details that are still required to understand the customer's issue
    missing_information: list[str] = Field(default_factory=list)

    # Single follow-up question suggested for the customer
    clarification_question: str | None = None

    @model_validator(mode="after")
    def ensure_consistent_output(self):
        """Ensure that the information assessment fields remain consistent."""

        # Add safe defaults when the model marks a ticket as incomplete
        if self.needs_more_information:
            if not self.missing_information:
                self.missing_information = [
                    "A clearer description of the customer's issue"
                ]

            if not self.clarification_question:
                self.clarification_question = (
                    "Could you please describe what you need help with?"
                )

        # Remove clarification fields when no additional information is needed
        else:
            self.missing_information = []
            self.clarification_question = None

        return self


class TicketInput(BaseModel):
    """Represent the normalized input passed to the triage agent."""

    ticket_id: str
    text: str


class TriageResult(BaseModel):
    """Represent the final structured output of the triage workflow."""

    ticket_id: str
    topic: Topic
    urgency: Urgency
    needs_more_information: bool
    missing_information: list[str]
    clarification_question: str | None
    next_action: str
    notes: str
    processing_status: Literal["success", "fallback"]