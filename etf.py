import time
import random


def trade_ETF(exchange, buy, sell, log, add, convert):
    fairprice = 3 * log.price_dict['BOND']  + 2 * log.price_dict['AAPL'] + 3 * log.price_dict['MSFT'] + 2 * log.price_dict['GOOG']
    
    if(len(sell) > 0 and sell[0][0] + 100 < fairprice):
        sell_best = sell[0]
        price = sell_best[0]
        size = min(sell_best[1], log.max_buy("XLK"))
        add(exchange, random.randint(0, 2**32), "XLK", "BUY", price, size)
        randint = random.randint(0, 2**32)
        print(randint, size, log.book_dict["XLK"], log.max_sell("XLK"))
        convert(exchange, randint, "XLK", "SELL", min(log.max_sell("XLK"), size))
        #time.sleep(0.1)
        #add(exchange, random.randint(0, 2**32), "BOND", "SELL", log.price_dict['BOND'], min(3 * size, log.max_sell("BOND")))
        #time.sleep(0.1)
        #add(exchange, random.randint(0, 2**32), "AAPL", "SELL", log.price_dict['AAPL'], min(2 * size, log.max_sell("AAPL")))
        #time.sleep(0.1)
        #add(exchange, random.randint(0, 2**32), "MSFT", "SELL", log.price_dict['MSFT'], min(3 * size, log.max_sell("MSFT")))
        #time.sleep(0.1)
        #add(exchange, random.randint(0, 2**32), "GOOG", "SELL", log.price_dict['GOOG'], min(2 * size, log.max_sell("GOOG")))
