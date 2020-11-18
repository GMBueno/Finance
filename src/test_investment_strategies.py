import pandas as pd
import pandas_datareader.data as web
import numpy as np
import investment_strategies as invest
import unittest

# print('true:', invest.is_before('1996-01-01', '1996-01-02'))

class Test(unittest.TestCase):

    def test_is_before(self):
        self.assertFalse(invest.is_before('1996-01-01', '1996-01-01'))
        self.assertFalse(invest.is_before('1996-02-01', '1996-01-01'))
        self.assertFalse(invest.is_before('1997-01-01', '1996-01-01'))
        self.assertFalse(invest.is_before('2010-01-01', '1998-12-31'))
        self.assertTrue(invest.is_before('1998-12-31', '2010-01-01'))
        self.assertTrue(invest.is_before('1996-01-01', '1996-02-01'))
        self.assertTrue(invest.is_before('1996-01-01', '1997-01-01'))
        self.assertTrue(invest.is_before('1996-01-01', '1996-01-02'))

    def test_make_date(self):
        self.assertEqual('1998-02-18', invest.make_date(1998, 2, 18))
        self.assertEqual('2000-01-01', invest.make_date(2000, 1, 1))
        self.assertNotEqual('2000-1-01', invest.make_date(2000, 1, 1))
        self.assertNotEqual('2000-01-1', invest.make_date(2000, 1, 1))
        self.assertNotEqual('2000-1-1', invest.make_date(2000, 1, 1))

    def test_buy24mo_hold10y_sellonce(self):
        '''
        tests the following strategy:
        invest monthly (100/24) for 2 years, withdraw everything once after 10y...
        '''
        start_year = 1995
        hold_period = 10
        investment = 100.0
        invests = []
        rets = []
        for yy in range(start_year, start_year+2):
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
        annual_multiplier = (multiplier**(1/float(10)))
        annual_ret = 100*(annual_multiplier-1)
        self.assertAlmostEqual(current_balance, 564.08, delta=0.1)
        self.assertAlmostEqual(annual_ret, 18.89, delta=0.1)
        self.assertAlmostEqual(ret, 464.08, delta=0.1)

    def test_buy24mo_hold12y_sellonce(self):
        '''
        tests the following strategy:
        invest monthly (100/24) for 2 years, withdraw everything once after 10y...
        '''
        start_year = 1995
        hold_period = 12
        investment = 100.0
        invests = []
        rets = []
        for yy in range(start_year, start_year+2):
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
        annual_multiplier = (multiplier**(1/float(10)))
        annual_ret = 100*(annual_multiplier-1)
        self.assertAlmostEqual(current_balance, 995.24, delta=0.1)
        # self.assertAlmostEqual(annual_ret, 18.89, delta=0.1)
        # self.assertAlmostEqual(ret, 464.08, delta=0.1)

    def test_buyonce_hold10y_sellonce(self):
        '''
        tests the following strategy:
        invest R$100 once and withdraw everything ten years later, also once;
        '''
        investment = 100.0
        close1 = invest.get_first_close_of_year(1995)
        close2 = invest.get_first_close_of_year(2005)
        current_balance = (close2/close1)*100
        multiplier = close2/close1
        ret = 100*(multiplier-1)
        annual_multiplier = (multiplier**(1/float(10)))
        annual_ret = 100*(annual_multiplier-1)
        self.assertAlmostEqual(current_balance, 598.05, delta=0.1)
        self.assertAlmostEqual(annual_ret, 19.58, delta=0.1)
        self.assertAlmostEqual(ret, 498.05, delta=0.1)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
