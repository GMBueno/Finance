import pandas as pd
import pandas_datareader.data as web
import numpy as np
from investment_strategies import InvestmentStrategies
from investment_utils import InvestUtils
import unittest
from pprint import pprint as pp
import datetime as dt


inv_strats = InvestmentStrategies('^BVSP')
# inv_strats.load_returns()
DEBUG = False

def calc_i():
    avg_ret_and_risk = inv_strats.simulate_buyonce_hold10y_sellonce()
    avg_annual_pct_ret = avg_ret_and_risk['avg_annual_pct_ret']
    avg_risk = avg_ret_and_risk['avg_risk']
    print(f'Strategy: Buy once, Hold 10y, Sell once')
    print(f'Average annual return: {avg_annual_pct_ret:.2f}%')
    print(f'Average Risk: {avg_risk:.2f}%')

def calc_ii():
    avg_ret_and_risk = inv_strats.simulate_buy24mo_hold10y_sellonce()
    avg_annual_pct_ret = avg_ret_and_risk['avg_annual_pct_ret']
    avg_risk = avg_ret_and_risk['avg_risk']    
    print(f'Strategy: Buy 24mo, Hold 10y, Sell once')
    print(f'Average annual return: {avg_annual_pct_ret:.2f}%')
    print(f'Average Risk: {avg_risk:.2f}%')

def calc_wallet_1():
    ''' we are going to invest 10% in each of 10 companies and get our return'''
    stocks = [
        'BBDC4.SA', 'BBAS3.SA', # Bradesco (BBDC4) e Banco do Brasil (BBAS3))
        'PSSA3.SA', 'BBSE3.SA', # Porto Seguro (PSSA3) e BB Seguridade (BBSE3))
        'VIVT4.SA', 'TELB4.SA', # Telefônica (VIVT4) e Telebrás (TELB4))
        'CPLE3.SA', 'CPFE3.SA', # Copel (CPLE3) e CPFL energia (CPFE3))
        'SAPR3.SA', 'SBSP3.SA', # sanepar (SAPR3) e sabesp (SBSP3))
    ]

    ''' gets all returns of the 10 companies '''
    pct_rets = []
    for stock in stocks:
        inv_utils = InvestUtils(f'{stock}')
        pct_ret = inv_utils.get_all_return()
        pct_rets.append(pct_ret)
    
    ''' calculates overall return'''
    overall_return = sum(pct_rets)/len(pct_rets)
    ''' calculates yearly return'''
    annual_pct_ret = inv_utils.get_annual_pct_return(pct_ret=overall_return, years=7.5)

    print(f'==> Bullet proof wallet')
    print(f'\tOverall return:{overall_return:.2f}%')
    print(f'\tAnnual return: {annual_pct_ret:.2f}%')



def calc_wallet_2():
    ''' we are going to invest equally in 8 companies and get our return'''
    stocks = [
        'LAME4.SA', 'VVAR3.SA', # Lojas Americas (LAME4) e Via Varejo (VVAR3))
        'BRFS3.SA', 'JBSS3.SA', # Brasil Foods (BRFS3) e JBS (JBSS3))
        'GOLL4.SA', 'CVCB3.SA', # Gol (GOLL4) e CVC (CVCB3))
        'CYRE3.SA', 'DIRR3.SA', # Cyrela (CYRE3) e Direcional Engenharia (DIRR3))
    ]

    ''' gets all returns of the 10 companies '''
    pct_rets = []
    for stock in stocks:
        inv_utils = InvestUtils(f'{stock}')
        pct_ret = inv_utils.get_all_return()
        pct_rets.append(pct_ret)
    
    ''' calculates overall return'''
    overall_return = sum(pct_rets)/len(pct_rets)
    ''' calculates yearly return'''
    annual_pct_ret = inv_utils.get_annual_pct_return(pct_ret=overall_return, years=7.5)

    print(f'==> Barsi proof wallet')
    print(f'\tOverall return:{overall_return:.2f}%')
    print(f'\tAnnual return: {annual_pct_ret:.2f}%')

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




# calc_i()
# calc_ii()
calc_wallet_1()
calc_wallet_2()