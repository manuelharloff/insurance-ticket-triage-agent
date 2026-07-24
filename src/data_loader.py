from pathlib import Path
import re

import pandas as pd


# Values that should be treated as missing rather than usable ticket content
EMPTY_VALUES = {
    "",
    "nan",
    "none",
    "null",
    "n/a",
    "na",
    "-",
}


def load_tickets(file_path: str | Path) -> pd.DataFrame:
    """Load the raw ticket dataset from a CSV file."""

    return pd.read_csv(file_path)


def normalize_text(value: object) -> str:
    """Normalize one text value without removing meaningful language context."""

    # Replace missing pandas values with an empty string
    if pd.isna(value):
        return ""

    # Convert the value to text and remove leading and trailing whitespace
    text = str(value).strip()

    # Replace repeated spaces, tabs and line breaks with a single space
    text = re.sub(r"\s+", " ", text)

    # Treat common placeholder values as missing content
    if text.lower() in EMPTY_VALUES:
        return ""

    return text


def prepare_tickets(
    df: pd.DataFrame,
    language: str = "en",
) -> pd.DataFrame:
    """Prepare support tickets for the local LLM triage workflow."""

    # Work on a copy to avoid modifying the original DataFrame
    prepared = df.copy()

    # Original index as stable ticket ID
    prepared = prepared.reset_index().rename(
        columns={"index": "ticket_id"}
    )

    # Restrict the prototype to tickets in the selected language
    prepared = prepared[
        prepared["language"]
        .fillna("")
        .astype(str)
        .str.lower()
        .eq(language.lower())
    ].copy()

    # Normalize the subject without changing its linguistic meaning
    prepared["normalized_subject"] = (
        prepared["subject"].apply(normalize_text)
    )

    # Normalize the body without removing punctuation, numbers or keywords
    prepared["normalized_body"] = (
        prepared["body"].apply(normalize_text)
    )

    # Remove rows without usable content in both subject and body
    prepared = prepared[
        prepared["normalized_subject"].ne("")
        | prepared["normalized_body"].ne("")
    ].copy()

    # Optional duplicate removal if duplicate tickets are found in future data
    # prepared = prepared.drop_duplicates(
    #     subset=["normalized_subject", "normalized_body"]
    # )

    # Combine subject and body into one structured input for the LLM
    prepared["ticket_text"] = (
        "Subject: "
        + prepared["normalized_subject"]
        + "\nDescription: "
        + prepared["normalized_body"]
    )

    # Convert ticket IDs to strings for consistent downstream processing
    prepared["ticket_id"] = prepared["ticket_id"].astype(str)

    return prepared