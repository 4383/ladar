import re


def normalize_value(value):
    """
    Normalize individual values by applying the following transformations:
    - Convert all characters to lowercase.
    - Remove underscores ('_') without replacement.
    - Remove extra spaces (multiple spaces reduced to a single one).

    Args:
        value (str): The value to normalize.

    Returns:
        str: The normalized value.
    """
    if isinstance(value, str):
        normalized = value.lower()
        normalized = normalized.replace("_", "")
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized
    return value


def normalize_docstring(docstring):
    """
    Normalize a docstring by converting it to lowercase and removing unnecessary newlines and spaces.

    Args:
        docstring (str): The docstring to normalize.

    Returns:
        str: The normalized docstring, formatted as a single, compact string.
    """
    if isinstance(docstring, str):
        # Remove leading/trailing whitespace and convert to lowercase
        normalized = docstring.strip().lower()

        # Replace multiple newlines with a single space
        normalized = re.sub(r"\s*\n\s*", " ", normalized)

        # Remove excess spaces between words
        normalized = re.sub(r"\s+", " ", normalized)

        return normalized
    return docstring


def normalize_content(content):
    """
    Normalize content depending on its structure.
    This function applies normalization to values while preserving the format.

    Args:
        content (dict or list): The parsed content to normalize.

    Returns:
        dict or list: The normalized content with the original structure.
    """
    if isinstance(content, dict):
        return {normalize_value(k): normalize_content(v) for k, v in content.items()}
    elif isinstance(content, list):
        return [normalize_content(item) for item in content]
    else:
        return normalize_value(content)
