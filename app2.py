# --------------------------------------------------------------------
# app2.py : Compare different strategies based on technical indicators
# Backtest strategies on historical data stored as CSV file
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

df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%Y')
df.set_index('Date', inplace=True)

print(df)

#--------------------------------------------------

# Store backtest results
cumulative_returns = pd.DataFrame(index=df.index)

# Define strategies and methods
strategies = ["RSI", "MACD", "Bollinger", "Breakout", "MA_Crossover"]

# Apply each strategy and store cumulative returns
for strategy in strategies:
    # Initialize Strategy Class
    ts = TradingStrategies(df.copy())  # reinitialize to avoid signal overlap
    if strategy == "RSI":
      ts.rsi_strategy()
    elif strategy == "MACD":
      ts.macd_strategy()
    elif strategy == "Bollinger":
      ts.bollinger_bands_strategy()
    elif strategy == "Breakout":
      ts.breakout_strategy()
    elif strategy == "MA_Crossover":
      ts.moving_average_crossover_strategy()        
    result = ts.backtest_strategy()
    cumulative_returns[strategy] = result['Cumulative_Strategy_Returns']

    # Save market returns from the first result only
    if 'Market' not in cumulative_returns.columns:
        cumulative_returns['Market'] = result['Cumulative_Market_Returns']

# Plot all strategies
plt.figure(figsize=(12, 6))
for column in cumulative_returns.columns:
    plt.plot(cumulative_returns.index, cumulative_returns[column], label=column)

plt.title("Backtest Comparison: Strategy vs Market")
plt.xlabel("Date")
plt.ylabel("Cumulative Returns")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()