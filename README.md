```sh
python main.py
```

![S&P500 correlation matrix](static/sp500_correlation_matrix.png)

_notes:_   
_Often enough competing companies will showcase a negative correlation
around the time of an important announcement. That said, the previous matrix
represents ~20 years of data, so we are not going to see this very narrow-timed
correlations._     
_Also, there are no negative numbers closer to -1 than to 0 because
we are biased by S&P 500, meaning that given two stocks with that correlation,
only one would be in the S&P 500, because the other would have had a dip in
price and would be removed from S&P 500 long before getting close to -1._

![Tesla (NASDAQ: TSLA) Stock price (US Dollars) 2010-2020](static/tslaplot.png)
