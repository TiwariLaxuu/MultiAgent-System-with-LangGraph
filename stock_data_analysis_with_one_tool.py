from typing import Annotated
import pandas as pd
import yfinance as yf
from langchain_core.tools import tool

@tool
def stock_data_tool(
    company_ticker: Annotated[str, "The ticker symbol of the company to retrieve their stock performance data."], 
    num_days: Annotated[int, "The number of days of stock data required to respond to the user query."]
) -> str:
    """
    Use this to look-up stock performance data for companies via Yahoo Finance. 
    You may need to convert company names into ticker symbols to call this function, 
    e.g, Apple Inc. -> AAPL, and you may need to convert weeks, months, and years, into days.
    """
    try:
        # Fetch data from Yahoo Finance using the yfinance library
        # We use a buffer period (e.g., num_days * 2) to ensure we get enough trading days
        period = f"{num_days}d" if num_days <= 30 else "1mo"
        
        # Alternatively, fetch by specific history period or calculate start/end dates
        ticker_obj = yf.Ticker(company_ticker)
        
        # 'period' handles formatting like '5d', '1mo', '1y'
        # Since we want exactly 'num_days' of calendar history, we can fetch slightly more and slice
        stock_df = ticker_obj.history(period=f"{num_days + 10}d")
        
        if stock_df.empty:
            return f"Sorry, but data for ticker '{company_ticker}' could not be retrieved from Yahoo Finance."
        
        # Format the index to date only
        stock_df.index = stock_df.index.date
        
        # Get the most recent date in the DataFrame
        final_date = stock_df.index.max()

        # Filter the DataFrame to get the last num_days of stock data based on calendar days
        filtered_df = stock_df[stock_df.index > (final_date - pd.Timedelta(days=num_days))]
        
        # Optional: Clean up columns for a cleaner markdown table
        filtered_df = filtered_df[['Open', 'High', 'Low', 'Close', 'Volume']]

        return f"Successfully executed the stock performance data retrieval tool from Yahoo Finance to retrieve data within the last *{num_days} days* for company **{company_ticker}**:\n\n{filtered_df.to_markdown()}"

    except Exception as e:
        return f"An error occurred while fetching data from Yahoo Finance: {str(e)}"

# Invoke the tool for META
retrieved_data = stock_data_tool.invoke({"company_ticker": "META", "num_days": 4})
print(retrieved_data)