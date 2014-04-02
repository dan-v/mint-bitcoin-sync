# mint-bitcoin-sync
A python script that will update Mint.com with current value of Bitcoins in specified bitcoin addresses. Uses Blockchain.info API to get price over past 24 hours. Note that there is no public Mint.com API, so this is using "private" API calls that may break at any point.

# Linux Requirements
* Python (2.7+ or 3.x)
* Install requests
<pre>
sudo pip install requests
</pre>

# Windows Requirements
* Install Python 3.4+ so pip is included
* Install requests
<pre>
c:\Python34\Scripts\pip.exe install requests
</pre>

# Mint.com Setup
1. On Mint.com, a new "Other" account needs to be added for Bitcoins 
2. Select 'Money (or Debt)' radio button
3. Pick 'Cash (Positive)' from dropdown and click 'Next' button
4. What would you like to call it? Set it to 'Bitcoin' (or call it whatever you want)
5. How much is it worth? Set it to '1' (script will update it to correct value when run)
6. Is this associated with a loan, mortgage, or line of credit == No
7. Click 'Add it!' button

#Script Usage
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
#Example Output
```
python mint_bitcoin_sync.py -e mintlogin@gmail.com -l Bitcoin -a xxxxxxxxxxxxxxxxxxxxx1 -a xxxxxxxxxxxxxxxxxxxxx2
Mint.com password: 
Bitcoin address 'xxxxxxxxxxxxxxxxxxxxx1' has x.xxxxxxxx BTC
Bitcoin address 'xxxxxxxxxxxxxxxxxxxxx2' has x.xxxxxxxx BTC
Using BTC price: $xxx.xx
Current combined balance for all addresses: $xxx.xx

Logging into Mint.com
Getting list of accounts
Updated account on Mint with current balance: $xxx.xx
Logging out of Mint.com

Finished
```
