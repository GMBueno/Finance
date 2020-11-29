import pandas as pd
import pandas_datareader.data as web
import numpy as np
import investment_strategies as invest
from investment_utils import InvestUtils
import unittest

inv_utils = InvestUtils('^BVSP')

# print('true:', invest.is_before('1996-01-01', '1996-01-02'))

class Test(unittest.TestCase):

    def test_is_before(self):
        self.assertFalse(inv_utils.is_before('1996-01-01', '1996-01-01'))
        self.assertFalse(inv_utils.is_before('1996-02-01', '1996-01-01'))
        self.assertFalse(inv_utils.is_before('1997-01-01', '1996-01-01'))
        self.assertFalse(inv_utils.is_before('2010-01-01', '1998-12-31'))
        self.assertTrue(inv_utils.is_before('1998-12-31', '2010-01-01'))
        self.assertTrue(inv_utils.is_before('1996-01-01', '1996-02-01'))
        self.assertTrue(inv_utils.is_before('1996-01-01', '1997-01-01'))
        self.assertTrue(inv_utils.is_before('1996-01-01', '1996-01-02'))

    def test_make_date(self):
        self.assertEqual('1998-02-18', inv_utils.make_date(1998, 2, 18))
        self.assertEqual('2000-01-01', inv_utils.make_date(2000, 1, 1))
        self.assertNotEqual('2000-1-01', inv_utils.make_date(2000, 1, 1))
        self.assertNotEqual('2000-01-1', inv_utils.make_date(2000, 1, 1))
        self.assertNotEqual('2000-1-1', inv_utils.make_date(2000, 1, 1))

    def test_buy24mo_hold10y_sellonce(self):
        '''
        tests the following strategy:
        invest monthly (100/24) for 2 years, withdraw everything once after 10y...
        '''

        # self.assertAlmostEqual(current_balance, 564.08, delta=0.1)
        # self.assertAlmostEqual(annual_ret, 18.89, delta=0.1)
        # self.assertAlmostEqual(ret, 464.08, delta=0.1)

    def test_buy24mo_hold12y_sellonce(self):
        '''
        tests the following strategy:
        invest monthly (100/24) for 2 years, withdraw everything once after 10y...
        '''

        # self.assertAlmostEqual(current_balance, 995.24, delta=0.1)
        # self.assertAlmostEqual(annual_ret, 18.89, delta=0.1)
        # self.assertAlmostEqual(ret, 464.08, delta=0.1)

    def test_buyonce_hold10y_sellonce(self):
        '''
        tests the following strategy:
        invest R$100 once and withdraw everything ten years later, also once;
        '''
        pct_ret = invest.buyonce_hold10y_sellonce(start_year=1995, month=1)
        self.assertAlmostEqual(pct_ret, 498.05, delta=0.1)
        
        annual_pct_ret = inv_utils.get_annual_pct_return(pct_ret=pct_ret, years=10)
        self.assertAlmostEqual(annual_pct_ret, 19.58, delta=0.1)

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
