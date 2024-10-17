# stock_indicator.py
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
        loss = -self.price_data.where(delta < 0,
                                      0).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
