import time
import random

def price(sell):
    min_price = 0
    count = 0
    for x in sell: 
        sell_price = x[0]
        sell_size = x[1]
        count+=sell_size
        min_price+=sell_price*sell_size
        if(count >= 10):
            return min_price
    return float('inf')


def trade_ETF2(exchange, buy, sell, log, add, convert):
    fairprice = 3 * log.price_dict['BOND']  + 2 * log.price_dict['AAPL'] + 3 * log.price_dict['MSFT'] + 2 * log.price_dict['GOOG']
    sell_price = price(sell)
    if(sell_price + 100 < fairprice):
        size = min(10, log.max_buy("XLK"))
        add(exchange, random.randint(0, 2**32), "XLK", "BUY", price, size)
        randint = random.randint(0, 2**32)
        #print(randint, size, log.book_dict["XLK"], log.max_sell("XLK"))
        convert_size = (int(log.book_dict["XLK"])/10)*10
        convert(exchange, randint, "XLK", "SELL", convert_size)

        add(exchange, random.randint(0, 2**32), "BOND", "SELL", log.price_dict['BOND'], min(3 * convert_size/10, log.max_sell("BOND")))
        add(exchange, random.randint(0, 2**32), "AAPL", "SELL", log.price_dict['AAPL'], min(2 * convert_size/10, log.max_sell("AAPL")))
        add(exchange, random.randint(0, 2**32), "MSFT", "SELL", log.price_dict['MSFT'], min(3 * convert_size/10, log.max_sell("MSFT")))
        add(exchange, random.randint(0, 2**32), "GOOG", "SELL", log.price_dict['GOOG'], min(2 * convert_size/10, log.max_sell("GOOG")))


def trade_ETF(exchange, buy, sell, log, add, convert):
    fairprice = 3 * log.price_dict['BOND']  + 2 * log.price_dict['AAPL'] + 3 * log.price_dict['MSFT'] + 2 * log.price_dict['GOOG']
    if(len(sell) > 0 and sell[0][0] + 10 > fairprice/10):
        price = sell[0][0]
        size = min(sell[0][1], log.max_buy("XLK"))

        add(exchange, random.randint(0, 2**32), "XLK", "BUY", price, size)
        convert_size = max(10, (log.book_dict["XLK"]/10)*10)
        convert(exchange, random.randint(0, 2**32), "XLK", "SELL", convert_size)

        #add(exchange, random.randint(0, 2**32), "BOND", "SELL", log.price_dict['BOND'], min(3 * convert_size/10, log.max_sell("BOND")))
        add(exchange, random.randint(0, 2**32), "AAPL", "SELL", log.price_dict['AAPL'], min(2 * convert_size/10, log.max_sell("AAPL")))
        add(exchange, random.randint(0, 2**32), "MSFT", "SELL", log.price_dict['MSFT'], min(3 * convert_size/10, log.max_sell("MSFT")))
        add(exchange, random.randint(0, 2**32), "GOOG", "SELL", log.price_dict['GOOG'], min(2 * convert_size/10, log.max_sell("GOOG")))






