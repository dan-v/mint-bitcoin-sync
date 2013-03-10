from cookielib import CookieJar, DefaultCookiePolicy
import json
import urllib2, urllib
import locale
from pyquery import PyQuery as pq

def enable_cookies():
    cj = CookieJar(DefaultCookiePolicy(rfc2965=True))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

def url_get(url, postVars=None):
    try:
        con = urllib2.urlopen(url, postVars)
    except Exception:
        result = None
    else:
        result = con.read()

    return result

def url_post(url, varDict):
    return url_get(url, urllib.urlencode(varDict))

def mint_login(email, password):
    enable_cookies()
    # login
    post_args = {"username": email, "password": password, "task": "L", "nextPage": ""}
    response = url_post("https://wwws.mint.com/loginUserSubmit.xevent", post_args)
    if "javascript-token" not in response.lower():
        raise Exception("Mint.com login failed")

    # grab token
    d = pq(response)
    token = d("input#javascript-token")[0].value

    return token

def get_bitcoin_account_id_from_mint(token):
    # issue service request
    request_id = "115485" # magic number? random number?
    post_args = {"input": json.dumps([
        {"args": {
            "types": [
                "OTHER_PROPERTY"
            ]
        }, 
        "id": request_id, 
        "service": "MintAccountService", 
        "task": "getAccountsSorted"}
    ])}
    json_response = url_post("https://wwws.mint.com/bundledServiceController.xevent?token="+token, post_args)
    response = json.loads(json_response)["response"]

    # turn into correct format
    accounts = response[request_id]["response"]
    for account in accounts:
        if account["name"] == "Bitcoin":
            return account["id"]

    raise Exception("Failed to find a mint account named Bitcoin")

def get_bitcoin_total_usd(addresses):
    # Get total bitcoins at address
    bitcoin_total = 0.00000000
    for address in addresses.split(","):
        con = urllib2.urlopen('http://blockchain.info/q/addressbalance/%s' % address)
        bitcoins_satoshis = con.read()
        if not bitcoins_satoshis:
            raise Exception("Failed to get address balance for address %s" % address)
        bitcoins = float(bitcoins_satoshis) / 100000000.00000000
        bitcoin_total += bitcoins
        print "Bitcoin address '%s' has %.8f BTC" % (address, bitcoins)
    print "\nTotal bitcoins for all addresses: %.8f BTC" % bitcoin_total

    # Get 24 hour price in USD
    con = urllib2.urlopen('http://blockchain.info/q/24hrprice')
    price = con.read()
    if not price:
        raise Exception("Failed to get 24 hour price")
    print "Using 24 hour price: %s USD" % price
    price = float(price)

    # Determine current balance
    total = bitcoin_total * price
    print "Current combined balance for all addresses: %s\n" % (format_usd(total))
    
    return total

def format_usd(amount):
    # Format total
    locale.setlocale( locale.LC_ALL, '' )
    formatted_amount= locale.currency(amount, grouping=True)
    return formatted_amount

def update_bitcoin_account_on_mint(token, account_id, amount):
    # update bitcoin amount
    formatted_amount = format_usd(amount)
    post_args = {"accountId": account_id, "types": "ot", "accountName": "Bitcoin", "accountValue": formatted_amount, "associatedLoanRadio": "No", "accountType": "3",  "accountStatus": "1",  "token": token}
    response = url_post("https://wwws.mint.com/updateAccount.xevent", post_args)
    print "Updated Bitcoin account on mint with current balance: %s" % (formatted_amount)
    return response

if __name__ == "__main__":
    import getpass, sys

    if len(sys.argv) >= 4:
        email, password, bitcoin_addresses = sys.argv[1:]
    else:
        bitcoin_addresses = raw_input("Bitcoin addresses: ")
        email = raw_input("Mint email: ")
        password = getpass.getpass("Password: ")

    total = get_bitcoin_total_usd(bitcoin_addresses) 
    input = raw_input("Press any key to update Mint with these details\n")
    login_token = mint_login(email, password)
    bitcoin_account_id = get_bitcoin_account_id_from_mint(login_token)
    update_response = update_bitcoin_account_on_mint(login_token, bitcoin_account_id, total)
