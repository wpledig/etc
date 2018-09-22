"""
class OrderBook:
    def __init__(self):
        self.buys = {}
        with open("buys.txt") as file_buys:
            for buy in file_buys:
                 buy.split()
        self.sells = {}
        with open("sells.txt") as file_sells:
            for sell in file_sells:
                 sell.split()
    def add(self, type, symbol, price, amount):
        if self == "buys"
"""

class TrackingBook:
    def __init__(self):
        self.pnl = 0
        self.aapl = 0
        self.baba = 0
        self.babz = 0
        self.bond = 0
        self.goog = 0
        self.msft = 0
        self.usd = 0
        self.xlk = 0
        self.book_dict = {
            "PNL": self.pnl,
            "AAPL": self.aapl,
            "BABA": self.baba,
            "BABZ": self.babz,
            "BOND": self.bond,
            "GOOG": self.goog,
            "MSFT": self.msft,
            "USD": self.usd,
            "XLK": self.xlk
        }
        self.price_dict = {
            "AAPL": 0,
            "BABA": 0,
            "BABZ": 0,
            "BOND": 1000,
            "GOOG": 0,
            "MSFT": 0,
            "XLK": 0,
        }

    def compute_pnl(self):
        self.pnl = self.usd + sum(map(lambda key: self.book_dict[key] * self.price_dict[key], self.price_dict.keys()))

    def fill(self, symbol, direction, price, size):
        dir = 1
        if direction == "SELL":
            dir = -1
        self.book_dict[symbol] += dir * size
        self.usd -= dir * price

    def update_price(self, symbol, price):
        self.price_dict[symbol] = price
