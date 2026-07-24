from langchain_ollama import ChatOllama

from src.schemas import ClassificationResult


def main() -> None:
    llm = ChatOllama(
        model="qwen3:1.7b",
        temperature=0,
    )

    structured_llm = llm.with_structured_output(
        ClassificationResult
    )

    result = structured_llm.invoke(
        """
        You classify customer support tickets for an insurance company.

        Ticket:
        I was charged twice for my monthly insurance premium.

        Return the topic, urgency and a short factual explanation.
        """
    )

    print(result)
    print(result.model_dump())


if __name__ == "__main__":
    main()