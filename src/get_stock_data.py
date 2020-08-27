import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

stock_ticker = 'TSLA'

'''
Gets stock data from Yahoo and saves as a csv
'''

style.use('ggplot')

# keep in mind that your stock might not have been traded in the entire period
start = dt.datetime(2010, 1, 1)
end = dt.datetime(2020,12,31)

df = web.DataReader(stock_ticker, 'yahoo', start, end)
df.to_csv(f'../csv/{stock_ticker}.csv')

# we use parse_dates and index_col so date is an index (and it's column 0)
df  = pd.read_csv(f'../csv/{stock_ticker}.csv', parse_dates=True, index_col=0)
# print(df.head())

fig, ax = plt.subplots()
ax.set_ylabel('US Dollars')

title = f'(NASDAQ: {stock_ticker}) Stock price'
df['Adj Close'].plot(title=title, ax=ax)
plt.show()
