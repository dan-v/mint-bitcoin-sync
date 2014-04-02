import json
import requests
import locale
import argparse
import getpass


class Mint:
    START_URL = 'https://wwws.mint.com/login.event?task=L'
    PRELOGIN_URL = 'https://wwws.mint.com/getUserPod.xevent'
    LOGIN_URL = 'https://wwws.mint.com/loginUserSubmit.xevent'
    LOGOUT_URL = 'https://wwws.mint.com/bundledServiceController.xevent?token=undefined'
    ACCOUNTS_URL = 'https://wwws.mint.com/bundledServiceController.xevent?token='
    ACCOUNTS_UPDATE_URL = 'https://wwws.mint.com/updateAccount.xevent'
    MAGIC_REQUEST_ID = '115484'  # Not sure what this value actually is
    HTTP_HEADERS = {"accept": "application/json"}

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None
        self.session = requests.Session()

    def login(self):
        print("Logging into Mint.com")
        # Go to main page
        start = self.session.get(Mint.START_URL)
        if start.status_code != requests.codes.ok:
            raise Exception("Failed to load Mint main page '%s'" % Mint.START_URL)

        # Send pre-login post?
        pre_login_data = {"username": self.email}
        pre_login = self.session.post(Mint.PRELOGIN_URL, data=pre_login_data)
        if pre_login.status_code != requests.codes.ok:
            raise Exception("Failed to post to Mint pre-login URL '%s'" % Mint.PRELOGIN_URL)

        # Post to login URL
        login_data = {"username": self.email, "password": self.password, "task": "L", "browser": "firefox",
                "browserVersion": "27", "os": "linux"}
        login = self.session.post(Mint.LOGIN_URL, data=login_data, headers=Mint.HTTP_HEADERS)
        if login.status_code != requests.codes.ok:
            raise Exception("Failed to login to Mint URL '%s'" % Mint.LOGIN_URL)

        # Get token and set
        if "token" not in login.text:
            raise Exception("Mint.com login failed[1]")
        login_json = (login.json())
        if not login_json["sUser"]["token"]:
            raise Exception("Mint.com login failed[2]")
        self.token = login_json["sUser"]["token"]

    def logout(self):
        print("Logging out of Mint.com")
        self.token = None
        try:
            self.session.post(Mint.LOGOUT_URL)
        except:
            pass

    def get_accounts(self):
        if not self.token:
            raise Exception("Can only get Mint accounts when logged in. Please login first.")

        print("Getting list of accounts")

        data = {"input": json.dumps([
                {"args": {
                    "types": [
                        "BANK",
                        "CREDIT",
                        "INVESTMENT",
                        "LOAN",
                        "MORTGAGE",
                        "OTHER_PROPERTY",
                        "REAL_ESTATE",
                        "VEHICLE",
                        "UNCLASSIFIED"
                    ]
                },
                "id": Mint.MAGIC_REQUEST_ID,
                "service": "MintAccountService",
                "task": "getAccountsSorted"}
                ])}

        accounts_url_with_token = Mint.ACCOUNTS_URL + self.token
        accounts = self.session.post(accounts_url_with_token, data=data, headers=Mint.HTTP_HEADERS)
        if accounts.status_code != requests.codes.ok:
            raise Exception("Failed to get account data from URL '%s'. Error: %s" % (Mint.ACCOUNTS_URL, accounts.text))

        if Mint.MAGIC_REQUEST_ID not in accounts.text:
            raise Exception("Could not parse account data: " + accounts)
        accounts_json = (accounts.json())
        account_list = accounts_json["response"][Mint.MAGIC_REQUEST_ID]["response"]
        return account_list

    def get_account_id_by_name(self, accounts_list, account_name):
        for account in accounts_list:
            if account["name"] == account_name:
                return account["id"]
        raise Exception("Failed to find a Mint account named %s" % account_name)

    def format_usd(self, amount):
        locale.setlocale(locale.LC_ALL, '')
        formatted_amount = locale.currency(amount, grouping=True)
        return formatted_amount

    def set_account_value(self, account_id, account_value):
        formatted_amount = self.format_usd(account_value)
        data = {"accountId": account_id, "types": "ot", "accountName": "Bitcoin", "accountValue": formatted_amount,
                "accountType": "3",  "accountStatus": "1",  "token": self.token}
        post_request = self.session.post(Mint.ACCOUNTS_UPDATE_URL, data=data)
        if post_request.status_code != requests.codes.ok:
            raise Exception("Failed to set new balance '%s' for Bitcoin account (%s). Error: %s" % (formatted_amount,
                                                                                                    account_id,
                                                                                                    post_request.text))
        print("Updated account on Mint with current balance: %s" % formatted_amount)


class BlockChainInfo:
    BALANCE_URL = 'http://blockchain.info/q/addressbalance'
    PRICE_URL = 'http://blockchain.info/q/24hrprice'

    def __init__(self):
        pass

    @staticmethod
    def get_bitcoin_current_address_balance(public_address):
        try:
            bitcoins_satoshis = requests.get('%s/%s' % (BlockChainInfo.BALANCE_URL, public_address)).text
            bitcoins = float(bitcoins_satoshis) / 100000000.00000000
        except:
            raise Exception("Failed to get balance for address %s" % public_address)

        print("Bitcoin address '%s' has %.8f BTC" % (public_address, bitcoins))
        return bitcoins

    @staticmethod
    def get_bitcoin_current_price_usd():
        try:
            raw_price = requests.get(BlockChainInfo.PRICE_URL).text
            price = float(raw_price)
        except:
            raise Exception("Failed to get price from '%s'" % BlockChainInfo.PRICE_URL)

        print("Using BTC price: $%.2f" % price)
        return price

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Update Mint.com with current value of Bitcoins in specified bitcoin '
                                                 'addresses')

    parser.add_argument('-e', action='store', dest='email',
                        help='Mint.com Email Address', required=True)
    parser.add_argument('-p', action='store', dest='password',
                        help='Mint.com Password (will prompt if not provided)')
    parser.add_argument('-l', action='store', dest='bitcoin_account_label',
                        help='Mint.com Bitcoin account label', required=True)
    parser.add_argument('-a', action='append', default=[], dest='bitcoin_addresses',
                        help='Bitcoin public address (specify multiple -a for more than one)', required=True)

    parser.add_argument('--version', action='version', version='%(prog)s 1.1')

    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass("Mint.com password: ")

    # Get bitcoin balance and price
    bitcoin_balance = 0.00000000
    for address in args.bitcoin_addresses:
        bitcoin_balance += BlockChainInfo.get_bitcoin_current_address_balance(address)
    current_bitcoin_price_usd = BlockChainInfo.get_bitcoin_current_price_usd()

    # Determine current balance
    total_usd = bitcoin_balance * current_bitcoin_price_usd
    print("Current combined balance for all addresses: $%.2f\n" % total_usd)

    # Initialize mint object
    mint = Mint(args.email, args.password)

    # Login
    mint.login()

    # Get all accounts
    mint_accounts = mint.get_accounts()

    # Find Bitcoin account id
    mint_bitcoin_account_id = mint.get_account_id_by_name(mint_accounts, args.bitcoin_account_label)

    # Update mint account id with new balance
    mint.set_account_value(mint_bitcoin_account_id, total_usd)

    # Logout
    mint.logout()

    print("\nFinished")
