"""Input validation utilities for the chatbot."""

import re
from typing import Tuple


def validate_user_input(user_input: str) -> Tuple[bool, str]:
    """
    Validate user input for the chatbot session.

    Args:
        user_input: Raw input string from the user.

    Returns:
        A tuple of (is_valid, cleaned_input).
    """
    if user_input is None:
        return False, ""

    cleaned = user_input.strip()

    if not cleaned:
        return False, ""

    if len(cleaned) > 500:
        return False, cleaned[:500]

    return True, cleaned


def validate_expression(expression: str) -> Tuple[bool, str]:
    """
    Validate a mathematical expression for safe evaluation.

    Only digits, basic operators, parentheses, decimal points,
    and whitespace are permitted.

    Args:
        expression: Mathematical expression string.

    Returns:
        A tuple of (is_valid, message_or_cleaned_expression).
    """
    if not expression or not expression.strip():
        return False, "Expression cannot be empty."

    cleaned = expression.strip()

    allowed_pattern = re.compile(r"^[\d+\-*/().\s]+$")
    if not allowed_pattern.match(cleaned):
        return False, (
            "Invalid characters detected. Use only numbers and "
            "operators (+, -, *, /, parentheses)."
        )

    if cleaned.count("(") != cleaned.count(")"):
        return False, "Mismatched parentheses in expression."

    return True, cleaned
