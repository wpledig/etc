import random
import math

class PriceCollection:
    def __init__(self):
        self.breakpoint = 30
        self.array_dict = {
            "AAPL": [],
            "BABA": [],
            "BABZ": [],
            "BOND": [],
            "GOOG": [],
            "MSFT": [],
            "XLK": [],
        }
    def getSTD(self, symbol):
        lst = self.array_dict[symbol]
        sum_ = 0
        mn = sum(lst)/float(len(lst))
        for i in range(len(lst)):
            sum_ += pow((lst[i]-mn),2)
        return math.sqrt(sum_/float(len(lst)-1))

    def getMean(self, symbol):
        return sum(self.array_dict[symbol])/1.0*len(self.array_dict[symbol])

    def add_price(self, symbol, price, add, exchange, buy, sell):
        self.array_dict[symbol].append(price)
        if symbol == "BABZ" and len(self.array_dict["BABZ"]) > self.breakpoint:
            self.array_dict[symbol].pop(0)
            if price < self.getMean("BABZ") - self.getSTD("BABZ") and len(sell) > 0:
                add(exchange, random.randint(0, 2**32), "BABA", "BUY", sell[0][0], sell[0][1])
            if price > self.getMean("BABZ") + self.getSTD("BABZ") and len(buy) > 0:
                ra = random.randint(0, 2**32)
                print(ra)
                add(exchange, ra, "BABA", "SELL", buy[0][0], buy[0][1])

