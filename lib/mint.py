import logging
import requests
import json


class Mint:
    START_URL = 'https://wwws.mint.com/login.event?task=L'
    LOGIN_URL = 'https://wwws.mint.com/loginUserSubmit.xevent'
    LOGOUT_URL = 'https://wwws.mint.com/bundledServiceController.xevent?token=undefined'
    ACCOUNTS_URL = 'https://wwws.mint.com/bundledServiceController.xevent?token='
    ACCOUNTS_UPDATE_URL = 'https://wwws.mint.com/updateAccount.xevent'
    MAGIC_REQUEST_ID = '115484'  # Random request id to use for HTTP Posts
    HTTP_HEADERS = {"accept": "application/json"}

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None
        self.session = requests.Session()

    def login(self):
        logging.info("Logging into Mint.com")

        # Go to main page
        start = self.session.get(Mint.START_URL)
        if start.status_code != requests.codes.ok:
            raise Exception("Failed to load Mint main page '{}'".format(Mint.START_URL))

        # Post to login URL
        login_data = {"username": self.email, "password": self.password, "task": "L", "browser": "firefox",
                        "browserVersion": "27", "os": "linux"}
        login = self.session.post(Mint.LOGIN_URL, data=login_data, headers=Mint.HTTP_HEADERS)
        if login.status_code != requests.codes.ok:
            raise Exception("Failed to login to Mint URL '{}'".format(Mint.LOGIN_URL))

        # Get token and set
        if "token" not in login.text:
            raise Exception("Mint.com login failed[1]")
        login_json = (login.json())
        if not login_json["sUser"]["token"]:
            raise Exception("Mint.com login failed[2]")

        self.token = login_json["sUser"]["token"]

    def logout(self):
        logging.info("Logging out of Mint.com")
        self.token = None
        try:
            self.session.post(Mint.LOGOUT_URL)
        except:
            pass

    def get_accounts(self):
        if not self.token:
            raise Exception("Can only get Mint accounts when logged in. Please login first.")

        logging.info("Getting list of accounts")

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

        # Post to get accounts
        accounts_url_with_token = Mint.ACCOUNTS_URL + self.token
        accounts = self.session.post(accounts_url_with_token, data=data, headers=Mint.HTTP_HEADERS)
        if accounts.status_code != requests.codes.ok:
            raise Exception("Failed to get account data from URL '{}'. Error: {}".format(Mint.ACCOUNTS_URL,
                                                                                         accounts.text))
        if Mint.MAGIC_REQUEST_ID not in accounts.text:
            raise Exception("Could not parse account data: " + accounts)

        # Extract account list
        accounts_json = (accounts.json())
        account_list = accounts_json["response"][Mint.MAGIC_REQUEST_ID]["response"]
        return account_list

    def get_account_id_by_name(self, accounts_list, account_name):
        for account in accounts_list:
            if account["name"] == account_name:
                return account["id"]
        raise Exception("Failed to find a Mint account named {}".format(account_name))

    def set_account_value(self, account_id, label, account_value):
        # Post to set value of account
        data = {"accountId": account_id, "types": "ot", "accountName": label, "accountValue": account_value,
                "accountType": "3",  "accountStatus": "1",  "token": self.token}
        post_request = self.session.post(Mint.ACCOUNTS_UPDATE_URL, data=data)
        if post_request.status_code != requests.codes.ok:
            raise Exception("Failed to set new balance '{}' for Bitcoin account ({}). Error: {}"
                            .format(account_value, account_id, post_request.text))

        logging.info("Updated account on Mint with current balance: {}".format(account_value))
