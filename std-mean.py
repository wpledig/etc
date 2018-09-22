import random

class PriceCollection:
    def __init__(self):
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
        sum = 0
        mn = mean(lst)
        for i in range(len(lst)):
            sum += pow((lst[i]-mn),2)
        return sqrt(sum/len(lst)-1)

    def getMean(self, symbol):
        return sum(self.array_dict[symbol])/float(len(self.array_dict[symbol]))

    def add_price(self, symbol, price, add, exchange, buy, sell):
        self.array_dict[symbol].append([price])
        if symbol == "BABZ" and self.array_dict["BABZ"].size > 30:
            if price < self.getMean("BABZ") - self.getSTD("BABZ"):
                add(exchange, random.randint(0, 2**32), "BABA", "BUY", sell[0][0], sell[0][1])
            if price > self.getMean("BABZ") + self.getSTD("BABZ"):
                add(exchange, random.randint(0, 2**32), "BABA", "SELL", buy[0][0], buy[0][1])
