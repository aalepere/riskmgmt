""" Computes historical VaR """
import numpy as np
import pandas as pd
import yfinance as yf

if __name__ == "__main__":
    tickerSymbolList = ["MSFT", "AAPL", "GOOGL", "TSLA"]
    portfolio_df = pd.DataFrame()
    for tickerSymbol in tickerSymbolList:
        tickerData = yf.Ticker(tickerSymbol).history(
            period="1d", start="2020-1-1", end="2020-12-31"
        )[["Close"]]
        tickerData["logReturn"] = np.log(tickerData["Close"]) - np.log(
            tickerData["Close"].shift(1)
        )
        tickerData["InitialValue"] = float(tickerData["Close"].iloc[[-1]]) * 100
        tickerData["NewValue"] = tickerData["InitialValue"] * np.exp(
            tickerData["logReturn"]
        )
        tickerData.columns = [
            f"Close_{tickerSymbol}",
            f"logReturn_{tickerSymbol}",
            f"InitialValue_{tickerSymbol}",
            f"NewValue_{tickerSymbol}",
        ]
        portfolio_df = pd.merge(
            tickerData, portfolio_df, how="left", right_index=True, left_index=True
        )
    portfolio_df["InitialPortfolio"] = 0
    portfolio_df["NewPortfolio"] = 0
    for tickerSymbol in tickerSymbolList:
        portfolio_df["InitialPortfolio"] = (
            portfolio_df["InitialPortfolio"]
            + portfolio_df[f"InitialValue_{tickerSymbol}"]
        )
        portfolio_df["NewPortfolio"] = (
            portfolio_df["NewPortfolio"] + portfolio_df[f"NewValue_{tickerSymbol}"]
        )
    portfolio_df["P&L"] = (
        portfolio_df["NewPortfolio"] - portfolio_df["InitialPortfolio"]
    )
    print(portfolio_df["P&L"].quantile(0.01))
