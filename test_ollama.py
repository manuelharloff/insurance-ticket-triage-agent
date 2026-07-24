from langchain_ollama import ChatOllama


def main() -> None:
    llm = ChatOllama(
        model="qwen3:1.7b",
        temperature=0,
    )

    response = llm.invoke(
        "Respond with exactly one word: READY"
    )

    print(response.content)


if __name__ == "__main__":
    main()