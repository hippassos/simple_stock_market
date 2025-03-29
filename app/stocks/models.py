from dataclasses import dataclass, field
import datetime
import math
import logging
from typing import Dict, List


@dataclass
class Stock:
    symbol: str
    type: str
    last_dividend: int
    fixed_dividend: float
    par_value: int

    def calculate_dividend_yield(self, price: int) -> float:
        if price <= 0:
            return 0
        if self.type == "Common":
            return self.last_dividend / price
        else:
            return (self.fixed_dividend * self.par_value) / price

    def calculate_pe_ratio(self, price: int) -> float:
        if price <= 0 or self.last_dividend <= 0:
            return 0
        else:
            return price / self.last_dividend


@dataclass
class Trade:
    timestamp: datetime.datetime
    symbol: str
    quantity: int
    price: int
    trade_type: str


@dataclass
class StockMarket:
    trades: List[Trade] = field(default_factory=list)  # empty list default for a new instance
    stocks: Dict[str, Stock] = field(default_factory=dict)  # empty dict default for a new instance

    def add_stock(self, stock: Stock):
        self.stocks[stock.symbol] = stock

    def get_stock(self, symbol: str):
        return self.stocks.get(symbol)

    def list_stocks(self):
        return list(self.stocks.values())

    def list_trades(self):
        return self.trades

    def trade(self, symbol: str, quantity: int, price: int, trade_type: str):
        trade = Trade(datetime.datetime.now(datetime.timezone.utc), symbol, quantity, price, trade_type)  # utc aware timestamp
        self.trades.append(trade)

    def calculate_volume_weighted_stock_price(self, symbol: str):
        now = datetime.datetime.now(datetime.timezone.utc)  # utc aware timestamp
        # trades in relevant window
        relevant_trades = [t for t in self.trades if (now - t.timestamp).total_seconds() <= (60 * 15) and t.symbol == symbol]
        # ensure there are trades to work with
        if not relevant_trades:
            return 0
        total_quantity = sum(t.quantity for t in relevant_trades)
        total_trade_value = sum(t.quantity * t.price for t in relevant_trades)
        return total_trade_value / total_quantity

    def calculate_gbce_all_share_index(self):
        prices = [t.price for t in self.trades]
        if not prices:
            return 0
        try:
            # go through the arithetic mean of the lns to provide overflow resistance
            return math.exp(sum(math.log(p) for p in prices) / len(prices))
        except OverflowError as e:
            logging.error(f"GBCE All Share Index overflowed with trace {e}")
            raise


available_stocks = {
    "TEA": Stock("TEA", "Common", 0, 0, 100),
    "POP": Stock("POP", "Common", 8, 0, 100),
    "ALE": Stock("ALE", "Common", 23, 0, 60),
    "GIN": Stock("GIN", "Preferred", 8, 0.2, 100),
    "JOE": Stock("JOE", "Common", 13, 0, 250)
}

stock_market = StockMarket([], available_stocks)
