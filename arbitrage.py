import random


def arbitrage_adr(exchange, log, buy, sell, add):
    if(len(sell) == 0):
        return
    fairval = log.price_dict["BABZ"]
    adr_val = sell[0][0]
    if(fairval > adr_val + 10):
        price = sell[0][0]
        size = sell[0][1]
        add(exchange, random.randint(0, 2**32), "BABA", "BUY", price, size)
        convert(exchange, random.randint(0, 2**32), "BABA", "SELL", size)
        add(exchange, random.randint(0, 2**32), "BABZ", "SELL", fairval, size)
