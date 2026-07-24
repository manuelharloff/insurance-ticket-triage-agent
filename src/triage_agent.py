from src.chains import (
    create_classification_chain,
    create_information_assessment_chain,
)
from src.routing import determine_next_action
from src.schemas import TicketInput, TriageResult


class TicketTriageAgent:
    def __init__(self) -> None:
        self.information_chain = create_information_assessment_chain()
        self.classification_chain = create_classification_chain()

    def triage_ticket(self, ticket: TicketInput) -> TriageResult:
        information = self.information_chain.invoke(
            {"ticket_text": ticket.text}
        )

        classification = self.classification_chain.invoke(
            {"ticket_text": ticket.text}
        )

        next_action = determine_next_action(
            topic=classification.topic,
            urgency=classification.urgency,
            needs_more_information=information.needs_more_information,
        )

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