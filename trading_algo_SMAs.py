# -*- coding: utf-8 -*-
"""
Algorithm for Stock Trading Using Simple Moving Averages

@author: Shanta
"""
# Import necessary libraries
import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web

# SMAs to focus on - these are shorter term swings technicals
ma_1 = 9
ma_2 = 21

# Using last 2 years of stock data for newer stocks
start = dt.datetime.now() - dt.timedelta(days=365*2)
end = dt.datetime.now()

# Scrape data off yahoo API
data = web.DataReader('NIO', 'yahoo', start, end)


data[f'SMA_{ma_1}'] = data['Adj Close'].rolling(window=ma_1).mean()
data[f'SMA_{ma_2}'] = data['Adj Close'].rolling(window=ma_2).mean()

data = data.iloc[ma_2:]

# Create lists to track buys, sells, profit, set trigger to guide buy/sells
buy_signals = []
sell_signals = []
profit= [0]
trigger = 0

# Loop through each day to determine buy/sell/hold position; add to profit total
# Trigger used to identify holding periods - no buys and/or sells 
# Find way to remove last buy without sell in profit list

for x in range(len(data)):
    if data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger != 1:
        buy_signals.append(data['Adj Close'].iloc[x])
        sell_signals.append(float('NaN'))
        profit[0] = profit[0] - data['Adj Close'].iloc[x]
        trigger = 1
    elif data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger != -1:
         buy_signals.append(float('NaN'))
         sell_signals.append(data['Adj Close'].iloc[x])
         profit[0] = profit[0] + data['Adj Close'].iloc[x]
         trigger = -1
    else: 
        buy_signals.append(float('NaN'))
        sell_signals.append(float('NaN'))


data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals


# Visualize price movement with signals
plt.style.use("dark_background")
# Share price is in gray, moving averages lines are colored
plt.plot(data['Adj Close'], label="Share Price", alpha = 0.5)
plt.plot(data[f'SMA_{ma_1}'], label=f"SMA_{ma_1}", color="orange", linestyle ="--")
plt.plot(data[f'SMA_{ma_2}'], label=f"SMA_{ma_2}", color="purple", linestyle ="--")
# Buy signal price highlighted with green arrow up, sell with red arrow down
plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="#00ff00", lw=3)
plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="#ff0000", lw=3)
plt.legend(loc="upper left")
plt.show()




