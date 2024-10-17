import pandas as pd
import numpy as np
from key_metrics import KeyMetrics

# Set up a simple DataFrame with dummy price data
data = {
    'AAPL': [150, 152, 148, 155],
    'MSFT': [300, 305, 310, 315]
}
price_data = pd.DataFrame(data, index=pd.date_range('2023-10-01', periods=4))
metrics = KeyMetrics(price_data)

# Test scaling function
scaled_prices = metrics.scaling()
print("Scaled Prices:\n", scaled_prices)

# Test portfolio weights
weights = metrics.portfolio_weights(2)
print("\nPortfolio Weights:", weights)

# Test asset allocation
investment = 10000
allocation = metrics.asset_allocation(weights, investment)
print("\nAsset Allocation:\n", allocation)


# Calculate covariance matrix of daily returns
daily_returns = price_data.pct_change().dropna()
covariance_matrix = round(daily_returns.cov(), 3)
print("\nCovariance Matrix:\n", covariance_matrix)
expected_volatility = np.sqrt(np.dot(weights.T, np.dot(
    covariance_matrix, weights)))
print("\nVolatility:\n", expected_volatility)

# Volatility and Sharpe Ratio
risk_freeRate = 0.08
expected_portfolio_return = np.sum(
    weights * daily_returns.mean()) * 252
print("\nPortfolio Return:\n", expected_portfolio_return)
sharpe_ratio = (expected_portfolio_return -
                risk_freeRate) / expected_volatility
print("\nSharpe Ratio:\n", sharpe_ratio)
print('\n')
