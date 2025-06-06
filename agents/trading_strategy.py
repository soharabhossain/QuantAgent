import pandas as pd
import numpy as np

class TradingStrategies:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def moving_average_crossover_strategy(self, short_window=50, long_window=200):
        self.data['SMA50'] = self.data['Close'].rolling(window=short_window).mean()
        self.data['SMA200'] = self.data['Close'].rolling(window=long_window).mean()
        self.data['Signal'] = np.where(self.data['SMA50'] > self.data['SMA200'], 1, 0)
        self.data['Position'] = self.data['Signal'].diff()
        return self.data[['SMA50', 'SMA200', 'Signal', 'Position']]

    def rsi_strategy(self, period=14):
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        self.data['Signal'] = np.where(self.data['RSI'] < 30, 1, np.where(self.data['RSI'] > 70, -1, 0))
        return self.data[['RSI', 'Signal']]

    def breakout_strategy(self):
        self.data['Support'] = self.data['Close'].rolling(window=20).min()
        self.data['Resistance'] = self.data['Close'].rolling(window=20).max()
        self.data['Signal'] = np.where(self.data['Close'] > self.data['Resistance'], 1,
                                       np.where(self.data['Close'] < self.data['Support'], -1, 0))
        return self.data[['Support', 'Resistance', 'Signal']]

    def macd_strategy(self):
        exp1 = self.data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = self.data['Close'].ewm(span=26, adjust=False).mean()
        self.data['MACD'] = exp1 - exp2
        self.data['SignalLine'] = self.data['MACD'].ewm(span=9, adjust=False).mean()
        self.data['Signal'] = np.where(self.data['MACD'] > self.data['SignalLine'], 1, -1)
        return self.data[['MACD', 'SignalLine', 'Signal']]

    def volume_strategy(self):
        self.data['AvgVolume'] = self.data['Volume'].rolling(window=20).mean()
        self.data['Signal'] = np.where(self.data['Volume'] > self.data['AvgVolume'], 1, 0)
        return self.data[['Volume', 'AvgVolume', 'Signal']]

    def bollinger_bands_strategy(self, window=20):
        self.data['MA20'] = self.data['Close'].rolling(window=window).mean()
        self.data['Upper'] = self.data['MA20'] + 2 * self.data['Close'].rolling(window=window).std()
        self.data['Lower'] = self.data['MA20'] - 2 * self.data['Close'].rolling(window=window).std()
        self.data['Signal'] = np.where(self.data['Close'] < self.data['Lower'], 1,
                                       np.where(self.data['Close'] > self.data['Upper'], -1, 0))
        return self.data[['MA20', 'Upper', 'Lower', 'Signal']]

    def adx_strategy(self, period=14):
        high = self.data['High']
        low = self.data['Low']
        close = self.data['Close']
        plus_dm = high.diff()
        minus_dm = low.diff()
        tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
        self.data['ADX'] = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        return self.data[['ADX']]

    def ichimoku_strategy(self):
        self.data['Tenkan_sen'] = (self.data['High'].rolling(window=9).max() + self.data['Low'].rolling(window=9).min()) / 2
        self.data['Kijun_sen'] = (self.data['High'].rolling(window=26).max() + self.data['Low'].rolling(window=26).min()) / 2
        self.data['Senkou_span_A'] = ((self.data['Tenkan_sen'] + self.data['Kijun_sen']) / 2).shift(26)
        self.data['Senkou_span_B'] = ((self.data['High'].rolling(window=52).max() + self.data['Low'].rolling(window=52).min()) / 2).shift(26)
        self.data['Chikou_span'] = self.data['Close'].shift(-26)
        self.data['Signal'] = np.where(self.data['Close'] > self.data['Kijun_sen'], 1, -1)
        return self.data[['Tenkan_sen', 'Kijun_sen', 'Senkou_span_A', 'Senkou_span_B', 'Chikou_span', 'Signal']]

    def fibonacci_retracement_levels(self):
        max_price = self.data['Close'].max()
        min_price = self.data['Close'].min()
        diff = max_price - min_price
        levels = {
            'Level_0': max_price,
            'Level_0.236': max_price - 0.236 * diff,
            'Level_0.382': max_price - 0.382 * diff,
            'Level_0.5': max_price - 0.5 * diff,
            'Level_0.618': max_price - 0.618 * diff,
            'Level_1': min_price
        }
        return levels

    def backtest_strategy(self, signal_col='Signal'):
        self.data['Daily_Return'] = self.data['Close'].pct_change()
        self.data['Strategy_Return'] = self.data[signal_col].shift(1) * self.data['Daily_Return']
        self.data['Cumulative_Market_Returns'] = (1 + self.data['Daily_Return']).cumprod()
        self.data['Cumulative_Strategy_Returns'] = (1 + self.data['Strategy_Return']).cumprod()
        return self.data[['Daily_Return', 'Strategy_Return', 'Cumulative_Market_Returns', 'Cumulative_Strategy_Returns']]
