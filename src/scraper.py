import os
import pickle
import datetime as dt

import bs4 as bs
import requests as req
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
import numpy as np

def scrap_and_save_sp500_tickers():
    '''
    Scraps list of S&P 500 from Wikipedia then saves their stock symbols/tickers
    as a python object (using pickle)
    '''
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
    '''
    For all stock tickers, gets their stock data from Yahoo Finance and save csv
    '''
    if reload_sp500:
        tickers = scrap_and_save_sp500_tickers()
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

# get_data_from_yahoo()

def compile_data():
    '''
    For every stock ticker, gets their csv, drops all columns but 'Adj Close'
    and joins into a csv (in the end containing S&P 500 stocks Adj Close)
    '''
    with open('../data/sp500_tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv(f'../data/stocks_dfs/{ticker}.csv')
        df.set_index('Date', inplace=True)

        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        df.drop(['Open','High','Low','Close','Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)

    print(main_df.tail())
    main_df.to_csv('../data/sp500_joined_adjcloses.csv')

# compile_data()

def get_correlation_table():
    '''
    Calculates the correlation matrix of all the stocks in
    'sp500_joined_adjcloses.csv' 
    '''
    df = pd.read_csv('../data/sp500_joined_adjcloses.csv')
    # df['AAPL'].plot()
    # plt.show()

    df.set_index('Date', inplace=True)
    '''
    We wanna check  how closely related the stock movement is to each other.
    It's better to measure the correlation of the % of variation of Adj Close in
    different stocks, not just amount variatiob. Let's say stock X is $100 and
    stock B is $10 and they move 1$. The variation in amount is pretty different
    than the variation in percentage, that makes more sense when evaluating
    correlation.
    '''
    df_corr = df.pct_change().corr()
    df_corr.to_csv('../data/sp500_correlation.csv')

    with open('../data/sp500_correlation.pickle', 'wb') as f:
        pickle.dump(df_corr, f)

# get_correlation_table()

def visualize_data():
    with open('../data/sp500_correlation.pickle', 'rb') as f:
        df = pickle.load(f)

    heatmap = sns.heatmap(df,
        annot=False,
        cmap='RdYlGn',
        xticklabels='auto', yticklabels='auto',
        vmin = -1.0, vmax = 1.0)

    # plt.show()
    # TODO: save figure with non-overlapping labels (will obvs be very large,
    # since the table is 500x500. If a label font is ~20 pixels in x or y, would
    # be an img with resolution of at least 10.000x10.000 (3x size of an 8K img)
    heatmap = heatmap.get_figure()
    heatmap.savefig('../static/sp500_correlation_matrix.png', dpi=400)

visualize_data()
