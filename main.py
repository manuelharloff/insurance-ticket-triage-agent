from pathlib import Path
from time import perf_counter

import pandas as pd
from tqdm import tqdm

from src.data_loader import load_tickets, prepare_tickets
from src.schemas import TicketInput
from src.triage_agent import TicketTriageAgent


INPUT_PATH = Path("data/dataset_tickets.csv")
OUTPUT_PATH = Path("outputs/triage_results.csv")
SAMPLE_SIZE = 200


def create_fallback_result(
    ticket_id: str,
    subject: str,
    body: str,
    error: Exception,
) -> dict:
    return {
        "ticket_id": ticket_id,
        "subject": subject,
        "body": body,
        "topic": "Other",
        "urgency": "Medium",
        "needs_more_information": True,
        "missing_information": [
            "The ticket could not be processed automatically."
        ],
        "clarification_question": (
            "Could you please provide more details about your request?"
        ),
        "next_action": "Escalate to human supervisor",
        "notes": f"Processing error: {type(error).__name__}",
        "processing_status": "fallback",
        "processing_time_seconds": None,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_tickets(INPUT_PATH)
    prepared_df = prepare_tickets(df, language="en")

    # Reproducible sample instead of always taking the first 20 rows
    sample = prepared_df.sample(
        n=min(SAMPLE_SIZE, len(prepared_df)),
        random_state=42,
    )

    agent = TicketTriageAgent()
    results = []

    total_start = perf_counter()

    for _, row in tqdm(
        sample.iterrows(),
        total=len(sample),
        desc="Processing tickets",
    ):
        ticket_start = perf_counter()

        try:
            ticket = TicketInput(
                ticket_id=row["ticket_id"],
                text=row["ticket_text"],
            )

            triage_result = agent.triage_ticket(ticket)

            output = {
                "ticket_id": row["ticket_id"],
                "subject": row["subject"],
                "body": row["body"],
                **triage_result.model_dump(),
                "processing_time_seconds": round(
                    perf_counter() - ticket_start,
                    2,
                ),
            }

        except Exception as error:
            output = create_fallback_result(
                ticket_id=row["ticket_id"],
                subject=row["subject"],
                body=row["body"],
                error=error,
            )

        results.append(output)

    result_df = pd.DataFrame(results)
    result_df.to_csv(OUTPUT_PATH, index=False)

    total_duration = perf_counter() - total_start
    fallback_count = (
        result_df["processing_status"]
        .eq("fallback")
        .sum()
    )

    print("\nBatch completed")
    print(f"Processed tickets: {len(result_df)}")
    print(f"Fallback results: {fallback_count}")
    print(f"Total runtime: {total_duration:.2f} seconds")
    print(
        "Average runtime per ticket: "
        f"{total_duration / len(result_df):.2f} seconds"
    )
    print(f"Output saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()