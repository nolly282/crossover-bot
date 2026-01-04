# last modification 23 Oct 2024
# Import necessary libraries
# import numpy as np
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import time

if mt5.initialize():
    print("connected to MetaTrader5 successfully")
else:
    print("connection to MetaTrader5 failed", mt5.last_error())


# create bot class
class TradingBot:
    def __init__(self):
        self.open_positions = []  # List to store open positions
        self.symbol = "BTCUSD" #input("Enter symbol: ").upper() # "BTCUSD"  # symbol
        self.ticks_df = pd.DataFrame()

        self.timeframe = mt5.TIMEFRAME_M3
        self.num_bars = 1000 # number of candles to store in ticks_df dataframe
        self.lot = 0.1 # lot size
        self.tp = 10 # take profit price
        # self.sl = -6
        self.looptime = 10

        self.new_candle = pd.DataFrame()
        self.trade_flag = False # Trade indicator
        self.last_candle_time = None # last candle time
        # SMA info
        self.ssma_period = 43 # Slow moving average
        self.fsma_period = 15 # fast moving average
        # trend info
        self.bullish = False  # bullish flag
        self.bearish = False  # bearish flag

        self.opf_long = False # to identify when there is an open position for long
        self.opf_short = False

    # function to check for open positions
    def check_for_positions(self):
        positions = mt5.positions_get()  # use mt5 position get function to get open positions
        self.open_positions = []  # Clear the list incase there are previous open positions
        if positions:
            print("Open positions:")
            for i, position in enumerate(positions, 1): # loop through each position index
                trade_type = "Long" if position.type == mt5.ORDER_TYPE_BUY else "Short"  # check trade type and store in "trade_type"

                if trade_type == "Long":
                    self.opf_long = True # open position flag long
                elif trade_type == "Short":
                    self.opf_short = True  # open position flag long

                # note each position "ticket", "symbol", "type" and profit
                print(f"{i}. Ticket: {position.ticket}, Symbol: {position.symbol}, "
                      f"Trade: {trade_type}, profit: {position.profit}")
                self.open_positions.append(position)  # add new position to the list

        else:
            self.opf_long = False # if no open positions open_position_flag remain False
            self.opf_short = False
            print("No open positions")

    # a function that fetches candle data and store it on a dataframe
    def get_sma_data(self):
        # fetch data from MetaTrader5 and store in ticks
        ticks = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, self.num_bars)
        if ticks is None or len(ticks) == 0: # check if any data is found
            print("failed to fetch data", mt5.last_error()) # print if no data is found
            return
        # convert to pandas dataframe and store in the class
        self.ticks_df = pd.DataFrame(ticks)[["time", "open", "high", "low", "close"]]
        # make the time readable
        self.ticks_df["time"] = (pd.to_datetime(self.ticks_df["time"], unit="s"))

        self.calc_sma()  # call calc_sma method
        # print(self.ticks_df)

    # a function to calculate SMA of the tick_df data
    def calc_sma(self):
        # ensure that the dataframe is not empty to avoid error
        if self.ticks_df.empty:
            print("dataframe is empty, failed to calculate SMA")
            return
        # calculate SMA and add to dataframe
        self.ticks_df["fast_sma"] = self.ticks_df["close"].rolling(self.fsma_period).mean()
        self.ticks_df["slow_sma"] = self.ticks_df["close"].rolling(self.ssma_period).mean()
        # self.ticks_df["trend"] = self.ticks_df["close"].rolling(self.tsma_period).mean()

        # defined the crossing
        self.ticks_df["prev_fast_sma"] = self.ticks_df["fast_sma"].shift(1)
        self.ticks_df.dropna(inplace=True)  # Drop rows with NaN values
        # print(self.ticks_df)

    # function to define crossovers
    def find_crossover(self, row):
        # define data to determine crossover from row in dataframe
        fast_sma = row["fast_sma"]
        prev_fast_sma = row["prev_fast_sma"]
        slow_sma = row["slow_sma"]
        candle_close = row["close"]
        # condition to indentify bullish and bearish crossing
        if fast_sma > slow_sma >= prev_fast_sma and candle_close > slow_sma > prev_fast_sma:  # bullish crossover condition
            self.bullish = True  # change the bullish flag to True if bullish condition is met
            self.bearish = False  # ensure the bearish flag is False
            return "bullish crossover"

        elif fast_sma < slow_sma <= prev_fast_sma and candle_close < slow_sma < prev_fast_sma:  # bearish crossover condition
            self.bearish = True  # if bearish condition is met, change bearish flag to True in the class
            self.bullish = False  # make sure the bullish flag is the opposite
            return "bearish crossover"
        else:
            return "None"
        # return None

    # identify crossovers from dataframe
    def detect_crossover(self):
        # check dataframe for data
        if self.ticks_df.empty:
            print("DataFrame is empty, cannot identify crossovers")
            return pd.DataFrame()  # return an empty dataframe if empty

        # call the find_crossover function and store the outcome in a new column "crossover"
        self.ticks_df["crossover"] = self.ticks_df.apply(lambda row: self.find_crossover(row), axis=1)
        # Assign the last row of the DataFrame to self.new_candle
        self.new_candle = self.ticks_df.iloc[[-1]].reset_index(drop=True)


    # function to update the trade flag and last candle time
    def update_trade_flag(self): # to prevent multiple trading from opening in the same candle
        if not self.new_candle.empty:
            latest_candle_time = self.new_candle["time"].iloc[0]  # assign last candle time to latest_candle_time
            # when latest_candle_time stops being = last_candle_time, it means the candle has changed
            if self.last_candle_time is None or latest_candle_time != self.last_candle_time:
                self.trade_flag = False  # then reset the flag for new crossover
                self.last_candle_time = latest_candle_time # make sure the both times remains same
                # so last_candle_time start as None and


    # attempt to create a function that opens long or short position
    def open_position(self, order_type):
        # check what type of order the user selected
        if order_type == mt5.ORDER_TYPE_BUY:
            price = mt5.symbol_info_tick(self.symbol).ask
        else:
            price = mt5.symbol_info_tick(self.symbol).bid

        # opening position request library
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,  # change symbol from class
            "volume": self.lot,  # change lot from class
            "type": order_type,
            "price": price,
            "deviation": 5,
            "type_filling": mt5.ORDER_FILLING_IOC,
            "type_time": mt5.ORDER_TIME_GTC
        }
        # sending the trade order
        trade = mt5.order_send(request)
        if trade.retcode != mt5.TRADE_RETCODE_DONE:  # check if trade failed
            print(f"Failed to open position: {trade.retcode}")
        else:
            print(f"Position opened successfully: {trade}")


    # an attempt to create a function that closes open position
    def close_positions(self):
        profit = None
        loss = None
        for position in self.open_positions:
            tick = mt5.symbol_info_tick(position.symbol)  # identify open position symbol
            if position.profit is not None:
                if position.profit > 0:  # if the value of open position is positive
                    profit = position.profit  # assign it to profit
                elif position.profit < 0:  # if the value is negative
                    loss = position.profit  # assign it to loss

            # close order request dictionary
            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "position": position.ticket,
                "volume": position.volume,  # Adjust the volume as needed
                "type": mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                "price": tick.ask if position.type == mt5.ORDER_TYPE_BUY else tick.bid,
                "deviation": 10,
                "magic": 100,
                "type_filling": mt5.ORDER_FILLING_IOC,
                "type_time": mt5.ORDER_TIME_GTC
            }
            # current_time = datetime.now()

            # send close order request
            if (position.type == mt5.ORDER_TYPE_BUY and self.bearish and not self.trade_flag
                    or position.type == mt5.ORDER_TYPE_SELL and self.bullish and not self.trade_flag
                    or profit is not None and profit >= self.tp):
                    # or loss is not None and loss <= self.sl:

                trade = mt5.order_send(close_request)
                if trade:
                    self.trade_flag = True
                    self.bearish = False
                    self.bullish = False
                    print("Position closed successfully")
                else:
                    print("Position closure failed:", mt5.last_error())

    # function that controls the run flow of the methods
    def run(self):
        while True:
            self.check_for_positions()
            self.get_sma_data()  # initialize data fetch
            # call detect_crossover method which will save the last row of ticks_df as a new DB new_candle
            self.detect_crossover()
            self.close_positions()
            # self.identify_trend()
            self.update_trade_flag()  # call method to update trade flag and last candle time

            # ensure that the new DB new_candle is not empty
            if not self.new_candle.empty:
                if self.new_candle["crossover"].iloc[0] == "None":
                    print("no crossover")  # print the DB is it is None


                elif (self.new_candle["crossover"].iloc[0] == "bullish crossover"
                      and not self.trade_flag
                      and not self.opf_long):
                    self.open_position(mt5.ORDER_TYPE_BUY)
                    self.trade_flag = True


                elif (self.new_candle["crossover"].iloc[0] == "bearish crossover"
                      and not self.trade_flag
                      and not self.opf_short):
                    self.open_position(mt5.ORDER_TYPE_SELL)
                    self.trade_flag = True
                    

            else:
                print("no new candle data available")

            time.sleep(self.looptime)  #wait for a 5 seconds


if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
