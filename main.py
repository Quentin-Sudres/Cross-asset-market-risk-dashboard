#==============================================
# IMPORT LIBRARIES
#==============================================

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#==============================================
# DOWNLOAD MARKET DATA
#==============================================

start_date="2020-01-01"
end_date="2026-05-22"
sp500=yf.download("^GSPC",start=start_date,end=end_date)
gold=yf.download("GC=F",start=start_date,end=end_date)
oil=yf.download("USO",start=start_date,end=end_date)

print(sp500)
print(gold)
print(oil)

sp500_close=sp500["Close"].squeeze()
print(sp500_close)
gold_close=gold["Close"].squeeze()
print(gold_close)
oil_close=oil["Close"].squeeze()
print(oil_close)

market_data=pd.DataFrame({"SP500":sp500_close,
                          "Gold":gold_close,
                          "Oil":oil_close})
market_data=market_data.dropna()
print(market_data)

#==============================================
# RETURNS CALCULATION
#==============================================

returns=market_data.pct_change()
returns=returns.dropna()
print(returns)

#==============================================
# RISK METRICS
#==============================================

volatility=returns.std()
print(volatility)

var_95=returns.quantile(0.05)
print(var_95)

expected_shortfall=returns[returns<=var_95].mean()
print(expected_shortfall)

rolling_volatility=returns.rolling(window=30).std()
print(rolling_volatility)

cumulative_returns=(1+returns).cumprod()
rolling_max=cumulative_returns.cummax()
drawdown=(cumulative_returns-rolling_max)/rolling_max
max_drawdown=drawdown.min()
print(max_drawdown)

#==============================================
# PORTFOLIO ANALYTICS
#==============================================

weights=np.array([0.5,0.3,0.2])
portfolio_returns=returns.dot(weights)
print(portfolio_returns)

portfolio_volatility=portfolio_returns.std()
print(portfolio_volatility)

portfolio_var_95=portfolio_returns.quantile(0.05)
print(portfolio_var_95)

portfolio_es_95=portfolio_returns[portfolio_returns<=portfolio_var_95].mean()
print(portfolio_es_95)

portfolio_mean_return=portfolio_returns.mean()
sharpe_ratio=portfolio_mean_return/portfolio_volatility
print(sharpe_ratio)

portfolio_cumulative=(1+portfolio_returns).cumprod()
portfolio_drawdown=(portfolio_cumulative/portfolio_cumulative.cummax())-1

#==============================================
# VISUALIZATION
#==============================================

market_data.plot(figsize=(12,6))
plt.title("Price evolution: SP500, Gold and Oil")
plt.xlabel("Date")
plt.ylabel("Price level")
plt.grid(True)
plt.show()

normalized_data=market_data/market_data.iloc[0]*100
normalized_data.plot(figsize=(12,6))
plt.title("Normalized performance")
plt.xlabel("Date")
plt.ylabel("Base 100")
plt.grid(True)
plt.show()

rolling_volatility.plot(figsize=(12,6))
plt.title("30-Day Rolling Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.grid(True)
plt.show()

drawdown.plot(figsize=(12,6))
plt.title("Drawdown Analysis")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.grid(True)
plt.show()

correlation_matrix=returns.corr()
print(correlation_matrix)
plt.figure(figsize=(8,6))
plt.imshow(correlation_matrix,cmap="coolwarm")
plt.colorbar()
plt.xticks(range(len(correlation_matrix.columns)),correlation_matrix.columns)
plt.yticks(range(len(correlation_matrix.columns)),correlation_matrix.columns)
plt.title("Correlation Heatmap")
plt.show()

portfolio_cumulative.plot(figsize=(12,6))
plt.title("Portfolio Cumulative Performance")
plt.xlabel("Date")
plt.ylabel("Portfolio Value")
plt.grid(True)
plt.show()

#==============================================
# RISK SUMMARY
#==============================================

risk_summary=pd.DataFrame({"Volatility":volatility,
                           "VaR_95":var_95,
                           "Expected_Shortfall_95":expected_shortfall})
print(risk_summary)

#==============================================
# EXCEL EXPORT
#==============================================

risk_summary.to_excel("risk_summary.xlsx")
print("Excel file created")
market_data.to_excel("market_data.xlsx")
returns.to_excel("returns.xlsx")
print("Market data ans returns exported")

with pd.ExcelWriter("cross_asset_market_risk_data.xlsx") as writer:
    market_data.to_excel(writer,sheet_name="Prices")
    returns.to_excel(writer,sheet_name="Returns")
    risk_summary.to_excel(writer,sheet_name="Risk Summary")
    correlation_matrix.to_excel(writer,sheet_name="Correlations")
    rolling_volatility.to_excel(writer,sheet_name="Rolling_Volatility")
    drawdown.to_excel(writer,sheet_name="Drawdown")
    portfolio_returns.to_excel(writer,sheet_name="Portfolio_Returns")
    portfolio_cumulative.to_excel(writer,sheet_name="Portfolio_Cumulative")
    portfolio_drawdown.to_excel(writer,sheet_name="Portfolio_Drawdown")
    portfolio_summary=pd.DataFrame({"Metric":["Portfolio Volatility","Portfolio VaR 95","Portfolio ES 95","Sharpe Ratio"],
                                    "Value":[portfolio_volatility,portfolio_var_95,portfolio_es_95,sharpe_ratio]})
    portfolio_summary.to_excel(writer,sheet_name="Portfolio_Metrics",index=False)
print("Final Excel workbook created")