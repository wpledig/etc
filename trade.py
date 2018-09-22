#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import random
import time
import tracking
import bonds
import etf
import stdmean
import arbitrage

price_collection = stdmean.PriceCollection()
log = tracking.TrackingBook()
team_name = "Chasers"

# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!

test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty

short = 1
test_exchange_index = 0
prod_exchange_hostname = "production"
USDlimit = 30000

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())

def hello(exchange, name):
    write_to_exchange(exchange, {"type": "hello", "team": name.upper()})
    return read_from_exchange(exchange)

def add(exchange, id, symbol, dir, price, size):
    write_to_exchange(exchange, {"type": "add", "order_id": id, "symbol": symbol, "dir": dir, "price": price, "size": size})
    return read_from_exchange(exchange)

def convert(exchange, id, symbol, dir, size):
    write_to_exchange(exchange, {"type": "convert", "order_id": id, "symbol": symbol, "dir": dir, "size": size})
    return read_from_exchange(exchange)

def cancel(exchange, id):
    write_to_exchange(exchange, {"type": "cancel", "order_id": id})
    return read_from_exchange(exchange)


def update_current_price(log, symbol, buy, sell):
    price = 0
    if(len(buy) == 0 and len(sell) == 0):
        return 0
    elif(len(buy) == 0):
        price = sell[0][0]
    elif(len(sell) == 0):
        price = buy[0][0]
    else:
        price = (buy[0][0] + sell[0][0])/2.0
    log.update_price(symbol, price)
    return price

# ~~~~~============== TRADING  ==============~~~~~


# ~~~~~============== MAIN LOOP ==============~~~~~


def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    pnl = 0
    while True:
        line = read_from_exchange(exchange)
        if(line['type'] == "fill"):
            log.fill(line['symbol'], line['dir'], line['price'], line['size'])
            print(line)
        if(line['type'] == "book"):
            symbol = line['symbol']
            buy = line['buy']
            sell = line['sell']
            if(symbol != "BOND"):
                price = update_current_price(log, symbol, buy, sell)
                if(price != 0):
                    price_collection.add_price(symbol, price, add, exchange, buy, sell)
            if(symbol == "BOND"):
                bonds.trade_bonds(exchange, log, buy, sell, add)

            #if(symbol == "XLK"):
                #etf.trade_ETF(exchange, buy, sell, log, add, convert)

            #if(symbol == "BABA"):
                #arbitrage.arbitrage_adr(exchange, log, buy, sell, add)

        if(log.book_dict["PNL"] != pnl):
            pnl = log.book_dict["PNL"]
            print(log.book_dict)
        #if(line['type'] == 'ack' or line['type'] == 'reject'):
            #print(line)

   
# A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)

if __name__ == "__main__":
    main()
