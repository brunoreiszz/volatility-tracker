# use for environment variables
import os
# needed for the binance API and websockets
from binance.client import Client
# used for dates
from datetime import datetime, timedelta
import time
# used to repeatedly execute the code
from itertools import count
# used to store trades and sell assets
import json


# Switch between testnet and mainnet
# Setting this to False will use REAL funds, use at your own risk
# Define your API keys below in order for the toggle to work
TESTNET = True
# Get binance key and secret for TEST and MAINNET
# The keys below are pulled from environment variables using os.getenv
# Simply remove this and use the following format instead: api_key_test = ‘YOUR_API_KEY’
api_key_test = os.getenv('binance_api_stalkbot_testnet')
api_secret_test = os.getenv('‘binance_secret_stalkbot_testnet’')
api_key_live = os.getenv('‘binance_api_stalkbot_live’')
api_secret_live = os.getenv('‘binance_secret_stalkbot_live’')
# Authenticate with the client
if TESTNET:
 client = Client(api_key_test, api_secret_test)
# The API URL needs to be manually changed in the library to work on the TESTNET
 client.API_URL = '‘https://testnet.binance.vision/api''
else:
 client = Client(api_key_live, api_secret_live)

 #CHANGE THIS API KEYS :)
# select what to pair the coins to and pull all coins paied with PAIR_WITH
PAIR_WITH = '‘USDT’'
# Define the size of each trade, by default in USDT
QUANTITY = 100
# List of pairs to exlcude
# by default we’re excluding the most popular fiat pairs
# and some margin keywords, as we’re only working on the SPOT account
FIATS = ['‘EURUSDT’', '‘GBPUSDT’', '‘JPYUSDT’', '‘USDUSDT’', ‘DOWN’, ‘UP’]
# the amount of time in MINUTES to calculate the differnce from the current price
TIME_DIFFERENCE = 5
# the difference in % between the first and second checks for the price, by default set at 10 minutes apart.
CHANGE_IN_PRICE = 3
# define in % when to sell a coin that’s not making a profit
STOP_LOSS = 3
# define in % when to take profit on a profitable coin
TAKE_PROFIT = 6

def get_price():
 ‘’’Return the current price for all coins on binance’’’
initial_price = {}
 prices = client.get_all_tickers()
for coin in prices:
# only Return USDT pairs and exlcude margin symbols like BTCDOWNUSDT
 if PAIR_WITH in coin[‘symbol’] and all(item not in coin[‘symbol’] for item in FIATS):
 initial_price[coin[‘symbol’]] = { ‘price’: coin[‘price’], ‘time’: datetime.now()}
return initial_price

def wait_for_price():
 ‘’’calls the initial price and ensures the correct amount of time has passed
 before reading the current price again’’’
volatile_coins = {}
 initial_price = get_price()
while initial_price[‘BNBUSDT’][‘time’] > datetime.now() — timedelta(minutes=TIME_DIFFERENCE):
 print(f’not enough time has passed yet…’)
# let’s wait here until the time passess…
 time.sleep(60*TIME_DIFFERENCE)
else:
 last_price = get_price()
# calculate the difference between the first and last price reads
 for coin in initial_price:
 threshold_check = (float(initial_price[coin][‘price’]) — float(last_price[coin][‘price’])) / float(last_price[coin][‘price’]) * 100
# each coin with higher gains than our CHANGE_IN_PRICE is added to the volatile_coins dict
 if threshold_check > CHANGE_IN_PRICE:
 volatile_coins[coin] = threshold_check
 volatile_coins[coin] = round(volatile_coins[coin], 3)
print(f’{coin} has gained {volatile_coins[coin]}% in the last {TIME_DIFFERENCE} minutes, calculating volume in {PAIR_WITH}’)
if len(volatile_coins) < 1:
 print(f’No coins moved more than {CHANGE_IN_PRICE}% in the last {TIME_DIFFERENCE} minute(s)’)
return volatile_coins, len(volatile_coins), last_price