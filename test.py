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

def add(exchange, id, symbol, dir, price, size):
    write_to_exchange(exchange, {"type": "add", "order_id": id, "symbol": symbol, "dir": dir, "price": price, "size": size})

def convert(exchange, id, symbol, dir, size):
    write_to_exchange(exchange, {"type": "convert", "order_id": id, "symbol": symbol, "dir": dir, "size": size})

def cancel(exchange, id):
    write_to_exchange(exchange, {"type": "cancel", "order_id": id})


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
    while True:
        x = read_from_exchange(exchange)
        print(x)

        if(x['type'] == "book"):
            price = update_current_price(log, x['symbol'], x['buy'], x['sell'])

        
        if(x['type'] == "book" and x['symbol'] == "GOOG"):
            fair_val_goog = log.price_dict["GOOG"]
            buy = x['buy']
            sell = x['sell']
            if(len(sell) != 0 and len(buy) != 0 ):
                if(fair_val_goog - buy[0][0] > sell[0][0] - fair_val_goog):
                    add(exchange, random.randint(0, 2**32), "GOOG", "BUY", buy[0][0], buy[0][1])
                else:
                    add(exchange, random.randint(0, 2**32), "GOOG", "SELL", sell[0][0], sell[0][1])

        #print("PRICE: "+str(log.price_dict["GOOG"]))
        


if __name__ == "__main__":
    main()
