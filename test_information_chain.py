from src.chains import create_information_assessment_chain


def main() -> None:
    chain = create_information_assessment_chain()

    test_tickets = [
        "I cannot log in to my customer portal.",
        "Please help me.",
        "My car was damaged yesterday and I want to report the incident.",
        "It does not work.",
        "I was charged twice for my monthly insurance premium.",
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

        print("\nAssessment:")
        print(result.model_dump())


if __name__ == "__main__":
    main()