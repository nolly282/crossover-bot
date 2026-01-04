## Customization Guide

The bot was written in a way that allows key trading parameters to be adjusted directly from the class configuration section of the code.

All customizations can be made inside the `__init__` method of the `TradingBot` class in `bot.py`.

---

### Trading Symbol

To change the trading instrument, modify the `self.symbol` variable.

```python
self.symbol = "BTCUSD"

Replace "BTCUSD" with any symbol available in your MetaTrader 5 terminal, for example:

self.symbol = "XAUUSD"
self.symbol = "EURUSD"


Timeframe
The timeframe is controlled by the self.timeframe variable.

self.timeframe = mt5.TIMEFRAME_M3
You can change this to any MT5-supported timeframe, such as:
mt5.TIMEFRAME_M1   # 1 minute
mt5.TIMEFRAME_M5   # 5 minutes
mt5.TIMEFRAME_M15  # 15 minutes
mt5.TIMEFRAME_H1   # 1 hour


Moving Average Periods
The fast and slow moving average periods are defined as follows:
self.fsma_period = 15   # Fast moving average
self.ssma_period = 43   # Slow moving average

You may adjust these values to test different crossover combinations, for example:
self.fsma_period = 10
self.ssma_period = 50


Lot Size
Trade volume is controlled using the self.lot variable:

self.lot = 0.1
Adjust this value according to your broker’s lot size requirements.

Take-Profit Value
The take-profit threshold is defined here:

self.tp = 10
This value represents the profit level at which open positions will be closed automatically.

Number of Candles Fetched
The number of historical candles fetched for analysis is controlled by:

self.num_bars = 1000
You can increase or reduce this number depending on how much historical data you want the bot to process.

Polling Interval
The bot checks for new market data at fixed intervals, defined at the end of the main loop:

self.looptime = 10
This value is measured in seconds and can be adjusted to control how frequently the bot evaluates market conditions.
10 means it will loop every ten seconds
