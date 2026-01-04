## Installation & Setup

### Requirements

- MetaTrader 5 Terminal
- Python 3.12 or above
- MetaTrader5 Python library (v5.0.47 recommended)
- pandas (v2.2.2 or compatible)

---

### Pre-Installation Checklist

Before running the bot, ensure the following:
- MetaTrader 5 is installed
- A broker account is set up
- Algo trading is enabled in the MT5 terminal
- Your broker allows algorithmic trading
- Python is installed and available in your system PATH

> If this setup feels overwhelming, watching a short tutorial on setting up MT5 and Python can be helpful.

---

## Project Setup

1. Copy `bot.py` into a folder  
   Example:
Desktop/MA_Crossover_Bot



2. Open a terminal (CMD, PowerShell, or equivalent)

3. Navigate to the project folder:
cd Desktop/MA_Crossover_Bot



---

## Install Dependencies

Run the following commands:
pip install MetaTrader5==5.0.47
pip install pandas


---

## Run the Bot

1. Ensure MetaTrader 5 is open and logged in
2. Ensure you are in the project directory
3. Run:
python bot.py


Once started, the bot will begin monitoring the market and executing trades based on the strategy logic.

---

## Customization

The following parameters can be modified directly in the code:
- Trading symbol
- Timeframe
- Fast and slow moving average periods
- Lot size
- Take-profit value
- Number of candles fetched



Check the customization.md file for details on how to change the parameters