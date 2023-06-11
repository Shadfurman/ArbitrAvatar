import requests
import json

def get_bid_ask(pair, exchange):
    if exchange.lower() == 'kraken':
        # convert general pair to Kraken-specific pair (e.g., 'BTCUSD' to 'XXBTZUSD')
        if (pair.upper() == 'BTCUSD'): kraken_pair = 'XXBTZUSD'
        return get_order_book_kraken(kraken_pair)
    elif exchange.lower() == 'bitfinex':
        # convert general pair to Bitfinex-specific pair (e.g., 'BTCUSD' to 'tBTCUSD')
        if (pair.upper() == 'BTCUSD'): bitfinex_pair = 'tBTCUSD'
        return get_order_book_bitfinex(bitfinex_pair)
    else:
        print(f'Exchange {exchange} not supported.')
        return None
    
def get_order_book_kraken(pair):
    url = 'https://api.kraken.com/0/public/Depth'
    params = {
        'pair': pair,
        'count': '1'
    }
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    return float(data['result'][pair]['bids'][0][0]), float(data['result'][pair]['asks'][0][0])

def get_order_book_bitfinex(pair):
    url = f'https://api-pub.bitfinex.com/v2/book/{pair}/P0'
    response = requests.get(url)
    data = json.loads(response.text)

    # In the response data, bids have a negative amount and asks have a positive amount.
    # We'll separate bids and asks, then take the highest bid and the lowest ask.
    bids = [entry for entry in data if entry[2] < 0]
    asks = [entry for entry in data if entry[2] > 0]
    highest_bid = max(bids, key=lambda x: x[0])
    lowest_ask = min(asks, key=lambda x: x[0])

    return highest_bid[0], lowest_ask[0]

# get the order book for the BTC/USD pair on Kraken
highest_bid, lowest_ask = get_bid_ask('BTCUSD', 'Kraken')
print("Highest bid:", highest_bid)
print("Lowest ask:", lowest_ask)

# get the order book for the BTC/USD pair on Bitfinex
highest_bid, lowest_ask = get_bid_ask('BTCUSD', 'Bitfinex')
print("Highest bid:", highest_bid)
print("Lowest ask:", lowest_ask)