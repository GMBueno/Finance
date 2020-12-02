from investment_utils import InvestUtils
import numpy as np


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

class InvestmentStrategies:
    def __init__(self, stock_ticker):
        self.inv_utils = InvestUtils(stock_ticker)

    def simulate_buyonce_hold10y_sellonce(self, start_y, end_y):
        pct_rets = []
        hold_period = 10
        risks = []
        for start_year in range(start_y, end_y):
            for month in range(1, 13):
                '''get overall percentage return on investment'''
                pct_ret = self.buyonce_hold10y_sellonce(start_year=start_year, month=month)
                pct_rets.append(pct_ret)

                ''' now lets calculate risk
                    first getting valid start and end dates
                '''
                end_year = start_year+hold_period
                risk = self.inv_utils.get_monthly_risk(start_y=start_year, start_month=month, end_year=end_year, end_month=month)
                risks.append(risk)

        ''' calculate average annual return of multiple wallets '''
        avg_pct_ret = sum(pct_rets)/len(pct_rets)
        avg_annual_pct_ret = self.inv_utils.get_annual_pct_return(pct_ret=avg_pct_ret, years=hold_period)

        ''' now let's calculate avg risk'''
        avg_risk = sum(risks)/float(len(risks))   

        response = {
            'avg_annual_pct_ret': avg_annual_pct_ret,
            'avg_risk': avg_risk
        }
        return response


    def buyonce_hold10y_sellonce(self, *, start_year, month=1, hold_period=10):
        '''
        tests the following strategy:
        invest R$100 once and withdraw everything ten years later, also once;
        '''
        close1 = self.inv_utils.get_first_close_of_month(start_year, month)
        close2 = self.inv_utils.get_first_close_of_month(start_year+hold_period, month)
        multiplier = close2/close1
        pct_ret = 100*(multiplier-1)
        return pct_ret


    def simulate_buy24mo_hold10y_sellonce(self, start_y, end_y):
        pct_rets = []
        hold_period = 10
        risks = []
        invest_period = 2
        for start_year in range(start_y, end_y):
            for month in range(1, 13):
                '''get overall percentage return on investment'''
                pct_ret = self.buy24mo_hold10y_sell(start_year=start_year, month=month, sell_once=True)
                '''append pct return to list of pct returns to calc avg later'''
                pct_rets.append(pct_ret)

                ''' now lets calculate risk
                    first getting valid start and end dates
                '''
                end_year = start_year+hold_period+invest_period
                risk = self.inv_utils.get_monthly_risk(start_y=start_year, start_month=month, end_year=end_year, end_month=month)
                risks.append(risk)

        ''' calculate average annual return of multiple wallets '''
        avg_pct_ret = sum(pct_rets)/len(pct_rets)
        avg_annual_pct_ret = self.inv_utils.get_annual_pct_return(pct_ret=avg_pct_ret, years=hold_period)

        ''' now let's calculate avg risk'''
        avg_risk = sum(risks)/float(len(risks))   

        response = {
            'avg_annual_pct_ret': avg_annual_pct_ret,
            'avg_risk': avg_risk
        }
        return response


    def simulate_buy24mo_hold10y_sell24mo(self, start_y, end_y):
        pct_rets = []
        hold_period = 10
        risks = []
        invest_period = 2
        sell_period = 2 
        for start_year in range(start_y, end_y):
            for month in range(1, 13):
                '''get overall percentage return on investment'''
                pct_ret = self.buy24mo_hold10y_sell(start_year=start_year, month=month, sell_once=False)
                '''append pct return to list of pct returns to calc avg later'''
                pct_rets.append(pct_ret)

                ''' now lets calculate risk
                    first getting valid start and end dates
                '''
                end_year = start_year+hold_period+invest_period+sell_period
                risk = self.inv_utils.get_monthly_risk(start_y=start_year, start_month=month, end_year=end_year, end_month=month)
                risks.append(risk)

        ''' calculate average annual return of multiple wallets '''
        avg_pct_ret = sum(pct_rets)/len(pct_rets)
        avg_annual_pct_ret = self.inv_utils.get_annual_pct_return(pct_ret=avg_pct_ret, years=hold_period)

        ''' now let's calculate avg risk'''
        avg_risk = sum(risks)/float(len(risks))   

        response = {
            'avg_annual_pct_ret': avg_annual_pct_ret,
            'avg_risk': avg_risk
        }
        return response

    def buy24mo_hold10y_sell(self,*, start_year, month=1, hold_period=10, sell_once=True):
        ''' tests the following strategy:
            invest monthly (100/24) for 2 years, withdraw everything once after 10y...
        '''
        invest_years = 2
        investment = 100.0
        current_balance = []
        rets = []

        final_year = start_year + invest_years + hold_period
        total_months = invest_years*12
        curr_month = month
        count_months = 0
        curr_year = start_year

        sell_month = month
        while(count_months < total_months):
            if curr_month > 12:
                curr_month = 1
                curr_year += 1
                if not sell_once:
                    final_year += 1
            curr_month += 1
            count_months += 1
            
            if not sell_once:
                sell_month = curr_month
            start_close = self.inv_utils.get_first_close_of_month(curr_year, month=curr_month)
            end_close = self.inv_utils.get_first_close_of_month(final_year, month=sell_month)
            multiplier = end_close/start_close
            current_balance.append(multiplier*investment)
            rets.append(multiplier-1)
        current_balance = np.array(current_balance)
        current_balance = np.sum(current_balance)/len(current_balance)
        multiplier = current_balance/investment
        pct_ret = 100 * (multiplier-1)
        return pct_ret