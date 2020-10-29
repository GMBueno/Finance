import pandas as pd
import pandas_datareader.data as web
import numpy as np

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

def get_return(date1, date2):
    wallet = 100
    date1 = get_next_valid_day(date1, try_current=True)
    date2 = get_next_valid_day(date2, try_current=True)
    initial_price = closes[date1]
    final_price = closes[date2]
    appreciation = 100 * ((final_price/initial_price)-1)
    return appreciation

def avg_return():
    riscs = []
    risc = get_risc('1995-01-01', '2005-01-01')

    appr = get_return('1995-01-01', '2005-01-01')

    print(f'--> Risc: {risc*100:.2f}%')
    print(f'--> Return: {appr:.2f}%')


def get_next_valid_day(date, try_current=False):
    '''
    receives a date in this format: '1996-01-01' and output the next valid day,
    that is, a day that the stock exchange was opened and there is data.
    '''
    next = 1
    if try_current==True:
        next = 0
    date = date.split('-')
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    for yy in range(year,2021):
        for mm in range(month, 13):
            for dd in range(day+next,32):
                date = make_date(yy, mm, dd)
                # print('trying: ', date)
                try:
                    price = closes[date]
                    return date
                except:
                    continue
            next = 0  # next iteration we have to try day 1.
            day = 1  # next iteration starts at day 1
        month = 1  # next iteration starts at month 1
    return 'THERE IS NO NEXT VALID DAY'

def make_date(year, month, day):
    '''
    very simple function that adds '0' to days and months if <=9, then
    concatenates year-month-day to create a date.
    '''
    if month <= 9:
        month = '0' + str(month)
    if day <= 9:
        day = '0' + str(day)
    date = f'{year}-{month}-{day}'
    return date

def is_before(date1, date2):
    date1 = date1.split('-')
    year1 = int(date1[0])
    month1 = int(date1[1])
    day1 = int(date1[2])

    date2 = date2.split('-')
    year2 = int(date2[0])
    month2 = int(date2[1])
    day2 = int(date2[2])

    if year1 != year2:
        if year1 < year2:
            return True
        return False
    if month1 != month2:
        if month1 < month2:
            return True
        return False
    if day1 < day2:
        return True
    return False

# print_calc_i()
# calc_sharpe()

def get_risc(date1, date2):
    prices = []
    d1 = get_next_valid_day(date1, try_current=True)
    d2 = get_next_valid_day(d1)
    while is_before(d2, date2):
        prices.append((closes[d2]/closes[d1])-1)
        d1 = d2
        d2 = get_next_valid_day(d1)
    risc = np.array(prices).std()
    return risc

date1 = '1995-01-01'
date2 = '2005-01-01'
risc = get_risc(date1, date2)
appr = get_return(date1, date2)
print(f'From {date1} to {date2}')
print(f'--> Risc: {risc*100:.2f}%')
print(f'--> Return: {appr:.2f}%')
