"""
Application-wide constants and predefined stock prices.
"""

from pathlib import Path

# Predefined stock prices (USD per share)
STOCK_PRICES: dict[str, float] = {
    "AAPL": 180.0,
    "TSLA": 250.0,
    "GOOGL": 140.0,
    "MSFT": 330.0,
    "AMZN": 145.0,
}

# Supported tickers for validation messages
SUPPORTED_TICKERS: tuple[str, ...] = tuple(STOCK_PRICES.keys())

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"

# Report file name prefix
REPORT_PREFIX = "portfolio_report"
