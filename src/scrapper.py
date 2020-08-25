import os
import pickle
import datetime as dt

import bs4 as bs
import requests as req
import pandas as pd
import pandas_datareader.data as web

def save_sp500_tickers():
    res = req.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(res.text, features='lxml')
    table = soup.find('table', {"id": "constituents"})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.find('td').text
        # Tickers can come with the new line character and we don't want that.
        ticker = ticker.replace('\n','')
        # Some stock tickers contain a dot instead of a hyphen. Ex: in Wikipedia
        # Brown-Forman Corp is listed BF.B, but in Yahoo it's listed BF-B.
        if "." in ticker:
            ticker = ticker.replace('.','-')
            print('ticker replaced to', ticker)
        tickers.append(ticker)

    with open('../data/sp500_tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)

    print('reloaded S&P 500 tickers')
    return tickers


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open('../data/sp500_tickers.pickle', 'rb') as f:
            tickers = pickle.load(f)

    if not os.path.exists('../data/stocks_dfs'):
        os.makedirs('../data/stocks_dfs')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2020,5,31)

    curr_ticker = 1
    total_tickers = len(tickers)
    for ticker in tickers:
        print(f'==> {curr_ticker}/{total_tickers}\t Searching for {ticker}')
        curr_ticker += 1
        if not os.path.exists(f'../data/stocks_dfs/{ticker}.csv'):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv(f'../data/stocks_dfs/{ticker}.csv')
            print(f'\t\t... {ticker} just retrieved\n')
        else:
            print(f'\t\t... {ticker} already exists\n')

get_data_from_yahoo()
