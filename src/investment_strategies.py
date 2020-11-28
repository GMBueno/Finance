import pandas as pd
import pandas_datareader.data as web
import numpy as np
from pprint import pprint as pp
import pickle

'''
Compare the following investment strategies, showing which had the highest
profitability, lowest risk & highest Sharpe ratio for the Bovespa index history.

i. invest R$X once and withdraw everything ten years later, also once;

ii. invest R$X a.m. for A years and withdraw the entire amount once, at the end;
    invest monthly (100/24) for 2 years, withdraw everything once...

iii. invest R$X a.m. for A years and withdraw the amount gradually over B years;
    invest monthly (100/24) for 2 years, withdraw monthly (100x/24) over 2 years...

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

def get_first_close_of_year(year):
    date = f'{year}-01-01'
    date = get_next_valid_day(date)
    return closes[date]

def get_first_close_of_month(year, month):
    date = make_date(year, month, 1)
    date = get_next_valid_day(date, try_current=True)
    return closes[date]

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

def get_risk(date1, date2):
    prices = []
    d1 = get_next_valid_day(date1, try_current=True)
    d2 = get_next_valid_day(d1)
    while is_before(d2, date2):
        prices.append((closes[d2]/closes[d1])-1)
        d1 = d2
        d2 = get_next_valid_day(d1)
    risk = 100 * np.array(prices).std()
    return risk

def save_rets_and_risks():
    risk_ret = {}
    rets = []
    risks = []
    start_year = 1995
    for year in range(start_year,2011):
        start_date = f'{year}-01-01'
        end_date = f'{year+10}-01-01'
        risk = get_risk(start_date, end_date)
        ret = get_return(start_date, end_date)
        rets.append(ret)
        risks.append(risk)

    with open('pickle/rets.pickle', 'wb') as f:
        pickle.dump(rets, f)
    with open('pickle/risks.pickle', 'wb') as f:
        pickle.dump(risks, f)

def load_returns():
    with open('pickle/rets.pickle', 'rb') as f:
        rets = pickle.load(f)
    with open('pickle/risks.pickle', 'rb') as f:
        risks = pickle.load(f)

    start_year = 1995
    for i in range(0, len(rets)):
        print(f'Years {start_year+i}-{start_year+10+i}')
        print(f'Bovespa {start_year+i}: {get_first_close_of_year(start_year+i):.0f}')
        print(f'Bovespa {start_year+10+i}: {get_first_close_of_year(start_year+10+i):.0f}')
        print(f'return: {rets[i]:.2f}%')
        print(f'risk: {risks[i]:.2f}%\n')

    sum_rets = 0
    for ret in rets:
        sum_rets = sum_rets + ret
    avg_ret = sum_rets/len(rets)

    sum_risks = 0
    for risk in risks:
        sum_risks = sum_risks + risk
    avg_risk = sum_risks/len(risks)

    print(f'avg 10-year return: {avg_ret:.2f}%')
    print(f'avg 10-year risk: {avg_risk:.2f}%')

def simulate_buyonce_hold10y_sellonce():
    pct_rets = []
    annual_pct_rets = []
    hold_period = 10
    for start_year in range(1995, 2010):
        for month in range(1, 13):
            '''get overall percentage return on investment'''
            pct_ret = buyonce_hold10y_sellonce(year=start_year, month=month)
            pct_rets.append(pct_ret)

            '''get annual pct_return on investment'''
            annual_pct_rets.append(get_annual_pct_return(pct_ret, hold_period))

    sum = 0
    for annual_pct_ret in annual_pct_rets:
        sum += annual_pct_ret
    avg = sum/float(len(annual_pct_rets))
    return avg



def buyonce_hold10y_sellonce(*, year, month=1, hold_period=10):
    '''
    tests the following strategy:
    invest R$100 once and withdraw everything ten years later, also once;
    '''
    close1 = get_first_close_of_month(year, month)
    close2 = get_first_close_of_month(year+hold_period, month)
    multiplier = close2/close1
    pct_ret = 100*(multiplier-1)
    return pct_ret

def get_annual_pct_return(pct_ret, years):
    multiplier = pct_ret/100.0 + 1
    annual_multiplier = multiplier**(1/float(years))
    annual_ret = 100*(annual_multiplier-1)
    return annual_ret
