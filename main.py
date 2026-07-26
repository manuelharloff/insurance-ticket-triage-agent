from pathlib import Path
from time import perf_counter

import pandas as pd
from tqdm import tqdm

from src.data_loader import load_tickets, prepare_tickets
from src.schemas import TicketInput
from src.triage_agent import TicketTriageAgent


# Input dataset, output location and number of tickets to process
INPUT_PATH = Path("data/dataset_tickets.csv")
OUTPUT_PATH = Path("outputs/triage_results.csv")
SAMPLE_SIZE = 200


def create_fallback_result(
    ticket_id: str,
    subject: str,
    body: str,
    error: Exception,
) -> dict:
    """Create a safe fallback result when automatic processing fails."""

    # Preserve the original ticket data and assign a conservative fallback
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
    """Run the complete batch ticket triage workflow."""

    # Create the output directory if it does not already exist
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load and preprocess the source ticket dataset
    df = load_tickets(INPUT_PATH)
    prepared_df = prepare_tickets(df, language="en")

    # Draw a reproducible random sample from the prepared tickets
    sample = prepared_df.sample(
        n=min(SAMPLE_SIZE, len(prepared_df)),
        random_state=42,
    )

    # Initialize the triage agent once for the complete batch
    agent = TicketTriageAgent()

    # Collect the structured result for every processed ticket
    results = []

    # Start measuring the complete batch runtime
    total_start = perf_counter()

    # Process tickets sequentially and display the current progress
    for _, row in tqdm(
        sample.iterrows(),
        total=len(sample),
        desc="Processing tickets",
    ):
        # Start measuring the runtime of the current ticket
        ticket_start = perf_counter()

        try:
            # Convert the prepared row into the validated agent input schema
            ticket = TicketInput(
                ticket_id=row["ticket_id"],
                text=row["ticket_text"],
            )

            # Run the complete multi-step triage workflow
            triage_result = agent.triage_ticket(ticket)

            # Combine original ticket data, model output and processing time
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
            # Keep the batch running by creating a safe fallback result
            output = create_fallback_result(
                ticket_id=row["ticket_id"],
                subject=row["subject"],
                body=row["body"],
                error=error,
            )

        # Add the current ticket result to the final batch output
        results.append(output)

    # Convert all ticket results into a DataFrame and save them as CSV
    result_df = pd.DataFrame(results)
    result_df.to_csv(OUTPUT_PATH, index=False)

    # Calculate final runtime and fallback statistics
    total_duration = perf_counter() - total_start
    fallback_count = (
        result_df["processing_status"]
        .eq("fallback")
        .sum()
    )

    # Print a concise batch-processing summary
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
    # Run the batch workflow only when this file is executed directly
    main()