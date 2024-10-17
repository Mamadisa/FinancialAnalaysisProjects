# key_metrics.py
import numpy as np
import pandas as pd
import random


class KeyMetrics:
    def __init__(self, price_data):
        self.price_data = price_data

    def scaling(self):
        scaled_prices = self.price_data.copy()
        for ticker in scaled_prices.columns:
            scaled_prices[ticker] = (scaled_prices[ticker] /
                                     scaled_prices[ticker].iloc[0])

        return scaled_prices

    def portfolio_weights(self, number_ofAssets):
        weights = np.array([random.random() for _ in range(number_ofAssets)])
        # can write it like: weights/= np.sum(weights)
        weights = weights / np.sum(weights)
        weights = np.round(weights, 2)
        weights[-1] = 1 - np.sum(weights[:-1])

        return weights

    def asset_allocation(self, portfolio_weights, investment_amount):
        scaled_prices = self.scaling()
        allocation = pd.DataFrame(
            index=scaled_prices.index, columns=scaled_prices.columns)

        for i, ticker in enumerate(scaled_prices.columns):
            allocation[ticker] = scaled_prices[ticker] * \
                portfolio_weights[i] * investment_amount

        allocation['Portfolio Value'] = allocation.sum(axis=1)
        allocation['Portfolio Daily Return'] = allocation['Portfolio Value'].pct_change(
            1) * 100
        allocation['Portfolio Daily Return'] = allocation['Portfolio Daily Return'].fillna(
            0)

        return allocation

    def simulation_engine(self, portfolio_weights, starting_investment):
        risk_freeRate = 0.08
        portfolio = self.asset_allocation(
            portfolio_weights, starting_investment)

        # ROI=(Last - First)/First
        return_OnInvestment = ((portfolio.iloc[-1]['Portfolio Value'] - portfolio.iloc[0]['Portfolio Value']) /
                               portfolio.iloc[0]['Portfolio Value']) * 100

        portfolio_dailyReturn = portfolio.drop(
            columns=['Portfolio Value', 'Portfolio Daily Return']).pct_change(1)
        portfolio_dailyReturn.fillna(0)

        expected_portfolio_return = np.sum(
            portfolio_weights * portfolio_dailyReturn.mean()) * 252

        # Portfolio Volatility Formula
        covariance = portfolio_dailyReturn.cov()
        expected_volatility = np.sqrt(np.dot(portfolio_weights.T, np.dot(
            covariance, portfolio_weights)))

        sharpe_ratio = (expected_portfolio_return -
                        risk_freeRate) / expected_volatility

        return (expected_portfolio_return, expected_volatility,
                sharpe_ratio, portfolio[-1:]['Portfolio Value'].values[0], return_OnInvestment)
