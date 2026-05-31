#!/usr/bin/env python3
"""
Stock Portfolio Tracker — Entry Point

CodeAlpha Python Programming Internship Project.

Run: python main.py
"""

import sys


def main() -> int:
    """
    Application entry point.

    Returns:
        Exit code (0 for success, 1 on fatal error).
    """
    try:
        from stock_portfolio_tracker.portfolio_manager import PortfolioManager

        manager = PortfolioManager(portfolio_name="My Investment Portfolio")
        manager.run()
        return 0

    except ImportError as err:
        print(
            "Error: Could not load application modules.\n"
            f"Details: {err}\n\n"
            "Run from the project root directory:\n"
            "  python main.py"
        )
        return 1
    except Exception as err:
        print(f"Fatal error: {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
