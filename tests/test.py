import pytest
from datetime import datetime, timedelta

from stockmarket.src import Stock, StockMarket, Trade
from stockmarket.utils import (find_recent_trades, is_recent_trade,
                                 convert_to_pounds, convert_to_percent)

NOW = datetime.utcnow()
TRADES = 3
QUANTITIES = [100, 200, 50]
PRICES = [50, 55, 35.76]
SYMBOLS = ['TEA', 'GIN', 'JOE']


@pytest.fixture()
def stocks():
    return [
        Stock('TEA', 'Common', last_dividend=0, par_value=100),
        Stock('POP', 'Common', last_dividend=8, par_value=100),
        Stock('ALE', 'Common', last_dividend=23, par_value=60),
        Stock('GIN', 'Preferred', last_dividend=8, par_value=100,
              fixed_dividend=0.02),
        Stock('JOE', 'Common', last_dividend=13, par_value=250),
              ]


@pytest.fixture()
def trades():
    MOMENTS = [NOW-timedelta(seconds=2), NOW - timedelta(minutes=1),
               NOW-timedelta(
        minutes=20)]
    return [Trade(symbol=SYMBOLS[i],
                  timestamp=MOMENTS[i], quantity=QUANTITIES[i],
                  indicator='buy', price=PRICES[i]) for i in range(0, TRADES)]


@pytest.fixture()
def stockmarket(trades):
    return StockMarket(trades)


def test_create_stock(stocks):
    assert stocks[0].symbol == 'TEA'
    assert stocks[1].symbol == 'POP'
    assert stocks[2].last_dividend == 23
    assert stocks[3].fixed_dividend == 0.02
    assert stocks[4].par_value == 250


def test_create_trade(trades):
    assert len(trades) == 3
    assert trades[0].quantity == 100
    assert trades[1].symbol == 'GIN'
    assert trades[2].price == 35.76


def test_create_stockmarket(stockmarket, trades):
    assert stockmarket.trades == trades


def test_is_recent(trades):
    recent_trades = find_recent_trades(trades, NOW-timedelta(minutes=15))
    assert list(recent_trades) == trades[:-1]


def test_is_recent_trade(trades):
    assert not is_recent_trade(trades[0], NOW-timedelta(seconds=1))
    assert is_recent_trade(trades[0], NOW-timedelta(minutes=30))
    assert not is_recent_trade(trades[1], NOW-timedelta(seconds=2))
    assert is_recent_trade(trades[1], NOW-timedelta(minutes=2))
    assert not is_recent_trade(trades[2], NOW-timedelta(minutes=2))
    assert is_recent_trade(trades[2], NOW-timedelta(hours=2))


def test_convert_to_pounds(trades):
    assert convert_to_pounds(trades[2].price) == '£35.76'


def test_convert_to_percent():
    assert convert_to_percent(0.02) == '2.0%'
    assert convert_to_percent(0.025) == '2.5%'
    assert convert_to_percent(1) == '100%'
    assert convert_to_percent(1/3) == '33.33333333333333%'


def test_calculate_dividend_yield(stocks):
    assert stocks[0].calculate_dividend_yield(price=50) == '0.0%'
    assert stocks[1].calculate_dividend_yield(price=50) == '16.0%'


def test_calculate_pe_ratio(stocks):
    assert stocks[0].calculate_pe_ratio(price=50.23) is None
    assert stocks[1].calculate_pe_ratio(price=50.00) == 6.25
    assert stocks[1].calculate_pe_ratio(price=100.00) == 12.5


def test_calculate_volume_weighted_price(stockmarket):
    assert stockmarket.calculate_volume_weighted_price() == '£53.33'


def test_calculate_gbce(stockmarket):
    assert stockmarket.calculate_gbce() == 32780.0
