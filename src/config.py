from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Store the central configuration for the local language model."""

    # Name of the Ollama model used by all LangChain components
    model_name: str = "qwen3:1.7b"

    # Deterministic model behavior for consistent classifications
    temperature: float = 0.0


# Create one shared immutable settings instance for the application
settings = Settings()