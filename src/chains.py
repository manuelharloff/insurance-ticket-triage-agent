from langchain_ollama import ChatOllama

from src.config import settings
from src.prompts import (
    information_assessment_prompt,
    classification_prompt,
)
from src.schemas import (
    InformationAssessment,
    ClassificationResult
)


def create_llm() -> ChatOllama:
    return ChatOllama(
        model=settings.model_name,
        temperature=settings.temperature,
    )


def create_information_assessment_chain():
    llm = create_llm()

    structured_llm = llm.with_structured_output(
        InformationAssessment
    )

    return information_assessment_prompt | structured_llm

def create_classification_chain():
    llm = create_llm()

    structured_llm = llm.with_structured_output(
        ClassificationResult
    )

    return classification_prompt | structured_llm