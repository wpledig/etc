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
        self.book_dict = {
            "PNL": 0,
            "AAPL": 0,
            "BABA": 0,
            "BABZ": 0,
            "BOND": 0,
            "GOOG": 0,
            "MSFT": 0,
            "USD": 0,
            "XLK": 0
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

        self.max_dict = {
            "AAPL": 100,
            "BABA": 10,
            "BABZ": 10,
            "BOND": 100,
            "GOOG": 100,
            "MSFT": 100,
            "XLK": 100,
        }

    def compute_pnl(self):
        self.book_dict["PNL"] = self.book_dict["USD"] + sum(map(lambda key: self.book_dict[key] * self.price_dict[key], self.price_dict.keys()))

    def fill(self, symbol, direction, price, size):
        dir = 1
        if direction == "SELL":
            dir = -1
        self.book_dict[symbol] += dir * size
        self.book_dict["USD"] -= dir * price * size
        self.compute_pnl()

    def update_price(self, symbol, price):
        self.price_dict[symbol] = price
        self.compute_pnl()

    def max_buy(self, symbol):
        return self.max_dict[symbol] - self.book_dict[symbol] - 1

    def max_sell(self, symbol):
        return self.max_dict[symbol] + self.book_dict[symbol] - 1

book = TrackingBook()
book.fill("GOOG", "BUY", 100, 100)
book.update_price("GOOG", 100)
print(book.book_dict)
