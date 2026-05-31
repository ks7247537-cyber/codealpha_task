"""
Portfolio model for aggregating multiple stock holdings.
"""

from __future__ import annotations

from stock_portfolio_tracker.stock import Stock


class Portfolio:
    """
    Manage a collection of stock holdings and portfolio-level analytics.

    Attributes:
        name: Display name for the portfolio.
        holdings: Dictionary mapping symbol to Stock instances.
    """

    def __init__(self, name: str = "My Portfolio") -> None:
        """
        Initialize an empty portfolio.

        Args:
            name: Human-readable portfolio name.
        """
        self.name = name
        self.holdings: dict[str, Stock] = {}

    def add_stock(self, stock: Stock) -> None:
        """
        Add or merge a stock into the portfolio.

        If the symbol already exists, quantities are combined.

        Args:
            stock: Stock instance to add.
        """
        symbol = stock.symbol
        if symbol in self.holdings:
            existing = self.holdings[symbol]
            self.holdings[symbol] = Stock(
                symbol=symbol,
                quantity=existing.quantity + stock.quantity,
                price_per_share=stock.price_per_share,
            )
        else:
            self.holdings[symbol] = stock

    def remove_stock(self, symbol: str) -> bool:
        """
        Remove a stock from the portfolio by symbol.

        Args:
            symbol: Ticker symbol to remove.

        Returns:
            True if removed, False if symbol was not found.
        """
        symbol = symbol.upper().strip()
        if symbol in self.holdings:
            del self.holdings[symbol]
            return True
        return False

    def get_stock(self, symbol: str) -> Stock | None:
        """Return a Stock by symbol, or None if not held."""
        return self.holdings.get(symbol.upper().strip())

    @property
    def is_empty(self) -> bool:
        """Return True if the portfolio has no holdings."""
        return len(self.holdings) == 0

    @property
    def total_investment(self) -> float:
        """Sum of all holding values in the portfolio."""
        return round(sum(stock.total_value for stock in self.holdings.values()), 2)

    @property
    def stock_count(self) -> int:
        """Number of distinct symbols in the portfolio."""
        return len(self.holdings)

    @property
    def total_shares(self) -> int:
        """Total number of shares across all holdings."""
        return sum(stock.quantity for stock in self.holdings.values())

    def get_most_valuable_stock(self) -> Stock | None:
        """
        Return the holding with the highest total market value.

        Returns:
            Stock with maximum total_value, or None if portfolio is empty.
        """
        if self.is_empty:
            return None
        return max(self.holdings.values(), key=lambda s: s.total_value)

    def get_least_valuable_stock(self) -> Stock | None:
        """Return the holding with the lowest total market value."""
        if self.is_empty:
            return None
        return min(self.holdings.values(), key=lambda s: s.total_value)

    def get_allocation(self) -> dict[str, float]:
        """
        Calculate percentage allocation per symbol.

        Returns:
            Dict mapping symbol to percentage of total portfolio (0-100).
        """
        total = self.total_investment
        if total == 0:
            return {}
        return {
            symbol: round((stock.total_value / total) * 100, 2)
            for symbol, stock in self.holdings.items()
        }

    def get_analytics(self) -> dict[str, str | float | int | None]:
        """
        Build a dictionary of portfolio analytics for display and reports.

        Returns:
            Analytics including totals, averages, and top/bottom holdings.
        """
        if self.is_empty:
            return {
                "portfolio_name": self.name,
                "stock_count": 0,
                "total_shares": 0,
                "total_investment": 0.0,
                "average_holding_value": 0.0,
                "most_valuable_symbol": None,
                "most_valuable_value": 0.0,
                "least_valuable_symbol": None,
                "least_valuable_value": 0.0,
            }

        most = self.get_most_valuable_stock()
        least = self.get_least_valuable_stock()
        avg_value = round(self.total_investment / self.stock_count, 2)

        return {
            "portfolio_name": self.name,
            "stock_count": self.stock_count,
            "total_shares": self.total_shares,
            "total_investment": self.total_investment,
            "average_holding_value": avg_value,
            "most_valuable_symbol": most.symbol if most else None,
            "most_valuable_value": most.total_value if most else 0.0,
            "least_valuable_symbol": least.symbol if least else None,
            "least_valuable_value": least.total_value if least else 0.0,
        }

    def list_holdings(self) -> list[Stock]:
        """Return holdings sorted by symbol."""
        return sorted(self.holdings.values(), key=lambda s: s.symbol)

    def clear(self) -> None:
        """Remove all holdings from the portfolio."""
        self.holdings.clear()
