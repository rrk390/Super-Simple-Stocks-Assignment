import unittest
import math
import superSimpleStocksAssignment
import time

class TestSuperSimpleStocksAssignment(unittest.TestCase):
    def testCalculateDividendYield(self):
        stock_name = superSimpleStocksAssignment.SuperSimpleStock('test/stock_data.csv')
        self.assertAlmostEqual(0, stock_name.calculate_dividend_yield(stock_name='TEA', stock_input_price=2))
        self.assertAlmostEqual(7.667, stock_name.calculate_dividend_yield(stock_name= 'ALE', stock_input_price= 3), places= 3)
        self.assertAlmostEqual(0.667, stock_name.calculate_dividend_yield(stock_name= 'GIN', stock_input_price= 3), places= 3)

        self.assertRaises(superSimpleStocksAssignment.SuperSimpleStocksException, stock_name.calculate_dividend_yield, stock_name= 'FOOBAR', stock_input_price= 3)
    
    def testCalculatePERatio(self):
        stock_name = superSimpleStocksAssignment.SuperSimpleStock('test/stock_data.csv')
        self.assertTrue(math.isnan(stock_name.calculate_pe_ratio(stock_name='TEA', stock_input_price=2)))
        self.assertAlmostEqual(3/7.667, stock_name.calculate_pe_ratio(stock_name='ALE', stock_input_price=3), places=3)

    def testRecordTrade(self):
        stock_name = superSimpleStocksAssignment.SuperSimpleStock('test/stock_data.csv')
        stock_name.record_trade(stock_name='ALE', quantity=10, buyORsell=True, price=5)
        self.assertEqual(1, len(stock_name.trade))
        stock_name.record_trade(stock_name='TEA', quantity=10, buyORsell=True, price=5)
        self.assertEqual(2, len(stock_name.trade))

        self.assertRaises(superSimpleStocksAssignment.SuperSimpleStocksException, stock_name.record_trade, stock_name= 'FOOBAR', quantity= 10, buyORsell= True, price= 5)

    def testCalculateStockPrice(self):
        stock_name = superSimpleStocksAssignment.SuperSimpleStock('test/stock_data.csv')
        self.assertTrue(math.isnan(stock_name.calculate_valume_weighted_stock_price('ALE')))
        stock_name.record_trade(stock_name='ALE', quantity=10, buyORsell=True, price=5)
        stock_name.record_trade(stock_name='ALE', quantity=15, buyORsell=True, price=4)

        self.assertTrue(math.isnan(stock_name.calculate_valume_weighted_stock_price('TEA')))
        stock_name.record_trade(stock_name='TEA', quantity=100, buyORsell=True, price=50)
        stock_name.record_trade(stock_name='TEA', quantity=150, buyORsell=True, price=40)
        
        self.assertAlmostEqual(4.4, stock_name.calculate_valume_weighted_stock_price('ALE'))
        self.assertAlmostEqual(44.0, stock_name.calculate_valume_weighted_stock_price('TEA'))

        time.sleep(2)
        self.assertTrue(math.isnan(stock_name.calculate_valume_weighted_stock_price('TEA', last_minutes=0.01)))

    
    def testGetAllShareIndex(self):
        stock_name = superSimpleStocksAssignment.SuperSimpleStock('test/stock_data.csv')
        self.assertTrue(math.isnan(stock_name.calculate_all_gbce_share_index()))
        stock_name.record_trade(stock_name='ALE', quantity=10, buyORsell=True, price=1)
        stock_name.record_trade(stock_name='ALE', quantity=15, buyORsell=True, price=2)
        stock_name.record_trade(stock_name='TEA', quantity=100, buyORsell=True, price=3)
        stock_name.record_trade(stock_name='TEA', quantity=150, buyORsell=True, price=4)

        self.assertAlmostEqual(2.21, stock_name.calculate_all_gbce_share_index(), places=2)

if __name__=='__main__':
    unittest.main()

