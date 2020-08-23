import mplfinance as mpf
import pandas as pd


df= pd.read_csv('./csv/TSLA.csv',parse_dates=True, index_col=0)
print(df.head())
mpf.plot(df,
        type='candle', # graph type (like bars, candlestick...)
        style='charles', # graph color ('chales' is green for pos, red for neg)
        title='NASDAQ: TSLA',
        ylabel='Price (US Dollars)',
        figratio=(25,10), # figure proportions. (25, 10) means x is 2.5 times y.
        mav=100, # (x-day) moving average
        ylabel_lower='Volume in millions',
        volume=True
        )
