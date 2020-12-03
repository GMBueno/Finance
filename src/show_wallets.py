import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

def get_wallet_A():
    stocks = [
        'BBDC4.SA', 'BBAS3.SA', # Bradesco (BBDC4) e Banco do Brasil (BBAS3))
        'PSSA3.SA', 'BBSE3.SA', # Porto Seguro (PSSA3) e BB Seguridade (BBSE3))
        'VIVT4.SA', 'TELB4.SA', # Telefônica (VIVT4) e Telebrás (TELB4))
        'CPLE3.SA', 'CPFE3.SA', # Copel (CPLE3) e CPFL Energia (CPFE3))
        'SAPR3.SA', 'SBSP3.SA', # Sanepar (SAPR3) e Sabesp (SBSP3))
    ]
    div = 1.68577
    df, total = get_df(stocks, div)
    return df, total

def get_wallet_ibov():
    stocks = ['^BVSP']
    div = 503.65
    df, total = get_df(stocks, div)
    return df, total

def get_wallet_B():
    stocks = [
        'LAME4.SA', 'VVAR3.SA', # Lojas Americanas (LAME4) e Via Varejo (VVAR3))
        'BRFS3.SA', 'JBSS3.SA', # Brasil Foods (BRFS3) e JBS (JBSS3))
        'GOLL4.SA', 'CVCB3.SA', # Gol (GOLL4) e CVC (CVCB3))
        'CYRE3.SA', 'DIRR3.SA', # Cyrela (CYRE3) e Direcional Engenharia (DIRR3))
    ]
    df, total = get_df(stocks, 1.1323)
    return df, total

def get_df(stocks, div):
    dfs = []
    for stock in stocks:
        # we use parse_dates and index_col so date is an index (and it's column 0)
        dfs.append(pd.read_csv(f'./csv/{stock}.csv', parse_dates=True, index_col=0))


    total = 0
    for df in dfs:
        total += df['Adj Close']

    total = total/div

    df1 = pd.read_csv(f'./csv/{stock}.csv', parse_dates=True, index_col=0)
    return df1, total

def show(df, total):
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan=5, colspan=1)
    ax1.plot(df.index, total)

    plt.show()

def show_all():
    dfa, totala = get_wallet_A()
    dfb, totalb = get_wallet_B()
    dfi, totali = get_wallet_ibov()

    ax1 = plt.subplot2grid((8,1), (0,0), rowspan=5, colspan=1)
    ax1.plot(dfa.index, totala)
    ax1.plot(dfb.index, totalb)
    ax1.plot(dfi.index, totali)

    plt.show()

def show_a():
    df, total = get_wallet_A()
    show(df, total)

def show_b():
    df, total = get_wallet_B()
    show(df, total)

def show_ibov():
    df, total = get_wallet_ibov()
    show(df, total)

show_all()