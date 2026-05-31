"""
PortfolioManager orchestrates portfolio operations and the CLI workflow.
"""

from __future__ import annotations

from stock_portfolio_tracker.portfolio import Portfolio
from stock_portfolio_tracker.report_exporter import ReportExporter
from stock_portfolio_tracker.stock import Stock
from stock_portfolio_tracker import ui
from stock_portfolio_tracker.validators import (
    ValidationError,
    validate_menu_choice,
    validate_quantity,
    validate_symbol,
)


class PortfolioManager:
    """
    High-level controller for portfolio management and user interaction.

    Coordinates between Portfolio model, validation, UI, and report export.
    """

    MENU_MIN = 0
    MENU_MAX = 8

    def __init__(self, portfolio_name: str = "My Portfolio") -> None:
        """
        Initialize the portfolio manager.

        Args:
            portfolio_name: Default name for the managed portfolio.
        """
        self.portfolio = Portfolio(name=portfolio_name)
        self.report_exporter = ReportExporter()
        self._running = False

    def add_stock_interactive(self) -> None:
        """Prompt user for symbol and quantity, then add to portfolio."""
        try:
            symbol_input = input(
                f"\n  {ui.Colors.CYAN}Enter stock symbol "
                f"(e.g., AAPL): {ui.Colors.RESET}"
            ).strip()
            symbol = validate_symbol(symbol_input)

            quantity_input = input(
                f"  {ui.Colors.CYAN}Enter quantity (shares): "
                f"{ui.Colors.RESET}"
            ).strip()
            quantity = validate_quantity(quantity_input)

            stock = Stock.from_symbol(symbol, quantity)
            self.portfolio.add_stock(stock)

            ui.print_success(
                f"Added {quantity} share(s) of {symbol} "
                f"(value: ${stock.total_value:,.2f})."
            )

            if symbol in self.portfolio.holdings:
                merged = self.portfolio.holdings[symbol]
                if merged.quantity > quantity:
                    ui.print_info(
                        f"Merged with existing position. "
                        f"Total {symbol}: {merged.quantity} shares."
                    )

        except ValidationError as err:
            ui.print_error(str(err))
        except KeyError as err:
            ui.print_error(str(err))
        except Exception as err:
            ui.print_error(f"Unexpected error while adding stock: {err}")

    def remove_stock_interactive(self) -> None:
        """Prompt user to remove a stock from the portfolio."""
        if self.portfolio.is_empty:
            ui.print_info("Portfolio is empty. Nothing to remove.")
            return

        try:
            symbol_input = input(
                f"\n  {ui.Colors.CYAN}Enter symbol to remove: "
                f"{ui.Colors.RESET}"
            ).strip()
            symbol = validate_symbol(symbol_input)

            if self.portfolio.remove_stock(symbol):
                ui.print_success(f"Removed {symbol} from portfolio.")
            else:
                ui.print_error(f"{symbol} is not in your portfolio.")

        except ValidationError as err:
            ui.print_error(str(err))

    def view_summary(self) -> None:
        """Display portfolio summary with individual stock values."""
        ui.print_portfolio_summary(self.portfolio)

    def calculate_investment(self) -> None:
        """Display total investment and per-stock breakdown."""
        ui.print_total_investment(self.portfolio)
        if not self.portfolio.is_empty:
            print(f"  {ui.Colors.BOLD}Individual Stock Values:{ui.Colors.RESET}")
            ui.print_holdings_detail(self.portfolio.list_holdings())

    def show_analytics(self) -> None:
        """Display portfolio analytics including most valuable stock."""
        ui.print_analytics(self.portfolio)

    def export_reports(self) -> None:
        """Export portfolio to TXT and CSV files."""
        if self.portfolio.is_empty:
            ui.print_info(
                "Cannot export an empty portfolio. Add stocks first."
            )
            return

        try:
            txt_path, csv_path = self.report_exporter.export_all(
                self.portfolio
            )
            ui.print_success("Reports saved successfully!")
            print(f"\n  TXT: {txt_path}")
            print(f"  CSV: {csv_path}\n")
        except OSError as err:
            ui.print_error(f"Failed to write report files: {err}")
        except Exception as err:
            ui.print_error(f"Export failed: {err}")

    def clear_portfolio(self) -> None:
        """Clear all holdings after user confirmation."""
        if self.portfolio.is_empty:
            ui.print_info("Portfolio is already empty.")
            return

        confirm = input(
            f"\n  {ui.Colors.YELLOW}Clear all holdings? (yes/no): "
            f"{ui.Colors.RESET}"
        ).strip().lower()

        if confirm in ("yes", "y"):
            self.portfolio.clear()
            ui.print_success("Portfolio cleared.")
        else:
            ui.print_info("Clear operation cancelled.")

    def process_menu_choice(self, choice: int) -> bool:
        """
        Execute the action for a validated menu choice.

        Args:
            choice: Menu option number (0-8).

        Returns:
            False if the application should exit, True otherwise.
        """
        actions = {
            1: self.add_stock_interactive,
            2: self.view_summary,
            3: self.calculate_investment,
            4: self.show_analytics,
            5: self.remove_stock_interactive,
            6: ui.print_stock_prices,
            7: self.export_reports,
            8: self.clear_portfolio,
        }

        if choice == 0:
            return False

        action = actions.get(choice)
        if action:
            action()
            if choice != 6:
                ui.pause()
        return True

    def run(self) -> None:
        """Start the main menu-driven CLI loop."""
        ui.enable_windows_ansi()
        self._running = True

        while self._running:
            try:
                ui.clear_screen()
                ui.print_banner()
                ui.print_menu()

                raw_choice = input(
                    f"\n  {ui.Colors.BOLD}Select an option: "
                    f"{ui.Colors.RESET}"
                )
                choice = validate_menu_choice(
                    raw_choice, self.MENU_MIN, self.MENU_MAX
                )

                if choice == 0:
                    ui.clear_screen()
                    ui.print_banner()
                    print(
                        f"\n  {ui.Colors.GREEN}Thank you for using "
                        f"Stock Portfolio Tracker. Goodbye!{ui.Colors.RESET}\n"
                    )
                    self._running = False
                else:
                    self._running = self.process_menu_choice(choice)

            except ValidationError as err:
                ui.print_error(str(err))
                ui.pause()
            except KeyboardInterrupt:
                print(f"\n\n  {ui.Colors.YELLOW}Interrupted. Exiting...{ui.Colors.RESET}\n")
                self._running = False
            except EOFError:
                self._running = False
