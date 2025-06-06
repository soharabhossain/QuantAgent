# --------------------------------------------------------------------
# app3.py : Test individual strategies based on technical indicators
# Backtest individual strategy on historical data stored as CSV file
# --------------------------------------------------------------------

# ---------------------------------
# Import libraries
# ---------------------------------
import pandas as pd
import matplotlib.pyplot as plt
from agents.trading_strategy import TradingStrategies  

#--------------------------------------------------
# Read Data from CSV
column_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover (₹ Cr)']
df = pd.read_csv("NIFTYBANK.csv", names=column_names, header=0)  # Ensure 'Close' is in the DataFrame
print(df)

#--------------------------------------------------
# Trading Strategy
ts = TradingStrategies(df)
ts.rsi_strategy()
# ts.breakout_strategy()
# ts.moving_average_crossover_strategy()
# ts.macd_strategy()
# ts.bollinger_bands_strategy()


# Backtest
result = ts.backtest_strategy()

# Show the plot
# Get plot data
result[['Cumulative_Market_Returns', 'Cumulative_Strategy_Returns']].plot()
plt.title("Backtest: Strategy vs Market")
plt.xlabel("Time")
plt.ylabel("Cumulative Returns")
plt.grid(True)
plt.show()


