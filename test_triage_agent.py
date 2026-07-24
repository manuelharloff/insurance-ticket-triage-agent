from src.schemas import TicketInput
from src.triage_agent import TicketTriageAgent


def main() -> None:
    agent = TicketTriageAgent()

    test_tickets = [
        TicketInput(
            ticket_id="1",
            text="I was charged twice for my monthly insurance premium.",
        ),
        TicketInput(
            ticket_id="2",
            text="Please help me.",
        ),
        TicketInput(
            ticket_id="3",
            text=(
                "Someone was injured in a car accident "
                "and needs immediate help."
            ),
        ),
        TicketInput(
            ticket_id="4",
            text="I cannot log in to the customer portal.",
        ),
    ]

    for ticket in test_tickets:
        print("=" * 80)
        print("Ticket:", ticket.text)

        result = agent.triage_ticket(ticket)

        print(result.model_dump())


if __name__ == "__main__":
    main()