"""
Terminal UI helpers for a clean, menu-driven CLI experience.
"""

import os
import sys
from typing import Iterable

from stock_portfolio_tracker.constants import STOCK_PRICES
from stock_portfolio_tracker.portfolio import Portfolio
from stock_portfolio_tracker.stock import Stock


# ANSI color codes (disabled on Windows without VT support handled by caller)
class Colors:
    """ANSI escape sequences for terminal styling."""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def enable_windows_ansi() -> None:
    """Enable ANSI colors on Windows 10+ terminals."""
    if sys.platform == "win32":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except (AttributeError, OSError):
            pass


def clear_screen() -> None:
    """Clear the terminal screen cross-platform."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """Display application title banner."""
    banner = r"""
  ____  _             _      ____            _ _     _
 / ___|| |_ ___  __ _| | __ |  _ \ ___  _ __| (_) __| | ___ _ __
 \___ \| __/ _ \/ _` | |/ / | |_) / _ \| '__| | |/ _` |/ _ \ '__|
  ___) | ||  __/ (_| |   <  |  __/ (_) | |  | | | (_| |  __/ |
 |____/ \__\___|\__,_|_|\_\ |_|   \___/|_|  |_|_|\__,_|\___|_|
"""
    print(f"{Colors.CYAN}{Colors.BOLD}{banner}{Colors.RESET}")
    print(
        f"{Colors.DIM}  CodeAlpha Python Programming Internship"
        f" — Stock Portfolio Tracker v1.0{Colors.RESET}\n"
    )


def print_separator(char: str = "=", width: int = 60) -> None:
    """Print a horizontal separator line."""
    print(f"{Colors.DIM}{char * width}{Colors.RESET}")


def print_menu() -> None:
    """Display the main application menu."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}  MAIN MENU{Colors.RESET}")
    print_separator("-")
    options = [
        ("1", "Add stock to portfolio"),
        ("2", "View portfolio summary"),
        ("3", "Calculate total investment"),
        ("4", "Portfolio analytics"),
        ("5", "Remove a stock"),
        ("6", "View available stocks & prices"),
        ("7", "Export report (TXT & CSV)"),
        ("8", "Clear portfolio"),
        ("0", "Exit program"),
    ]
    for key, label in options:
        print(f"  {Colors.CYAN}[{key}]{Colors.RESET} {label}")
    print_separator("-")


def print_success(message: str) -> None:
    """Print a success message in green."""
    print(f"\n{Colors.GREEN}✓ {message}{Colors.RESET}")


def print_error(message: str) -> None:
    """Print an error message in red."""
    print(f"\n{Colors.RED}✗ Error: {message}{Colors.RESET}")


def print_info(message: str) -> None:
    """Print an informational message."""
    print(f"\n{Colors.YELLOW}ℹ {message}{Colors.RESET}")


def print_stock_prices() -> None:
    """Display predefined stock prices table."""
    print(f"\n{Colors.BOLD}  AVAILABLE STOCKS & PRICES{Colors.RESET}")
    print_separator()
    print(f"  {'Symbol':<10} {'Price (USD)':>15}")
    print_separator("-")
    for symbol, price in sorted(STOCK_PRICES.items()):
        print(f"  {Colors.CYAN}{symbol:<10}{Colors.RESET} ${price:>14,.2f}")
    print_separator()


def print_portfolio_summary(portfolio: Portfolio) -> None:
    """
    Display formatted portfolio summary with individual stock values.

    Args:
        portfolio: Portfolio instance to display.
    """
    print(f"\n{Colors.BOLD}  PORTFOLIO SUMMARY — {portfolio.name}{Colors.RESET}")
    print_separator()

    if portfolio.is_empty:
        print_info("Your portfolio is empty. Add stocks using menu option 1.")
        return

    print(f"  {'Symbol':<8} {'Qty':>6} {'Price':>12} {'Value':>14}")
    print_separator("-")

    for stock in portfolio.list_holdings():
        print(
            f"  {Colors.CYAN}{stock.symbol:<8}{Colors.RESET}"
            f" {stock.quantity:>6}"
            f" ${stock.price_per_share:>10,.2f}"
            f" ${stock.total_value:>12,.2f}"
        )

    print_separator("-")
    print(
        f"  {Colors.BOLD}{'TOTAL INVESTMENT':<26}"
        f" ${portfolio.total_investment:>12,.2f}{Colors.RESET}"
    )
    print_separator()


def print_total_investment(portfolio: Portfolio) -> None:
    """Display total investment value prominently."""
    print(f"\n{Colors.BOLD}  TOTAL INVESTMENT VALUE{Colors.RESET}")
    print_separator()
    if portfolio.is_empty:
        print_info("No holdings. Total investment is $0.00.")
        return
    print(
        f"\n  {Colors.GREEN}{Colors.BOLD}"
        f"${portfolio.total_investment:,.2f}{Colors.RESET}"
    )
    print(f"\n  Across {portfolio.stock_count} stock(s), "
          f"{portfolio.total_shares:,} total shares.\n")


def print_analytics(portfolio: Portfolio) -> None:
    """
    Display portfolio analytics including most valuable stock.

    Args:
        portfolio: Portfolio to analyze.
    """
    analytics = portfolio.get_analytics()
    allocation = portfolio.get_allocation()

    print(f"\n{Colors.BOLD}  PORTFOLIO ANALYTICS{Colors.RESET}")
    print_separator()

    if portfolio.is_empty:
        print_info("Add stocks to view analytics.")
        return

    most_symbol = analytics["most_valuable_symbol"]
    most_value = analytics["most_valuable_value"]
    least_symbol = analytics["least_valuable_symbol"]
    least_value = analytics["least_valuable_value"]

    print(f"  Portfolio Name      : {analytics['portfolio_name']}")
    print(f"  Distinct Stocks     : {analytics['stock_count']}")
    print(f"  Total Shares        : {analytics['total_shares']:,}")
    print(f"  Total Investment    : ${analytics['total_investment']:,.2f}")
    print(f"  Avg Holding Value   : ${analytics['average_holding_value']:,.2f}")
    print_separator("-")
    print(
        f"  {Colors.GREEN}Most Valuable Stock : "
        f"{most_symbol} (${most_value:,.2f}){Colors.RESET}"
    )
    print(
        f"  Least Valuable Stock: "
        f"{least_symbol} (${least_value:,.2f})"
    )
    print_separator("-")
    print(f"\n  {Colors.BOLD}Asset Allocation (%){Colors.RESET}")
    for symbol, pct in sorted(allocation.items(), key=lambda x: -x[1]):
        bar_len = int(pct / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {symbol:<6} {bar} {pct:>5.1f}%")
    print_separator()


def print_holdings_detail(stocks: Iterable[Stock]) -> None:
    """Print individual stock value lines."""
    for stock in stocks:
        print(f"  • {stock}")

def pause() -> None:
    """Wait for user to press Enter before continuing."""
    try:
        input(f"\n{Colors.DIM}  Press Enter to continue...{Colors.RESET}")
    except (EOFError, KeyboardInterrupt):
        pass
