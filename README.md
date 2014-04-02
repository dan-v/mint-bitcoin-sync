Python script that will update Mint.com with current Bitcoin USD value of specified bitcoin addresses. Uses Blockchain.info to get price over past 24 hours. Note that there is no Mint.com public API, so this is using "private" API calls that may break at any point.

Mint.com Setup
===
1. On Mint.com, a new "Other" account needs to be added for Bitcoins 
2. Select 'Money (or Debt)' radio button
3. Pick 'Cash (Positive)' from dropdown and click 'Next' button
4. What would you like to call it? Set it to 'Bitcoin' (or call it whatever you want)
5. How much is it worth? Set it to '1' (script will update it to correct value when run)
6. Is this associated with a loan, mortgage, or line of credit == No
7. Click 'Add it!' button

Script Usage
===
<pre>
python mint_bitcoin_sync.py -e <mint-email-address> -p <mint-password> -l <bitcoin-account-text-label> -a <bitcoin-public-address-1> -a <bitcoin-public-address-2>
</pre>