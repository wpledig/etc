
import random


def trade_ETF(exchange, buy, sell, log, add, convert):
    fairprice = 3 * log.price_dict['BOND']  + 2 * log.price_dict['AAPL'] + 3 * log.price_dict['MSFT'] + 2 * log.price_dict['GOOG']
    if(len(sell) > 0 and sell[0][0] + 100 < fairprice):
        sell_best = sell[0]
        price = sell_best[0]
        size = min(sell_best[1], log.max_buy("XLK"))

        add(exchange, random.randint(0, 2**32), "XLK", "BUY", price, size)

        convert(exchange, random.randint(0, 2**32), "XLK", "BUY", size)

        add(exchange, random.randint(0, 2**32), "BOND", "SELL", log.price_dict['BOND'], min(3 * size, log.max_sell("BOND")))
        add(exchange, random.randint(0, 2**32), "AAPL", "SELL", log.price_dict['AAPL'], min(2 * size, log.max_sell("AAPL")))
        add(exchange, random.randint(0, 2**32), "MSFT", "SELL", log.price_dict['MSFT'], min(3 * size, log.max_sell("MSFT")))
        add(exchange, random.randint(0, 2**32), "GOOG", "SELL", log.price_dict['GOOG'], min(2 * size, log.max_sell("GOOG")))
