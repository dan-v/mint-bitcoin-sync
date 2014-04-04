import requests
import logging


def get_bitcoin_current_price_usd():
    price_url = 'http://blockchain.info/q/24hrprice'
    logging.info("Getting current bitcoin price from {}".format(price_url))

    price_request = requests.get(price_url)
    if price_request.status_code != requests.codes.ok:
        raise Exception("Failed to get price from URL '{}'. Error: {}".format(price_url, price_request.text))
    if not price_request.text:
        raise Exception("No price could be retrieved from URL '{}'".format(price_url))

    try:
        current_price = float(price_request.text)
    except:
        raise Exception("Failed to convert price '{}' to float".format(price_request.text))

    logging.info("Using retrieved BTC price: ${:.2f}".format(current_price))
    return current_price


def get_bitcoin_current_address_balance(public_address):
    balance_url = 'http://blockchain.info/q/addressbalance'
    logging.info("Getting current bitcoin balance from {}".format(balance_url))

    balance_url_with_address = '{}/{}'.format(balance_url, public_address)
    balance_request = requests.get(balance_url_with_address)
    if balance_request.status_code != requests.codes.ok:
        raise Exception("Failed to get balance from URL '{}'. Error: {}".format(balance_url_with_address,
                                                                                balance_request.text))
    if not balance_request.text:
        raise Exception("No balance could be retrieved from URL '{}'".format(balance_url_with_address))

    try:
        balance = float(balance_request.text) / 100000000.00000000
    except:
        raise Exception("Failed to convert balance '{}' to float".format(public_address))

    logging.info("Bitcoin address '{}' has {:.8f} BTC".format(public_address, balance))
    return balance