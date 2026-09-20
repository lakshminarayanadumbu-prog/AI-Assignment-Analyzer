import re


def clean_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def get_words(text):
    cleaned_text = clean_text(text)

    # Split text into words
    words = cleaned_text.split()

    return words