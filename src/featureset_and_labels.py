import numpy as np
import pandas as pd
# support vector machine, neighbors for keynyan neighbors
from sklearn import svm, neighbors
# for cross validation
from sklearn.model_selection import train_test_split
# voting classifier bc we are going to use many classifiers and let them vote
# what strategy is best. Random forest is another classifier
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

from collections import Counter
import pickle

def process_data_for_labels(ticker):
    '''
    Brief:
    This function receives the 'ticker' that it will calculate the stock price
    variation across 5 days. Then, it creates 5 new columns for the .csv that
    will represent the percentage variation of that stock in X days into the
    future.

    More details:
    It reads 'sp500_joined_adjcloses.csv', that is in the following format
    | AAPL | AMZN | ... | ticker
    |------|------|-----|
    | 200  | 4000 | ... | price in day 0
    | 210  | 4200 | ... | price in day 1
    | 220  | 4100 | ... | price in day 2
    | 200  | 3800 | ... | price in day 3
    | ...  | ...  | ... | price in day n

    Then, it calculates the variation of that received stock (ticker) in 5 days.
    Then, it creates a new column for each calculation. It means that the first
    cell in the column GE_3d (for ticker = 'GE', that is General Electric)
    will contain the variation in stock price of General Electric of 3 days from
    the first day in relation to the first day.
    More specifically, will be = (df[ticker].shift(-i) - df[ticker]) /df[ticker]
    This is a print of the last 5 rows and last 4 tickers on the dataframe:
                    GE_2d     GE_3d     GE_4d       GE_5d
    Date
    2020-05-22      0.137285  0.057722  0.024961    0.0
    2020-05-26     -0.002941 -0.033824  0.000000    0.0
    2020-05-27     -0.098765  0.000000  0.000000    0.0
    2020-05-28      0.000000  0.000000  0.000000    0.0
    2020-05-29      0.000000  0.000000  0.000000    0.0
    '''
    hm_days = 5  # how many days in the future. Is stock going to rise or fall?
    df = pd.read_csv('../data/sp500_joined_adjcloses.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    # calcs stock variation in the next hm_days in respect to today
    for i in range(1, hm_days+1):
        # day "i" in the future.
        df[f'{ticker}_{i}d'] = (df[ticker].shift(-i) - df[ticker])/df[ticker]

    df.fillna(0, inplace=True)
    # print(df[f'{ticker}'])
    # print(df[f'{ticker}_1d'])
    # print(df.tail())
    return tickers, df

# process_data_for_labels('AAPL')

def buy_sell_hold(*args):
    '''
    if variation of the stock price is above a certain requirement (2% in
    this case), we decide to buy (if positive) or sell (if negative) or hold if
    within the requirement (for all 5 days/columns).
    note that we check in chronological order. If the variation is not within 2%
    for the next day, we already decide if it is a buy or sell and return. We
    only check the next day (let's say, we only check ['ticker_2d'] if
    ['ticker_1d'] was a hold.
    '''
    cols = [col for col in args]
    requirement = 0.02 # means 2%
    for col in cols:
        if col > requirement:
            return 1  # buy
        if col < -requirement:
            return -1  # sell
    return 0  # hold

def extract_feature_sets(ticker):
    tickers, df = process_data_for_labels(ticker)

    # creates a new column with '1', '-1' or '0', meaning buy, sell or hold
    df[f'{ticker}_target'] = list(map(buy_sell_hold,
                                      df[f'{ticker}_1d'],
                                      df[f'{ticker}_2d'],
                                      df[f'{ticker}_3d'],
                                      df[f'{ticker}_4d'],
                                      df[f'{ticker}_5d']
                                      ))

    # calculate data spread, so when we add our strategy, we check if it's
    # better than random or just "buybuybuy", since stocks are usually going up.
    vals = df[f'{ticker}_target'].values.tolist()
    str_vals = [str(i) for i in vals]

    # printing data spread
    count = Counter(str_vals)
    print('Data spread:\t\t', {'Up':count['1'],'Still':count['0'],'Down':count['-1']})

    # some cleaning
    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    # today's value based on yesterday's value (% change)
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    # X is our feature set (daily percentage change for all stocks)
    X = df_vals.values
    # y is our labels (buy or sell or hold column (aswer) just for given ticker)
    y = df[f'{ticker}_target'].values

    return X, y, df

# extract_feature_sets('GE')

def do_ml(ticker):
    X, y, df = extract_feature_sets(ticker)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    # classifier
    clf = neighbors.KNeighborsClassifier()

    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)

    # if you want to not retrain the model, just pickle it.
    predictions = clf.predict(X_test)

    print('Prediction spread:\t', count(predictions))
    print(f'Accuracy {int(confidence*10000)/100.0}%')

    return confidence

def count(data):
    count = Counter(data)
    ans = {
        'Buy':count[1],
        'Hold':count[0],
        'Sell':count[-1],
        }
    return ans

# print('==> BAC') # Bank of America
# do_ml('BAC')
# print('\n==> AAPL') # Apple
# do_ml('AAPL')
# print('\n==> FB') # Facebook
# do_ml('FB')
# print('\n==> AMZN') # Amazon
# do_ml('AMZN')
# print('\n==> GE') # General Electric
# do_ml('GE')

'''
==> BAC
Data spread:		 {'Up': 1869, 'Still': 1582, 'Down': 1683}
Prediction spread:	 {'Buy': 407, 'Hold': 412, 'Sell': 465}
Accuracy 63.78%

==> AAPL
Data spread:		 {'Up': 2282, 'Still': 967, 'Down': 1885}
Prediction spread:	 {'Buy': 532, 'Hold': 219, 'Sell': 533}
Accuracy 61.37%

==> FB
Data spread:		 {'Up': 886, 'Still': 3567, 'Down': 681}
Prediction spread:	 {'Buy': 197, 'Hold': 910, 'Sell': 176}
Accuracy 85.11%

==> AMZN
Data spread:		 {'Up': 2307, 'Still': 864, 'Down': 1963}
Prediction spread:	 {'Buy': 547, 'Hold': 214, 'Sell': 523}
Accuracy 63.31%

==> GE
Data spread:		 {'Up': 1720, 'Still': 1709, 'Down': 1705}
Prediction spread:	 {'Buy': 366, 'Hold': 432, 'Sell': 486}
Accuracy 62.69%
'''
