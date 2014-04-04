# mint-bitcoin-sync
A python script that will update Mint.com with current value of Bitcoins in specified bitcoin addresses. Uses
Blockchain.info API to get price over past 24 hours. Note that there is no public Mint.com API, so this is
using "private" API calls that may break at any point.

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
2014-04-03 21:49:19,924 INFO   line 171  Starting new HTTP connection (1): blockchain.info
2014-04-03 21:49:20,386 INFO   line 153  Bitcoin address 'xxxxxxxxxxxxxxxxxxxxx1' has x.xx BTC
2014-04-03 21:49:20,389 INFO   line 171  Starting new HTTP connection (1): blockchain.info
2014-04-03 21:49:20,718 INFO   line 153  Bitcoin address 'xxxxxxxxxxxxxxxxxxxxx2' has x.xx BTC
2014-04-03 21:49:20,721 INFO   line 171  Starting new HTTP connection (1): blockchain.info
2014-04-03 21:49:21,083 INFO   line 134  Using BTC price: $xxx.xx
2014-04-03 21:49:21,083 INFO   line 191  Current combined balance for all addresses: $x.xx

2014-04-03 21:49:21,084 INFO   line 26   Logging into Mint.com
2014-04-03 21:49:21,086 INFO   line 635  Starting new HTTPS connection (1): wwws.mint.com
2014-04-03 21:49:22,034 INFO   line 65   Getting list of accounts
2014-04-03 21:49:22,274 INFO   line 117  Updated account on Mint with current balance: $x.xx
2014-04-03 21:49:22,275 INFO   line 54   Logging out of Mint.com
2014-04-03 21:49:22,317 INFO   line 211  Finished
```