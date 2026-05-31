# Stock Portfolio Tracker

A professional **Python Object-Oriented Programming (OOP)** project built for the **CodeAlpha Python Programming Internship**. This application lets users manage a stock portfolio, calculate investment values, view analytics, and export reports through a clean, menu-driven command-line interface.

---

## Project Overview

The Stock Portfolio Tracker simulates a personal investment portfolio using predefined stock prices. Users can add holdings, view summaries, analyze performance metrics (including the most valuable stock), and save detailed reports as **TXT** and **CSV** files.

The design follows **separation of concerns**: domain models (`Stock`, `Portfolio`), business logic (`PortfolioManager`), validation, UI rendering, and report export are organized into dedicated modules.

---

## Features

| Feature | Description |
|--------|-------------|
| **Add stocks** | Enter ticker symbol and share quantity |
| **Portfolio summary** | Table of holdings with per-stock and total value |
| **Total investment** | Aggregate portfolio value with per-stock breakdown |
| **Analytics** | Most/least valuable stock, allocation %, averages |
| **Remove stocks** | Delete a symbol from the portfolio |
| **Price lookup** | View all supported tickers and prices |
| **Report export** | Save TXT and CSV reports to `reports/` |
| **Input validation** | Symbols, quantities, and menu choices validated |
| **Exception handling** | Graceful errors for invalid input and I/O failures 

## Technologies Used

- **Python 3.10+** (recommended)
- **Standard library only** — `csv`, `dataclasses`, `pathlib`, `datetime`, `os`, `sys`
- **OOP** — Classes: `Stock`, `Portfolio`, `PortfolioManager`, `ReportExporter`
- **PEP 8** coding style with docstrings and module comments

---

## Folder Structure

```
CodeAlpha_Stock_Portfolio_Tracker/
├── main.py                          # Application entry point
├── requirements.txt                 # Dependencies (stdlib only)
├── README.md                        # Project documentation
├── stock_portfolio_tracker/         # Main package
│   ├── __init__.py
│   ├── constants.py                 # Stock prices & paths
│   ├── stock.py                     # Stock class
│   ├── portfolio.py                 # Portfolio class
│   ├── portfolio_manager.py         # PortfolioManager + CLI flow
│   ├── validators.py                # Input validation
│   ├── ui.py                        # Terminal UI helpers
│   └── report_exporter.py           # TXT & CSV export
├── reports/                         # Generated reports (output)
├── samples/
│   └── sample_output.txt            # Example terminal & report output
```

---

## Installation Steps

### Prerequisites

- Python **3.10** or newer installed
- Terminal (Command Prompt, PowerShell, or bash)

### Setup

1. **Clone or download** the project folder.

2. **Open a terminal** in the project root:

   ```bash
   cd CodeAlpha_Stock_Portfolio_Tracker
   ```

3. **(Optional)** Create a virtual environment:

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

4. **Install dependencies** (no external packages required):

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage Instructions

### Run the application

```bash
python main.py
```

### Supported stock symbols & prices

| Symbol | Price (USD) |
|--------|-------------|
| AAPL   | 180.00      |
| TSLA   | 250.00      |
| GOOGL  | 140.00      |
| MSFT   | 330.00      |
| AMZN   | 145.00      |

### Menu options

| Option | Action |
|--------|--------|
| **1** | Add stock (symbol + quantity) |
| **2** | View portfolio summary |
| **3** | Calculate total investment |
| **4** | Portfolio analytics |
| **5** | Remove a stock |
| **6** | View available stocks & prices |
| **7** | Export report (TXT & CSV) |
| **8** | Clear portfolio |
| **0** | Exit program |

### Example workflow

1. Run `python main.py`
2. Choose **1** to add `AAPL` with quantity `10`
3. Add `MSFT` (5 shares) and `TSLA` (8 shares)
4. Choose **2** for summary, **4** for analytics
5. Choose **7** to export reports to the `reports/` folder
6. Choose **0** to exit

See [`samples/sample_output.txt`](samples/sample_output.txt) for full example output.

---

## Class Design (OOP)

### `Stock`

- Attributes: `symbol`, `quantity`, `price_per_share`
- Methods: `from_symbol()`, `total_value` property
- Creates holdings from the predefined price dictionary

### `Portfolio`

- Manages multiple `Stock` instances
- Methods: `add_stock()`, `remove_stock()`, `get_analytics()`, `get_most_valuable_stock()`
- Computes `total_investment` and asset allocation

### `PortfolioManager`

- Orchestrates user interaction and menu loop
- Delegates validation, UI, and report export
- Implements the menu-driven CLI workflow

