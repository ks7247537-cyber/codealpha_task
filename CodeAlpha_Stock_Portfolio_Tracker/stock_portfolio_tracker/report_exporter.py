"""
Export portfolio reports to TXT and CSV files.
"""

import csv
from datetime import datetime
from pathlib import Path

from stock_portfolio_tracker.constants import REPORTS_DIR, REPORT_PREFIX
from stock_portfolio_tracker.portfolio import Portfolio


class ReportExporter:
    """Generate and save portfolio reports in multiple formats."""

    def __init__(self, output_dir: Path | None = None) -> None:
        """
        Initialize the report exporter.

        Args:
            output_dir: Directory for saved reports. Defaults to reports/.
        """
        self.output_dir = output_dir or REPORTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _timestamp(self) -> str:
        """Return a filesystem-safe timestamp string."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _base_filename(self) -> str:
        """Build report base name with timestamp."""
        return f"{REPORT_PREFIX}_{self._timestamp()}"

    def export_txt(self, portfolio: Portfolio) -> Path:
        """
        Save a detailed text report of the portfolio.

        Args:
            portfolio: Portfolio to export.

        Returns:
            Path to the created TXT file.
        """
        filepath = self.output_dir / f"{self._base_filename()}.txt"
        analytics = portfolio.get_analytics()
        allocation = portfolio.get_allocation()
        most = portfolio.get_most_valuable_stock()

        lines = [
            "=" * 60,
            "STOCK PORTFOLIO TRACKER — REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            "",
            f"Portfolio Name: {portfolio.name}",
            "",
            "-" * 60,
            "HOLDINGS",
            "-" * 60,
        ]

        if portfolio.is_empty:
            lines.append("  (No holdings in portfolio)")
        else:
            lines.append(
                f"{'Symbol':<10}{'Qty':>8}{'Price':>12}{'Value':>14}"
            )
            lines.append("-" * 60)
            for stock in portfolio.list_holdings():
                lines.append(
                    f"{stock.symbol:<10}{stock.quantity:>8}  "
                    f"${stock.price_per_share:>10,.2f}  "
                    f"${stock.total_value:>12,.2f}"
                )

        lines.extend([
            "",
            "-" * 60,
            "SUMMARY",
            "-" * 60,
            f"Total Investment     : ${analytics['total_investment']:,.2f}",
            f"Distinct Stocks        : {analytics['stock_count']}",
            f"Total Shares           : {analytics['total_shares']:,}",
            f"Average Holding Value  : ${analytics['average_holding_value']:,.2f}",
        ])

        if most:
            lines.extend([
                "",
                "-" * 60,
                "MOST VALUABLE STOCK",
                "-" * 60,
                f"  {most.symbol}: ${most.total_value:,.2f} "
                f"({most.quantity} shares @ ${most.price_per_share:.2f})",
            ])

        if allocation:
            lines.extend([
                "",
                "-" * 60,
                "ASSET ALLOCATION (%)",
                "-" * 60,
            ])
            for symbol, pct in sorted(allocation.items(), key=lambda x: -x[1]):
                lines.append(f"  {symbol:<8} {pct:>6.2f}%")

        lines.extend(["", "=" * 60, "End of Report", "=" * 60, ""])

        filepath.write_text("\n".join(lines), encoding="utf-8")
        return filepath

    def export_csv(self, portfolio: Portfolio) -> Path:
        """
        Save portfolio holdings and summary to CSV.

        Args:
            portfolio: Portfolio to export.

        Returns:
            Path to the created CSV file.
        """
        filepath = self.output_dir / f"{self._base_filename()}.csv"
        analytics = portfolio.get_analytics()

        with filepath.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(["STOCK PORTFOLIO TRACKER — CSV REPORT"])
            writer.writerow([
                "Generated",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ])
            writer.writerow(["Portfolio Name", portfolio.name])
            writer.writerow([])

            writer.writerow([
                "Symbol", "Quantity", "Price Per Share", "Total Value",
            ])

            if portfolio.is_empty:
                writer.writerow(["(empty)", 0, 0, 0])
            else:
                for stock in portfolio.list_holdings():
                    writer.writerow([
                        stock.symbol,
                        stock.quantity,
                        f"{stock.price_per_share:.2f}",
                        f"{stock.total_value:.2f}",
                    ])

            writer.writerow([])
            writer.writerow(["SUMMARY METRICS"])
            writer.writerow([
                "Total Investment", f"{analytics['total_investment']:.2f}",
            ])
            writer.writerow([
                "Stock Count", analytics["stock_count"],
            ])
            writer.writerow([
                "Total Shares", analytics["total_shares"],
            ])
            writer.writerow([
                "Most Valuable Symbol",
                analytics["most_valuable_symbol"] or "N/A",
            ])
            writer.writerow([
                "Most Valuable Value",
                f"{analytics['most_valuable_value']:.2f}",
            ])

            allocation = portfolio.get_allocation()
            if allocation:
                writer.writerow([])
                writer.writerow(["ALLOCATION"])
                writer.writerow(["Symbol", "Percentage"])
                for symbol, pct in allocation.items():
                    writer.writerow([symbol, f"{pct:.2f}"])

        return filepath

    def export_all(self, portfolio: Portfolio) -> tuple[Path, Path]:
        """
        Export both TXT and CSV reports.

        Args:
            portfolio: Portfolio to export.

        Returns:
            Tuple of (txt_path, csv_path).
        """
        txt_path = self.export_txt(portfolio)
        csv_path = self.export_csv(portfolio)
        return txt_path, csv_path
