# stock_plotter.py
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf

from stock_indicators import StockIndicators


class StockPlotter:
    def __init__(self, tickers, stock_data):
        self.tickers = tickers
        self.stock_data = stock_data

    def plot(self, plot_type='line', resample=None, window_ma=30, window_rsi=14):
        closing_prices, opening_prices, volumes, low, high = self.stock_data.get_prices()

        if resample:
            self.stock_data.resample_data(resample)

        if plot_type == 'line':
            self._plot_line(closing_prices)
        elif plot_type == 'candlestick':
            self._plot_candlestick(
                opening_prices, closing_prices, volumes, low, high, window_ma, window_rsi)
        elif plot_type == 'bar':
            self._plot_bar(volumes)
        else:
            raise ValueError(
                "Unsupported plot type. Use 'line', 'candlestick', or 'bar'.")
        plt.show()

    def _plot_line(self, closing_prices):
        plt.figure(figsize=(12, 8))
        for ticker in self.tickers:
            plt.plot(closing_prices.index,
                     closing_prices[ticker], label=f'{ticker} Close Price')

        plt.title(f'{",".join(self.tickers)} Closing Prices - Line Plot')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        plt.grid(False)

    def _plot_candlestick(self, opening_prices, closing_prices, volumes, low, high, window_ma, window_rsi):
        for ticker in self.tickers:
            data_df = pd.DataFrame({
                'Open': opening_prices[ticker],
                'High': high[ticker],
                'Low': low[ticker],
                'Close': closing_prices[ticker],
                'Volume': volumes[ticker]
            }).dropna()

            indicators = StockIndicators(data_df['Close'])
            simple_ma = indicators.calculate_sma(window_ma)
            exponential_ma = indicators.calculate_ema(window_ma)
            rsi = indicators.calculate_rsi(window_rsi)

            data_df['SMA_30'] = simple_ma
            data_df['EMA_30'] = exponential_ma
            data_df['RSI_14'] = rsi

            add_plots = [
                mpf.make_addplot(
                    data_df['SMA_30'], color='darkslateblue', label='SMA 30', panel=0),
                mpf.make_addplot(
                    data_df['EMA_30'], color='blue', label='EMA 30', panel=0),
                mpf.make_addplot(
                    data_df['RSI_14'], color='purple', label='RSI 14', panel=2, ylabel='RSI')
            ]

            title = f'{ticker} Candlestick Chart (SMA({window_ma}), EMA({
                window_ma}), RSI({window_rsi}))'
            mpf.plot(data_df, type='candle', style='yahoo', volume=True,
                     title=title, addplot=add_plots, panel_ratios=(3, 1))

    def _plot_bar(self, volumes):
        plt.figure(figsize=(12, 8))
        for ticker in self.tickers:
            plt.bar(volumes.index, volumes[ticker], label=f'{
                    ticker} Volume', alpha=0.5)

        plt.title(f'{",".join(self.tickers)} Trading Volume')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.legend()
        plt.grid(False)
