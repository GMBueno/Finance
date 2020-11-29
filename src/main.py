import pandas as pd
import pandas_datareader.data as web
import numpy as np
import investment_strategies as invest
import unittest
from pprint import pprint as pp

# invest.load_returns()
DEBUG = False

def calc_i():
    avg_ret_and_risk = invest.simulate_buyonce_hold10y_sellonce()
    avg_annual_pct_ret = avg_ret_and_risk['avg_annual_pct_ret']
    avg_risk = avg_ret_and_risk['avg_risk']
    print(f'Strategy: Buy once, Hold 10y, Sell once')
    print(f'Average annual return: {avg_annual_pct_ret:.2f}%')
    print(f'Average Risk: {avg_risk:.2f}%')

def calc_ii():
    avg_ret_and_risk = invest.simulate_buy24mo_hold10y_sellonce()
    avg_annual_pct_ret = avg_ret_and_risk['avg_annual_pct_ret']
    avg_risk = avg_ret_and_risk['avg_risk']    
    print(f'Strategy: Buy 24mo, Hold 10y, Sell once')
    print(f'Average annual return: {avg_annual_pct_ret:.2f}%')
    print(f'Average Risk: {avg_risk:.2f}%')



def strat():
    '''
    tests the following strategy:
    invest monthly (100/24) for 2 years, withdraw everything once after 12y...
    '''
    start_year = 1995
    hold_period = 12
    invest_period = 2
    investment = 100.0
    invests = []
    rets = []
    for yy in range(start_year, start_year+invest_period):
        for mm in range(1,13):
            start_close = invest.get_first_close_of_month(yy, month=mm)
            end_close = invest.get_first_close_of_year(start_year+hold_period)
            ret = end_close/start_close
            invests.append(ret*investment)
            rets.append(ret-1)
    invests = np.array(invests)
    current_balance = np.sum(invests)/len(invests)
    multiplier = current_balance/investment
    ret = 100 * (multiplier-1)
    annual_multiplier = (multiplier**(1/float(hold_period)))
    annual_ret = 100*(annual_multiplier-1)

    print(f'24-month Entry in 1995. One-time sell after 12y.')
    print(f'\tInital Investment: {investment}')
    print(f'\tCurrent Balance: {current_balance:.2f}')
    print(f'\tAnnual Return: {annual_ret:.2f}%')
    print(f'\tOverall Return: {ret:.2f}%\n')

    '''
    tests the following strategy:
    invest monthly (100/24) for 2 years, withdraw everything once after 20y...
    '''
    start_year = 1995
    hold_period = 20
    invest_period = 2
    investment = 100.0
    invests = []
    rets = []
    for yy in range(start_year, start_year+invest_period):
        for mm in range(1,13):
            start_close = invest.get_first_close_of_month(yy, month=mm)
            end_close = invest.get_first_close_of_year(start_year+hold_period)
            ret = end_close/start_close
            invests.append(ret*investment)
            rets.append(ret-1)
    invests = np.array(invests)
    current_balance = np.sum(invests)/len(invests)
    multiplier = current_balance/investment
    ret = 100 * (multiplier-1)
    annual_multiplier = (multiplier**(1/float(hold_period)))
    annual_ret = 100*(annual_multiplier-1)

    print(f'24-month Entry in 1995. One-time sell after 20y.')
    print(f'\tInital Investment: {investment}')
    print(f'\tCurrent Balance: {current_balance:.2f}')
    print(f'\tAnnual Return: {annual_ret:.2f}%')
    print(f'\tOverall Return: {ret:.2f}%')
    print(f'\tnote: due to 2008 crash, market in 2015 was still similar to 2007\n')




calc_i()
calc_ii()
