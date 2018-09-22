




def trade_ETF(exchange, buy, sell, log, add, convert):
    fairprice = 3 * log.price_dict['BOND']  + 2 * log.price_dict['AAPL'] + 3 * log.price_dict['MSFT'] + 2 * log.price_dict['GOOG']
    if(len(buy) > 0 and buy[0][0] + 100 < fairprice):
        buy_best = buy[0]
        price = buy_best[0]
        size = min(buy_best[1], log.max_buy("XLK"))
        add(exchange, random_id(), "XLK", "BUY", price, size)
        convert(exchange, random_id(), "XLK", "CONVERT", size)
        add(exchange, random_id(), "BOND", "SELL", log.price_dict['BOND'], min(3 * size, log.max_buy("BOND"))
        add(exchange, random_id(), "AAPL", "SELL", log.price_dict['AAPL'], min(2 * size, log.max_buy("AAPL"))
        add(exchange, random_id(), "MSFT", "SELL", log.price_dict['MSFT'], min(3 * size, log.max_buy("MSFT"))
        add(exchange, random_id(), "GOOG", "SELL", log.price_dict['GOOG'], min(2 * size, log.max_buy("GOOG"))
