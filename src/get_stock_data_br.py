import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

stock_ticker = '^BVSP'  # since 1993
# stock_ticker = 'BOVA11.SA'  # since 2008
# stock_ticker = 'EGIE3.SA'  # since 2002

'''
Gets stock data from Yahoo and saves as a csv
'''

stock_tickers = [
    'BBDC4.SA', 'BBAS3.SA', # Bradesco (BBDC4) e Banco do Brasil (BBAS3))
    'PSSA3.SA', 'BBSE3.SA', # Porto Seguro (PSSA3) e BB Seguridade (BBSE3))
    'VIVT4.SA', 'TELB4.SA', # Telefônica (VIVT4) e Telebrás (TELB4))
    'CPLE3.SA', 'CPFE3.SA', # Copel (CPLE3) e CPFL energia (CPFE3))
    'SAPR3.SA', 'SBSP3.SA', # sanepar (SAPR3) e sabesp (SBSP3))
    'LAME4.SA', 'VVAR3.SA', # Lojas Americas (LAME4) e Via Varejo (VVAR3))
    'BRFS3.SA', 'JBSS3.SA', # Brasil Foods (BRFS3) e JBS (JBSS3))
    'GOLL4.SA', 'CVCB3.SA', # Gol (GOLL4) e CVC (CVCB3))
    'CYRE3.SA', 'DIRR3.SA', # Cyrela (CYRE3) e Direcional Engenharia (DIRR3))
]

# keep in mind that your stock might not have been traded in the entire period
start = dt.datetime(2014, 1, 1)
end = dt.datetime(2020, 7, 1)

def get_all_stocks():
    for stock_ticker in stock_tickers:
        get_one_stock(stock_ticker=stock_ticker)

def get_one_stock(*, stock_ticker):
    print(f'==> Retrieving {stock_ticker}')
    df = web.DataReader(stock_ticker, 'yahoo', start, end)
    df.to_csv(f'./csv/{stock_ticker}.csv')
    print(f'\tSuccess!\n')


def plot_stock_df(*, stock_df):
    style.use('ggplot')
    # we use parse_dates and index_col so date is an index (and it's column 0)
    df  = pd.read_csv(f'./csv/{stock_ticker}.csv', parse_dates=True, index_col=0)
    # print(df.head())

    fig, ax = plt.subplots()
    ax.set_ylabel('BRL (R$)')

    title = f'(B3: preço {stock_ticker}) '
    df['Adj Close'].plot(title=title, ax=ax)
    plt.show()

get_all_stocks()