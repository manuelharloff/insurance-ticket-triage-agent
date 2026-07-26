from src.chains import (
    create_classification_chain,
    create_information_assessment_chain,
)
from src.routing import determine_next_action
from src.schemas import TicketInput, TriageResult


class TicketTriageAgent:
    """Orchestrate the complete multi-step ticket triage workflow."""

    def __init__(self) -> None:
        """Initialize the information assessment and classification chains."""

        # Create the chain that checks whether the ticket is clear enough
        self.information_chain = create_information_assessment_chain()

        # Create the chain that classifies topic and urgency
        self.classification_chain = create_classification_chain()

    def triage_ticket(self, ticket: TicketInput) -> TriageResult:
        """Process one ticket and return the final structured triage result."""

        # Assess whether the ticket contains enough information for routing
        information = self.information_chain.invoke(
            {"ticket_text": ticket.text}
        )

        # Classify the primary topic and operational urgency
        classification = self.classification_chain.invoke(
            {"ticket_text": ticket.text}
        )

        # Derive the operational next action from the model outputs
        next_action = determine_next_action(
            topic=classification.topic,
            urgency=classification.urgency,
            needs_more_information=information.needs_more_information,
        )

        # Combine all intermediate results into one validated output object
        return TriageResult(
            ticket_id=ticket.ticket_id,
            topic=classification.topic,
            urgency=classification.urgency,
            needs_more_information=information.needs_more_information,
            missing_information=information.missing_information,
            clarification_question=information.clarification_question,
            next_action=next_action,
            notes=classification.notes,
            processing_status="success",
        )