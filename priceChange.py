import websocket, json, pprint, talib
import numpy as np
import tulipy as ti
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ldousdt@kline_1m"


closes = np.array([])
variation = 0.00001

client = Client(config.API_KEY, config.API_SECRET, testnet=True)

def on_open(ws):
    print("Connection open")

def on_close(ws):
    print("Connection closed")

def on_message(ws, message):
    global change, closes, variation

    # global price_on_buy
    
    # print("Received message")
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    candle = json_message['k']
    isCandleClosed = candle['x']
    price = candle['c']


    if isCandleClosed:
        print(price)
        np.append(closes,price)
        print(closes)

        if closes.size > 2:
            np.delete(closes,0)
            print(closes)
            # B  - A / A * 100
            change = (float(closes[1]) - float(closes[0])) / float(closes[0])
            print(closes)
            print(change * 100)
            
            if change > variation:
                print("ALEEEEERTTT! Percent change of " + (change * 100) + "%")
            elif change < variation:
                print("Smaller")
            else:
                print("HEEYYY wtf is going on")
        else:
            pass
    else:
        pass

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
print(client.get_account())
ws.run_forever()



