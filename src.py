from datetime import datetime, timedelta
from functools import reduce
from stock_project.utils import (find_recent_trades, convert_to_pounds,
                                 convert_to_percent)


class Stock:
    def __init__(self, symbol, stock_type, last_dividend, par_value,
                 fixed_dividend=None):
        self.symbol = symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.fixed_dividend = fixed_dividend

    def calculate_dividend_yield(self, price):
        """
        This method calculates dividend yield
        :param price: float
        :return: float
        """
        if self.stock_type == 'Preferred':
            return convert_to_percent(self.fixed_dividend * self.par_value/price)
        else:
            return convert_to_percent(self.last_dividend/price)

    def calculate_pe_ratio(self, price):
        """
        This method calculates P/E ratio
        :param price: float
        :return: float
        """
        if self.last_dividend == 0:
            return None
        return price/self.last_dividend


class Trade:
    """
    This class represents a single transaction
    symbol - symbol of action (e.g. 'TEA')
    timestamp - when the transaction took place
    quantity - quantity of actions bought/sold
    indicator - "buy" or "sell"
    price - price paid
    """
    def __init__(self, symbol, timestamp, quantity, indicator, price):
        self.symbol = symbol
        self.timestamp = timestamp
        self.quantity = quantity
        self.indicator = indicator
        self.price = price

    def __repr__(self):
        return f'{self.symbol}-{self.timestamp}-{self.price}-{self.quantity}'


class StockMarket:
    """
    This class represents the StockMarket
    """

    def __init__(self, trades):
        """
        The StockMarket constructor
        :param trades: list
        """
        self.trades = trades

    def calculate_volume_weighted_price(self):
        """
        The method calculates the Volume Weighted Stock Price
        based on trades conducted in last 15 minutes.
        :param trades: list of Trade objects
        :return: sum in pounds
        """
        time_expression = datetime.utcnow() - timedelta(minutes=15)
        recent_trades = list(find_recent_trades(self.trades, time_expression))
        numerator = sum(t.price * t.quantity for t in recent_trades)
        denominator = sum(t.quantity for t in recent_trades)
        return convert_to_pounds(numerator/denominator)

    def calculate_gbce(self):
        """
        The method calculates GBCE for all transactions
        :param trades: list of Trade objects
        :return: percentage
        """
        prices = [t.price for t in self.trades]
        result = reduce(lambda x, y: x*y, prices) ** 1/len(prices)
        return result
