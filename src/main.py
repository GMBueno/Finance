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
    avg_ret_and_risk = inv_strats.simulate_buyonce_hold10y_sellonce(2000, 2010)
    avg_annual_pct_ret = avg_ret_and_risk['avg_annual_pct_ret']
    avg_risk = avg_ret_and_risk['avg_risk']
    return(avg_annual_pct_ret, avg_risk)

def calc_ii():
    avg_ret_and_risk = inv_strats.simulate_buy24mo_hold10y_sellonce(2000, 2008)
    avg_annual_pct_ret = avg_ret_and_risk['avg_annual_pct_ret']
    avg_risk = avg_ret_and_risk['avg_risk']    
    return(avg_annual_pct_ret, avg_risk)

def calc_iii():
    avg_ret_and_risk = inv_strats.simulate_buy24mo_hold10y_sell24mo(2000, 2006)
    avg_annual_pct_ret = avg_ret_and_risk['avg_annual_pct_ret']
    avg_risk = avg_ret_and_risk['avg_risk']    
    return(avg_annual_pct_ret, avg_risk)

def calc_ibov():
    ''' we are going to invest in Bovespa index (B3)'''
    stock = '^BVSP'

    ''' gets pct return on investment '''
    inv_utils = InvestUtils(stock)
    pct_ret = inv_utils.get_all_return()
    
    ''' calculates yearly return'''
    annual_pct_ret = inv_utils.get_annual_pct_return(pct_ret=pct_ret, years=6.5)
    ''' calculates risk'''
    risk = inv_utils.get_monthly_risk(start_y=2014, start_month=1, end_year=2020, end_month=7)

    return(annual_pct_ret, risk) 


def calc_wallet_1():
    ''' we are going to invest 10% in each of 10 companies and get our return'''
    stocks = [
        'BBDC4.SA', 'BBAS3.SA', # Bradesco (BBDC4) e Banco do Brasil (BBAS3))
        'PSSA3.SA', 'BBSE3.SA', # Porto Seguro (PSSA3) e BB Seguridade (BBSE3))
        'VIVT4.SA', 'TELB4.SA', # Telefônica (VIVT4) e Telebrás (TELB4))
        'CPLE3.SA', 'CPFE3.SA', # Copel (CPLE3) e CPFL Energia (CPFE3))
        'SAPR3.SA', 'SBSP3.SA', # Sanepar (SAPR3) e Sabesp (SBSP3))
    ]

    ''' gets all returns of the 10 companies '''
    pct_rets = []
    for stock in stocks:
        inv_utils = InvestUtils(stock)
        pct_ret = inv_utils.get_all_return()
        pct_rets.append(pct_ret)
    
    ''' calculates overall return'''
    overall_return = sum(pct_rets)/len(pct_rets)
    ''' calculates yearly return'''
    annual_pct_ret = inv_utils.get_annual_pct_return(pct_ret=overall_return, years=6.5)
    ''' calculates risk'''
    risk = inv_utils.get_monthly_risk(start_y=2014, start_month=1, end_year=2020, end_month=7)

    return(annual_pct_ret, risk)



def calc_wallet_2():
    ''' we are going to invest equally in 8 companies and get our return'''
    stocks = [
        'LAME4.SA', 'VVAR3.SA', # Lojas Americanas (LAME4) e Via Varejo (VVAR3))
        'BRFS3.SA', 'JBSS3.SA', # Brasil Foods (BRFS3) e JBS (JBSS3))
        'GOLL4.SA', 'CVCB3.SA', # Gol (GOLL4) e CVC (CVCB3))
        'CYRE3.SA', 'DIRR3.SA', # Cyrela (CYRE3) e Direcional Engenharia (DIRR3))
    ]

    ''' gets all returns of the 10 companies '''
    pct_rets = []
    for stock in stocks:
        inv_utils = InvestUtils(stock)
        pct_ret = inv_utils.get_all_return()
        pct_rets.append(pct_ret)
    
    ''' calculates overall return'''
    overall_return = sum(pct_rets)/len(pct_rets)
    ''' calculates yearly return'''
    annual_pct_ret = inv_utils.get_annual_pct_return(pct_ret=overall_return, years=6.5)
    ''' calculates risk'''
    risk = inv_utils.get_monthly_risk(start_y=2014, start_month=1, end_year=2020, end_month=7)

    return(annual_pct_ret, risk)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_results():

    ''' INVESTMENT STRATEGIES '''

    print(f'{bcolors.OKCYAN}Simulating invesment strategies...2000-2020{bcolors.ENDC}')

    print('1. Buy once, Hold 10y after only aport, Sell once')
    avg_annual_pct_ret, avg_risk = calc_i()
    print(f'\tAverage annual return: {bcolors.OKGREEN}{avg_annual_pct_ret:.3f}%{bcolors.ENDC}')
    print(f'\tAverage Risk:\t\t{bcolors.WARNING}{avg_risk:.3f}%{bcolors.ENDC}')

    print('2. Buy 24mo, Hold 10y after last aport, Sell once')
    avg_annual_pct_ret, avg_risk = calc_ii()
    print(f'\tAverage annual return: {bcolors.OKGREEN}{avg_annual_pct_ret:.3f}%{bcolors.ENDC}')
    print(f'\tAverage Risk:\t\t{bcolors.WARNING}{avg_risk:.3f}%{bcolors.ENDC}')   

    print('3. Buy 24mo, Hold 10y after last aport, Sell 24mo')
    avg_annual_pct_ret, avg_risk = calc_iii()
    print(f'\tAverage annual return: {bcolors.OKGREEN}{avg_annual_pct_ret:.3f}%{bcolors.ENDC}')
    print(f'\tAverage Risk:\t\t{bcolors.WARNING}{avg_risk:.3f}%{bcolors.ENDC}')

    ''' Bovespa Index 2014-2020 '''

    print('')
    print(f'{bcolors.OKCYAN}Investment in Bovespa index...2014-2020{bcolors.ENDC}')
    avg_annual_pct_ret, avg_risk = calc_ibov()
    print(f'\tAverage annual return:\t{bcolors.OKGREEN}{avg_annual_pct_ret:.3f}%{bcolors.ENDC}')
    print(f'\tAverage Risk:\t\t{bcolors.WARNING}{avg_risk:.3f}%{bcolors.ENDC}') 

    ''' WALLETS '''

    print('')
    print(f'{bcolors.OKCYAN}Simulating two wallets...2014-2020{bcolors.ENDC}')

    print('1. Recommended (banks, insurance, telecom, energy & sanitation)')
    avg_annual_pct_ret, avg_risk = calc_wallet_1()
    print(f'\tAverage annual return:\t{bcolors.OKGREEN}{avg_annual_pct_ret:.3f}%{bcolors.ENDC}')
    print(f'\tAverage Risk:\t\t{bcolors.WARNING}{avg_risk:.3f}%{bcolors.ENDC}')

    print('2. Advised against (retail, meat-processing, aviation, tourism & civil engineering)')
    avg_annual_pct_ret, avg_risk = calc_wallet_2()
    print(f'\tAverage annual return:\t{bcolors.OKGREEN}{avg_annual_pct_ret:.3f}%{bcolors.ENDC}')
    print(f'\tAverage Risk:\t\t{bcolors.WARNING}{avg_risk:.3f}%{bcolors.ENDC}')  


print_results()