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

'''
1995 0
1996 246
1997 494
1998 743
1999 990
2000 1236
2001 1484
2002 1731
2003 1978
2004 2228
2005 2477
2006 2726
2007 2972
2008 3217
2009 3466
2010 3712
2011 3959
2012 4208
2013 4452
2014 4700
2015 4948
2016 5196
2017 5443
2018 5690
2019 5934
2020 6181
1995-2005 0-2476
1996-2006 246-2725
1997-2007 494-2971
1998-2008 743-3216
1999-2009 990-3465
2000-2010 1236-3711
2001-2011 1484-3958
2002-2012 1731-4207
2003-2013 1978-4451
2004-2014 2228-4699
2005-2015 2477-4947
2006-2016 2726-5197
2007-2017 2972-5442
2008-2018 3217-5689
2009-2019 3466-5933
2010-2020 3712-6181
'''

def calc_i():
    wallet = 100
    day = '1'
    wallets = []
    for year in range(1995, 2011):
        initial_year = str(year)
        final_year = str(year + 10)
        initial_price = find_first_price_of_year(initial_year)
        final_price = find_first_price_of_year(final_year)
        appreciation = final_price/initial_price
        wallet = wallet*appreciation
        wallets.append([initial_year, final_year, appreciation])
    return wallets

def print_calc_i():
    wallets = calc_i()
    avg_appreciation = 0
    for wallet in wallets:
        initial_year = wallet[0]
        final_year = wallet[1]
        appreciation = wallet[2]
        print(f'From {initial_year} to {final_year}: {appreciation*100:.2f}%')
        avg_appreciation += appreciation
    print(f'Average appreciation: {(avg_appreciation/len(wallets))*100:.2f}%')

def find_first_price_of_year(year):
    for day in range(1,9):
        try:
            price = closes[f'{year}-01-0{day}']
            # print(f'found {year}-01-0{day}')
            return price
        except:
            continue

def calc_sharpe():
    # wallet = calc_i()[0]
    test = np.array([1, 2, 3])
    print(f'Risco: {test.std()}')

# def calc_ii():
#     for i, date, close in enumerate(closes):
#         if i%30 == 0:
#             invest


def get_next_valid_day(date):
    '''
    receives a date in this format: '1996-01-01' and output the next valid day,
    that is, a day that the stock exchange was opened and there is data.
    '''
    date = date.split('-')
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    for year in range(year,2021):
        for month in range(month, 13):
            for day in range(day+1,32):
                date = make_date(year, month, day)
                try:
                    price = closes[date]
                    return date
                except:
                    continue
            day = 1
        month = 1
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

def get_risc():
    riscs = []
    prices = []
    for i in range(0, 2476):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(246, 2725):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(494, 2971):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(743, 3216):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(990, 3465):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(1236, 3711):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(1484, 3958):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(1731, 4207):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(1978, 4451):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(2228, 4699):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(2477, 4947):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(2726, 5197):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(2972, 5442):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(3217, 5689):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(3466, 5933):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    prices = []
    for i in range(3712, 6181):
        prices.append((closes[i+1]/closes[i])-1)
    riscs.append(np.array(prices).std())
    return riscs

# year = 1995
# wallets = calc_i()
# for i, risc in enumerate(get_risc()):
#     print(f'Years {year}-{year+10}')
#     print(f'--> Risc: {risc*100:.2f}%')
#     print(f'--> Return {wallets[i][2]*100:.2f}%\n')
#     year = year +1
