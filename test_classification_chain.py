from src.chains import create_classification_chain


def main() -> None:
    chain = create_classification_chain()

    test_tickets = [
        "I was charged twice for my monthly insurance premium.",
        "I cannot log in to the customer portal.",
        "My car was damaged in an accident yesterday.",
        "Please send me a copy of my insurance policy.",
        "Someone was injured in a car accident and needs immediate help.",
        "I would like to order a pizza.",
    ]

    for ticket in test_tickets:
        print("=" * 80)
        print("Ticket:")
        print(ticket)

        result = chain.invoke(
            {
                "ticket_text": ticket
            }
        )

        print("\nClassification:")
        print(result.model_dump())


if __name__ == "__main__":
    main()