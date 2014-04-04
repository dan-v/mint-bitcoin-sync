# mint-bitcoin-sync
A python script that will update Mint.com with current value of Bitcoins in specified bitcoin addresses. Uses
Blockchain.info API to get price over past 24 hours. Note that there is no public Mint.com API, so this is using
"private" API calls that may break at any point.

# Requirements
* Python 2.7 or 3.x, requests
<pre>
pip install requests
</pre>

# Mint.com Setup
1. On Mint.com, a new "Other" account needs to be added for Bitcoins 
2. Select 'Money (or Debt)' radio button
3. Pick 'Cash (Positive)' from dropdown and click 'Next' button
4. What would you like to call it? Set it to 'Bitcoin' (or call it whatever you want)
5. How much is it worth? Set it to '1' (script will update it to correct value when run)
6. Is this associated with a loan, mortgage, or line of credit == No
7. Click 'Add it!' button

#Usage
```
usage: mint_bitcoin_sync.py [-h] -e EMAIL [-p PASSWORD] -l
                            BITCOIN_ACCOUNT_LABEL -a BITCOIN_ADDRESSES
                            [--version]

Update Mint.com with current value of Bitcoins in specified bitcoin addresses

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL              Mint.com Email Address
  -p PASSWORD           Mint.com Password (will prompt if not provided)
  -l BITCOIN_ACCOUNT_LABEL
                        Mint.com Bitcoin account label
  -a BITCOIN_ADDRESSES  Bitcoin public address (specify multiple -a for more
                        than one)
  --version             show program's version number and exit

```
#Example
```
python mint_bitcoin_sync.py -e mintlogin@gmail.com -l Bitcoin -a xxxxxxxxxxxxxxxxxxxxx1 -a xxxxxxxxxxxxxxxxxxxxx2
Mint.com password:
2014-04-03 23:43:07,199 INFO   line 26   Getting current bitcoin balance from http://blockchain.info/q/addressbalance
2014-04-03 23:43:07,211 INFO   line 171  Starting new HTTP connection (1): blockchain.info
2014-04-03 23:43:07,664 INFO   line 41   Bitcoin address 'xxxxxxxxxxxxxxxxxxxxx1' has x.xx BTC
2014-04-03 23:43:07,665 INFO   line 26   Getting current bitcoin balance from http://blockchain.info/q/addressbalance
2014-04-03 23:43:07,668 INFO   line 171  Starting new HTTP connection (1): blockchain.info
2014-04-03 23:43:08,051 INFO   line 41   Bitcoin address 'xxxxxxxxxxxxxxxxxxxxx2' has x.xx BTC
2014-04-03 23:43:08,051 INFO   line 7    Getting current bitcoin price from http://blockchain.info/q/24hrprice
2014-04-03 23:43:08,054 INFO   line 171  Starting new HTTP connection (1): blockchain.info
2014-04-03 23:43:08,246 INFO   line 20   Using retrieved BTC price: $xxx.xx
2014-04-03 23:43:08,247 INFO   line 44   Current combined balance for all addresses: $x.xx

2014-04-03 23:43:08,248 INFO   line 22   Logging into Mint.com
2014-04-03 23:43:08,250 INFO   line 635  Starting new HTTPS connection (1): wwws.mint.com
2014-04-03 23:43:09,626 INFO   line 57   Getting list of accounts
2014-04-03 23:43:09,887 INFO   line 107  Updated account on Mint with current balance: $x.xx
2014-04-03 23:43:09,888 INFO   line 46   Logging out of Mint.com
2014-04-03 23:43:09,940 INFO   line 64   Finished
```