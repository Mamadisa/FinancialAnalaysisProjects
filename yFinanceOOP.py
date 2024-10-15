import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import datetime

pd.options.display.max_columns = None


class StockData:
    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers if isinstance(tickers, list) else [tickers]
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.closing_price = None
        self.opening_price = None
        self.volume = None
        self.low = None
        self.high = None

    def fetch_data(self):
        try:
            data = yf.download(
                self.tickers, start=self.start_date, end=self.end_date)
            if data.empty:
                raise ValueError(f'No data found for {self.tickers}.')
            self.data = data
            self._process_data()
        except Exception as e:
            print(f'Error fetching data for {self.tickers}: {e}')
            return None

    def _process_data(self):
        is_single_ticker = len(self.tickers) == 1
        if is_single_ticker:
            ticker = self.tickers[0]
            self.closing_price = pd.DataFrame({ticker: self.data['Close']})
            self.opening_price = pd.DataFrame({ticker: self.data['Open']})
            self.volume = pd.DataFrame({ticker: self.data['Volume']})
            self.low = pd.DataFrame({ticker: self.data['Low']})
            self.high = pd.DataFrame({ticker: self.data['High']})
        else:
            self.closing_price = pd.DataFrame()
            self.opening_price = pd.DataFrame()
            self.volume = pd.DataFrame()
            self.low = pd.DataFrame()
            self.high = pd.DataFrame()

            for ticker in self.tickers:
                self.opening_price[ticker] = self.data[ticker]['Open']
                self.closing_price[ticker] = self.data[ticker]['Close']
                self.volume[ticker] = self.data[ticker]['Volume']
                self.low[ticker] = self.data[ticker]['Low']
                self.high[ticker] = self.data[ticker]['High']

    def resample_data(self, resample_rule):
        self.closing_price = self.closing_price.resample(resample_rule).last()
        self.opening_price = self.opening_price.resample(resample_rule).first()
        self.volume = self.volume.resample(resample_rule).sum()
        self.low = self.low.resample(resample_rule).min()
        self.high = self.high.resample(resample_rule).max()

    def get_prices(self):
        return self.closing_price.round(3), self.opening_price.round(3), self.volume.round(3), self.low.round(3), self.high.round(3)


class StockIndicators:
    def __init__(self, price_data):
        self.price_data = price_data

    def calculate_sma(self, window=30):
        return self.price_data.rolling(window=window).mean()

    def calculate_ema(self, window=30):
        return self.price_data.ewm(span=window, adjust=False).mean()

    def calculate_rsi(self, window=14):
        delta = self.price_data.diff()
        gain = self.price_data.where(
            delta > 0, 0).rolling(window=window).mean()
        loss = -self.price_data.where(delta < 0, 0).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi


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

            add_plots = [mpf.make_addplot(data_df['SMA_30'], color='darkslateblue', label='SMA 30', panel=0),
                         mpf.make_addplot(data_df['EMA_30'],
                                          color='blue', label='EMA 30', panel=0),
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

start_date = datetime.datetime(2023, 1, 1)
end_date = datetime.datetime.now()
stocks = ['SOL.JO']
stock_data = StockData(stocks, start_date, end_date)
stock_data.fetch_data()
plotter = StockPlotter(stocks, stock_data)
plotter.plot(plot_type='candlestick')

