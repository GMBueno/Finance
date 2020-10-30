import pandas as pd
import pandas_datareader.data as web
import numpy as np
import investment_strategies as invest
import unittest

# invest.load_returns()

def calc_ii():
    start_year = 1995
    investment = 100.0
    invests = []
    final_cash = 100
    rets = []
    for yy in range(start_year, start_year+2):
        for mm in range(1,13):
            start_close = invest.get_first_close_of_month(yy, month=mm)
            end_close = invest.get_first_close_of_year(start_year+10)
            ret = end_close/start_close
            invests.append(ret*investment)
            rets.append(ret-1)
    invests = np.array(invests)
    now_money = np.sum(invests)/len(invests)
    ret = 100 * ((now_money/investment)-1)
    print(f'24-month Entry. One-time sell after 10y.')
    print(f'initial investment: {investment}, now: {now_money:.2f}. Return: {ret:.2f}%\n')

    close1 = invest.get_first_close_of_year(1995)
    close2 = invest.get_first_close_of_year(2005)
    now_money = (close2/close1)*100
    ret = 100 * ((close2/close1)-1)
    print(f'One-time Entry. One-time sell after 10y.')
    print(f'inital investment: {investment}, now: {now_money:.2f}. Return: {ret:.2f}%')

calc_ii()
