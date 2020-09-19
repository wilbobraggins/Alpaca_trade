import alpaca_trade_api as tradeapi
import requests
import json
from config import *
import pandas as pd
import csv


BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
HEADERS = {"APCA-API-KEY-ID": API_KEY, "APCA-API-SECRET-KEY": SECRET_KEY}
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITIONS_URL = "{}/v2/positions".format(BASE_URL)
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)



def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)


def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(r.content)


def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)


def get_position(sym):
    r = requests.get(POSITIONS_URL, {"sym": sym}, headers=HEADERS)

    return json.loads(r.content)

#response = create_order("AAPL", 100, "buy", "market", "gtc")
#orders = get_orders()
#account = get_account()


def get_SP500():
    table = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    df.to_csv('S&P500-Info.csv')
    df.to_csv("S&P500-Symbols.csv", columns=['Symbol'])

def check_symbol():
    file = csv.reader(open('S&P500-Symbols.csv'), delimiter=',')
    included_cols = [1]
    for row in file:
        symbol = list(row[i] for i in included_cols)   
        yield symbol

out_str = " "
for value in check_symbol():
    symbol = out_str.join(value)
    print(api.get_aggs(symbol=symbol, timespan="day", multiplier=1, _from="2020-09-17", to="2020-09-18"))