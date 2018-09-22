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

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!

team_name = "Chasers"

# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!

test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty

positions = 0
test_exchange_index = 2
prod_exchange_hostname = "production"

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

# ~~~~~============== TRADING  ==============~~~~~

def random_id():
    return random.randint(0, 2**32)

def trade_bonds(exchange):
    while True:
        order = read_from_exchange(exchange)
        if(line['type'] == "book" and line['symbol'] == "BOND"):
            buy = line['buy']
            sell = line['sell']
            buy_best = buy[0]
            sell_best = sell[0]
            if(buy_best[0] < 1000):
                price = buy_best[0][0]
                size = buy_best[0][1]
                return_val = add(exchange, random_id(), "BOND", "BUY", price, size)

            if(sell_best[0] < 1000):
                price = sell_best[0][0]
                #size = min(positions, sell_best[0][1])
                size = sell_best[0][1]
                return_val = add(exchange, random_id(), "BOND", "SELL", price, size)
        print("\n\nOUTPUT: "+return_val+"\n\n")

# ~~~~~============== MAIN LOOP ==============~~~~~

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)

if __name__ == "__main__":
    main()
