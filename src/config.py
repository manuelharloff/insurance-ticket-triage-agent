from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model_name: str = "qwen3:1.7b"
    temperature: float = 0.0


settings = Settings()