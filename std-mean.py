import numpy as np
import random

class PriceCollection:
    def __init__(self):
        self.array_dict = {
            "AAPL": np.array([]),
            "BABA": np.array([]),
            "BABZ": np.array([]),
            "BOND": np.array([]),
            "GOOG": np.array([]),
            "MSFT": np.array([]),
            "XLK": np.array([])
        }
    def getSTD(self, symbol):
        return np.std(self.array_dict[symbol])
    def getMean(self, symbol):
        return np.mean(self.array_dict[symbol])

    def add_price(self, symbol, price, add, exchange, buy, sell):
        self.array_dict[symbol].append([price])
        if symbol == "BABZ" and self.array_dict["BABZ"].size > 30:
            if price < self.getMean("BABZ") - self.getSTD("BABZ"):
                add(exchange, random.randint(0, 2**32), "BABA", "BUY", sell[0][0], sell[0][1])
            if price > self.getMean("BABZ") + self.getSTD("BABZ"):
                add(exchange, random.randint(0, 2**32), "BABA", "SELL", buy[0][0], buy[0][1])
