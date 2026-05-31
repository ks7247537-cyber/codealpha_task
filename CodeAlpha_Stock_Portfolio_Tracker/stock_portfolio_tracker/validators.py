"""
Input validation utilities for the Stock Portfolio Tracker.
"""

from stock_portfolio_tracker.constants import STOCK_PRICES, SUPPORTED_TICKERS


class ValidationError(Exception):
    """Raised when user input fails validation."""


def validate_symbol(symbol: str) -> str:
    """
    Validate and normalize a stock ticker symbol.

    Args:
        symbol: Raw user input for ticker.

    Returns:
        Uppercase, stripped symbol.

    Raises:
        ValidationError: If symbol is empty or unsupported.
    """
    if not symbol or not symbol.strip():
        raise ValidationError("Stock symbol cannot be empty.")

    normalized = symbol.upper().strip()
    if normalized not in STOCK_PRICES:
        raise ValidationError(
            f"Invalid symbol '{normalized}'. "
            f"Choose from: {', '.join(SUPPORTED_TICKERS)}"
        )
    return normalized


def validate_quantity(quantity_input: str) -> int:
    """
    Validate share quantity input.

    Args:
        quantity_input: Raw user input for quantity.

    Returns:
        Positive integer quantity.

    Raises:
        ValidationError: If quantity is not a positive integer.
    """
    if not quantity_input or not quantity_input.strip():
        raise ValidationError("Quantity cannot be empty.")

    try:
        quantity = int(quantity_input.strip())
    except ValueError as exc:
        raise ValidationError(
            "Quantity must be a whole number (no decimals)."
        ) from exc

    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero.")

    if quantity > 1_000_000:
        raise ValidationError("Quantity exceeds maximum allowed (1,000,000).")

    return quantity


def validate_menu_choice(choice: str, min_val: int, max_val: int) -> int:
    """
    Validate a numeric menu selection.

    Args:
        choice: Raw menu input.
        min_val: Minimum valid option number.
        max_val: Maximum valid option number.

    Returns:
        Validated integer choice.

    Raises:
        ValidationError: If choice is out of range or not numeric.
    """
    if not choice or not choice.strip():
        raise ValidationError("Please enter a menu option.")

    try:
        option = int(choice.strip())
    except ValueError as exc:
        raise ValidationError("Menu choice must be a number.") from exc

    if option < min_val or option > max_val:
        raise ValidationError(
            f"Please enter a number between {min_val} and {max_val}."
        )
    return option
