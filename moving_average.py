import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

# we use parse_dates and index_col so date is an index (and it's column 0)
df  = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
# min_periods so .head() does not present NaN bc there were no 100 previous days.
df['100 M.A.'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
print(df.head())

ax1 = plt.subplot2grid((8,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((8,1), (6,0), rowspan=2, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100 M.A.'])
ax2.bar(df.index, df['Volume'])

plt.show()
