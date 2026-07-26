from langchain_ollama import ChatOllama

from src.config import settings
from src.prompts import (
    information_assessment_prompt,
    classification_prompt,
)
from src.schemas import (
    InformationAssessment,
    ClassificationResult,
)


def create_llm() -> ChatOllama:
    """Create the locally hosted Ollama chat model."""

    # Initialize the model with the central project configuration
    return ChatOllama(
        model=settings.model_name,
        temperature=settings.temperature,
    )


def create_information_assessment_chain():
    """Create the chain that checks whether a ticket is clear enough for triage."""

    # Create a local LLM instance for the information assessment
    llm = create_llm()

    # Constrain the model response to the InformationAssessment schema
    structured_llm = llm.with_structured_output(
        InformationAssessment
    )

    # Combine the assessment prompt with the structured model output
    return information_assessment_prompt | structured_llm


def create_classification_chain():
    """Create the chain that classifies ticket topic and urgency."""

    # Create a separate local LLM instance for the classification step
    llm = create_llm()

    # Constrain the model response to the ClassificationResult schema
    structured_llm = llm.with_structured_output(
        ClassificationResult
    )

    # Combine the classification prompt with the structured model output
    return classification_prompt | structured_llm