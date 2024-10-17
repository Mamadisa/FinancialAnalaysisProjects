# stock_data.py
import pandas as pd
import yfinance as yf


class StockData:
    def __init__(self, tickers, start_date, end_date):
        if not isinstance(tickers, list) or len(tickers) < 2:
            raise ValueError(
                "Error: Please provide 2 or more ticker symbols for analysis."
            )

        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.opening_price = None
        self.closing_price = None
        self.volume = None
        self.low = None
        self.high = None

    def fetch_data(self):
        try:
            data = yf.download(
                self.tickers, start=self.start_date, end=self.end_date, group_by='ticker')
            if data.empty:
                raise ValueError(f'No data found for {self.tickers}.')
            self.data = data
            self._process_data()
        except Exception as e:
            print(f'Error fetching data for {self.tickers}: {e}')
            return None

    def _process_data(self):
        self.opening_price = pd.DataFrame()
        self.closing_price = pd.DataFrame()
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
        self.opening_price = self.opening_price.resample(resample_rule).first()
        self.closing_price = self.closing_price.resample(resample_rule).last()
        self.volume = self.volume.resample(resample_rule).sum()
        self.low = self.low.resample(resample_rule).min()
        self.high = self.high.resample(resample_rule).max()

    def get_prices(self):
        return (self.opening_price.round(3),
                self.closing_price.round(3),
                self.volume.round(3),
                self.low.round(3),
                self.high.round(3))
