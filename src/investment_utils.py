import pandas as pd
import pandas_datareader.data as web
import numpy as np
from pprint import pprint as pp
import pickle

class InvestUtils:
    def __init__(self, stock_ticker):
        # we use parse_dates and index_col so date is an index (and it's column 0)
        self.df = pd.read_csv(f'./csv/{stock_ticker}.csv', parse_dates=True, index_col=0)
        self.closes = self.df['Adj Close']
        # print(closes.head())
        # close = closes['2020-06-03']
        # print(close)

    def get_return(self, date1, date2):
        date1 = self.get_next_valid_day(date1, try_current=True)
        date2 = self.get_next_valid_day(date2, try_current=True)
        initial_price = self.closes[date1]
        final_price = self.closes[date2]
        appreciation = 100 * ((final_price/initial_price)-1)
        return appreciation

    def get_first_close_of_year(self, year):
        date = f'{year}-01-01'
        date = self.get_next_valid_day(date)
        return self.closes[date]

    def get_first_close_of_month(self, year, month):
        date = self.make_date(year, month, 1)
        date = self.get_next_valid_day(date, try_current=True)
        return self.closes[date]

    def get_next_valid_day(self, date, try_current=False):
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
                    date = self.make_date(yy, mm, dd)
                    # print('trying: ', date)
                    try:
                        # if able to get the close, can return the date, because there is data for that day
                        self.closes[date]
                        return date
                    except:
                        continue
                next = 0  # next iteration we have to try day 1.
                day = 1  # next iteration starts at day 1
            month = 1  # next iteration starts at month 1
        return 'THERE IS NO NEXT VALID DAY'

    def make_date(self, year, month, day):
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

    def is_before(self, date1, date2):
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

    def get_risk(self, date1, date2):
        prices = []
        d1 = self.get_next_valid_day(date1, try_current=True)
        d2 = self.get_next_valid_day(d1)
        while self.is_before(d2, date2):
            prices.append((self.closes[d2]/self.closes[d1])-1)
            d1 = d2
            d2 = self.get_next_valid_day(d1)
        risk = 100 * np.array(prices).std()
        return risk

    def get_monthly_risk(self, *, start_y, month, end_year, invest_period=0):
        start_date = self.make_date(start_y, month, 1)
        start_date = self.get_next_valid_day(start_date, try_current=True)
        next_date = self.make_date(start_y, month, 1)

        hold_period = 10
        end_date = self.make_date(start_y+hold_period+invest_period, month, 1)
        start_date = self.get_next_valid_day(start_date, try_current=False)
        
        prices = []
        next_month = month
        curr_year = start_y
        curr_date = start_date

        while self.is_before(next_date, end_date):
            next_month += 1
            if next_month > 12:
                next_month = 1
                curr_year += 1

            next_date = self.make_date(curr_year, next_month, 1)
            next_date = self.get_next_valid_day(next_date, try_current=True)
            prices.append((self.closes[curr_date]/self.closes[next_date])-1)
            curr_date = next_date
        risk = 100 * np.array(prices).std()
        return risk  

    def save_rets_and_risks(self):
        rets = []
        risks = []
        start_year = 1995
        for year in range(start_year,2011):
            start_date = f'{year}-01-01'
            end_date = f'{year+10}-01-01'
            risk = self.get_risk(start_date, end_date)
            ret = self.get_return(start_date, end_date)
            rets.append(ret)
            risks.append(risk)

        with open('pickle/rets.pickle', 'wb') as f:
            pickle.dump(rets, f)
        with open('pickle/risks.pickle', 'wb') as f:
            pickle.dump(risks, f)

    def load_returns(self):
        with open('pickle/rets.pickle', 'rb') as f:
            rets = pickle.load(f)
        with open('pickle/risks.pickle', 'rb') as f:
            risks = pickle.load(f)

        start_year = 1995
        for i in range(0, len(rets)):
            print(f'Years {start_year+i}-{start_year+10+i}')
            print(f'Bovespa {start_year+i}: {self.get_first_close_of_year(start_year+i):.0f}')
            print(f'Bovespa {start_year+10+i}: {self.get_first_close_of_year(start_year+10+i):.0f}')
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

    def get_annual_pct_return(self, *, pct_ret, years):
        multiplier = pct_ret/100.0 + 1
        annual_multiplier = multiplier**(1/float(years))
        annual_ret = 100*(annual_multiplier-1)
        return annual_ret
