import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

'''
Compare the following investment strategies, showing which had the highest
profitability, lowest risk & highest Sharpe ratio for the Bovespa index history.
i. invest R$X once and remove everything ten years later, also once;
ii. invest R$X a.m. for A years and withdraw the entire amount once, at the end;
iii. invest R$X a.m. for A years and withdraw the amount gradually over B years;
iv. Test the above strategies for some values, such as R$100.00 per month, in
    10, 15, 20 and 25 years, and withdrawing for 5 years.
'''

# we use parse_dates and index_col so date is an index (and it's column 0)
df  = pd.read_csv('./csv/^BVSP.csv', parse_dates=True, index_col=0)
closes = df['Adj Close']
# print(closes.head())
# close = closes['2020-06-03']
# print(close)


def calc_i():
    wallet = 100
    day = '1'
    for year in range(1995, 2011):
        initial_year = str(year)
        final_year = str(year + 10)
        initial_price = find_first_price_of_year(initial_year)
        final_price = find_first_price_of_year(final_year)
        appreciation = final_price/initial_price
        wallet = wallet*appreciation
        print(f'From {initial_year} to {final_year}: {appreciation*100:.2f}%')

def find_first_price_of_year(year):
    for day in range(1,9):
        try:
            price = closes[f'{year}-01-0{day}']
            # print(f'found {year}-01-0{day}')
            return price
        except:
            continue

# def calc_ii():
#     for i, date, close in enumerate(closes):
#         if i%30 == 0:
#             invest


# def buy(date, amount):
#
#
# def sell(date, amount):

calc_i()
