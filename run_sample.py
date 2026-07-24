import pandas as pd

from src.data_loader import load_tickets, prepare_tickets
from src.schemas import TicketInput
from src.triage_agent import TicketTriageAgent


def main() -> None:
    df = load_tickets("data/dataset_tickets.csv")
    prepared_df = prepare_tickets(df, language="en")

    sample = prepared_df.head(5)

    agent = TicketTriageAgent()
    results = []

    for _, row in sample.iterrows():
        ticket = TicketInput(
            ticket_id=row["ticket_id"],
            text=row["ticket_text"],
        )

        result = agent.triage_ticket(ticket)

        output = {
            "ticket_id": row["ticket_id"],
            "subject": row["subject"],
            "body": row["body"],
            **result.model_dump(),
        }

        results.append(output)

        print("=" * 80)
        print(row["ticket_text"])
        print(result.model_dump())

    result_df = pd.DataFrame(results)

    print("\nResult overview:")
    print(
        result_df[
            [
                "ticket_id",
                "subject",
                "topic",
                "urgency",
                "needs_more_information",
                "next_action",
            ]
        ]
    )


if __name__ == "__main__":
    main()