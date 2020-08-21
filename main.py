import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')
start = dt.datetime(2010, 1, 1)
end = dt.datetime(2020,12,31)

df = web.DataReader('TSLA', 'yahoo', start, end)
df.to_csv('tsla.csv')

# we use parse_dates and index_col so date is an index (and it's column 0)
df  = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
# print(df.head())

fig, ax = plt.subplots()
ax.set_ylabel('US Dollars')

title = 'Tesla (NASDAQ: TSLA) Stock price'
df['Adj Close'].plot(title=title, ax=ax)
plt.show()
