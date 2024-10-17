# main.py
from stock_data import StockData
from key_metrics import KeyMetrics
from stock_plotter import StockPlotter

import numpy as np
import datetime as dt


def main():
    print('\nWelcome to the Portfolio Analysis Tool.')
    print('Note: This model does not differentiate between different currencies.')
    print('For the best experience, use stocks trading with the same currency.')
    print('Example input: AMZN,AAPL,GOOG,META\n')

    tickers = input(
        'Please input Ticker Symbols. Please separate using commas( , ): ').split(',')

    try:
        print("Please enter a wide enough date range (e.g., at least 7-10 trading days) for better visualization.")
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Error: Incorrect date format")
        return

    try:
        initial_investment = float(
            input('Please input the amount you would like to invest: '))
    except ValueError:
        print("Error: Invalid input.")
        return

    stock_data = StockData(tickers, start_date, end_date)
    stock_data.fetch_data()
    opening_price, closing_price, volume, low, high = stock_data.get_prices()

    plot_type = input(
        "Choose plot type: 'line', 'bar', or 'candlestick': ").lower()
    if plot_type not in ['line', 'bar', 'candlestick']:
        print("Error: Invalid plot type. Please choose 'line', 'bar', or 'candlestick'.")
        return

    stock_plotter = StockPlotter(tickers, stock_data)
    stock_plotter.plot(plot_type)

    simulation_runs = int(
        input('Enter the number of simulations to run (e.g., 1000): '))
    run_simulation(tickers, closing_price, initial_investment, simulation_runs)


def run_simulation(tickers, closing_price, initial_investment, simulation_runs):

    key_metrics = KeyMetrics(closing_price)
    n = len(tickers)
    weight_runs = np.zeros((simulation_runs, n))
    expected_returns = np.zeros(simulation_runs)
    volatility_runs = np.zeros(simulation_runs)
    sharpe_ratios = np.zeros(simulation_runs)
    final_values = np.zeros(simulation_runs)
    roi_runs = np.zeros(simulation_runs)

    for i in range(simulation_runs):
        weights = key_metrics.portfolio_weights(n)
        weight_runs[i, :] = weights

        (expected_returns[i], volatility_runs[i], sharpe_ratios[i],
         final_values[i], roi_runs[i]) = key_metrics.simulation_engine(weights, initial_investment)

    # Display Results for Portfolio that has the Highest Expected Return:
    optimal_weight = weight_runs[sharpe_ratios.argmax(), :]

    (optimal_portfolio_return, optimal_volatility, optimal_sharpe_ratio,
     highest_final_value, optimal_return_on_investment) = key_metrics.simulation_engine(optimal_weight, initial_investment)

    print(f'The best Portfolio Metrics based on {
          simulation_runs} Monte Carlo Simulation Runs:')
    print(f'  -Optimal Portfolio Weights: {optimal_weight}')
    print(
        f'  -Portfolio Annual Return is {optimal_portfolio_return * 100:.2f}%')
    print(f'  -Portfolio Volatility is {optimal_volatility * 100:.2f}%')
    print(f'  -Sharpe Ratio is {optimal_sharpe_ratio:.2f}')
    print(f'  -Final Value is ${highest_final_value:.2f}')
    print(
        f'  -The Return on Investment is {optimal_return_on_investment:.2f}%')


if __name__ == "__main__":
    main()
