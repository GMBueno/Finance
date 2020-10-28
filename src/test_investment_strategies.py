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
