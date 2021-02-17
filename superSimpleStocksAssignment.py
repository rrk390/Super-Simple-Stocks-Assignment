"""
Introduction: Implementation of Super Simple Stocks system of The Global Beverage Corporation Exchange, which is used to run trading.
Assigment : JP Morgan & Chase
Author : Ritish Ranjan Khan
"""

import pandas
import re
import math
import datetime
import dateutil

class SuperSimpleStock:
    def __init__(self, csv_file):
        self.gbce_input_data = self._read_stock_data(csv_file)
        self.trade = pandas.DataFrame({'Stock_Symbol':[], 'timestamp':[], 'quantity':[], 'buyORsell':[], 'price':[]})
    
    def calculate_dividend_yield(self, stock_name, stock_input_price):
        """
        Function to calculate dividend yield
        """
        stock_data = self.gbce_input_data[self.gbce_input_data['Stock_Symbol'] == stock_name]
        if len(stock_data['Type']) != 1:
            raise SuperSimpleStocksException("Invalid stock_name value for {}".format(stock_name))

        if list(stock_data['Type'])[0] == 'Common':
            return list(stock_data['Last_Dividend'])[0] / stock_input_price
        elif list(stock_data['Type'])[0] == 'Preferred':
            return (list(stock_data['Fixed_Dividend'])[0] * list(stock_data['Par_Value'])[0]) / stock_input_price
        else:
            raise Exception('Invalid stock_name type: {}'.format(stock_data['Type']))


    def calculate_pe_ratio(self, stock_name, stock_input_price):
        """
        Function to calculate the P/E Ratio
        """
        dividend = self.calculate_dividend_yield(stock_name, stock_input_price)
        if dividend == 0:
            return float('nan')
        return stock_input_price / dividend


    def record_trade(self, stock_name, quantity, buyORsell, price):
        """
        Function to record a trade, with timestamp, quantity, 
        buy or sell indicator and price
        """
        if stock_name not in set(self.gbce_input_data['Stock_Symbol']):
            raise SuperSimpleStocksException("Invalid SuperSimpleStock: %s".format(stock_name))

        trade = {'Stock_Symbol': stock_name,
        'timestamp': datetime.datetime.now().isoformat(),
        'quantity': quantity,
        'buyORsell': buyORsell,
        'price': price}

        self.trade = self.trade.append(trade, ignore_index=True)


    def calculate_valume_weighted_stock_price(self, stock_name, last_minutes=5):
        """
        Function to calculate Volume Weighted Stock Price 
        based on trades in past 5 minutes
        """
        transaction = datetime.datetime.now() - datetime.timedelta(minutes=last_minutes)

        if len(self.trade) == 0:
            return float('nan')

        transact_stock = self.trade[self.trade['Stock_Symbol'] == stock_name]
        if len(transact_stock) == 0:
            return float('nan')

        last_trades = [ dateutil.parser.parse(x) > transaction for x in list(transact_stock['timestamp']) ]

        transact_stock = transact_stock[last_trades]
        if len(transact_stock) == 0:
            return float('nan')

        return sum(transact_stock['price'] * transact_stock['quantity']) / sum(transact_stock['quantity'])
        

    def calculate_all_gbce_share_index(self):
        """
        Function to calculate the GBCE All Share Index using the geometric mean of the 
        Volume Weighted Stock Pricefor all stocks
        """
        if len(self.trade) == 0:
            return float('nan')
        
        all_share_index = 1
        n = 0
        for p in list(self.trade['price']):
            all_share_index *= p
            n = n+1
        return all_share_index ** (1 / n)

    def _read_stock_data(self, csv_file):
        """
        Function to read the csv file and returning a clean dataframe
        """
        gbce_input_data = pandas.read_csv(csv_file)
        fixed_dividend = []
        for x in gbce_input_data['Fixed_Dividend']:
            if type(x) == float and math.isnan(x):
                pass
            else:
                try:
                    x = float(re.sub('%$', '', x)) / 100
                except:
                    raise ("Cannot convert {} to numeric".format(x))
            fixed_dividend.append(x)
        gbce_input_data['Fixed_Dividend'] = fixed_dividend
        return gbce_input_data

class SuperSimpleStocksException(Exception):
    pass

