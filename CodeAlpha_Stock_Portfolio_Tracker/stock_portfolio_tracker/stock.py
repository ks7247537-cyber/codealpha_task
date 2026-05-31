"""
Stock model representing a single holding in the portfolio.
"""

from __future__ import annotations

from dataclasses import dataclass

from stock_portfolio_tracker.constants import STOCK_PRICES


@dataclass
class Stock:
    """
    Represent a stock holding with ticker, quantity, and unit price.

    Attributes:
        symbol: Stock ticker symbol (e.g., AAPL).
        quantity: Number of shares held.
        price_per_share: Current price per share in USD.
    """

    symbol: str
    quantity: int
    price_per_share: float

    def __post_init__(self) -> None:
        """Normalize symbol to uppercase after initialization."""
        self.symbol = self.symbol.upper().strip()

    @classmethod
    def from_symbol(cls, symbol: str, quantity: int) -> Stock:
        """
        Create a Stock instance using the predefined price dictionary.

        Args:
            symbol: Stock ticker symbol.
            quantity: Number of shares.

        Returns:
            Stock instance with price from STOCK_PRICES.

        Raises:
            KeyError: If symbol is not in STOCK_PRICES.
        """
        symbol = symbol.upper().strip()
        if symbol not in STOCK_PRICES:
            raise KeyError(
                f"Unknown symbol '{symbol}'. "
                f"Supported: {', '.join(STOCK_PRICES.keys())}"
            )
        return cls(
            symbol=symbol,
            quantity=quantity,
            price_per_share=STOCK_PRICES[symbol],
        )

    @property
    def total_value(self) -> float:
        """Calculate total market value of this holding."""
        return round(self.quantity * self.price_per_share, 2)

    def __str__(self) -> str:
        return (
            f"{self.symbol}: {self.quantity} shares @ "
            f"${self.price_per_share:.2f} = ${self.total_value:,.2f}"
        )

    def to_dict(self) -> dict[str, str | int | float]:
        """Return holding data as a dictionary for reports."""
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "price_per_share": self.price_per_share,
            "total_value": self.total_value,
        }
