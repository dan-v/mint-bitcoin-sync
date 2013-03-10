mint-bitcoin-sync
=================

Python script that will update mint.com with bitcoin balance at specified address

Python Requirements
===
1. pip install pyquery

Mint.com Requirements
===
1. On Mint.com, a new "Other" account needs to be added for bitcoins 
2. Select 'Money (or Debt)' radio button
3. Pick 'Cash (Positive)' from dropdown and click 'Next' button
4. What would you like to call it? == Bitcoin
5. How much is it worth == 0 (script will update it to correct value)
6. Is this associated with a loan, mortgage, or line of credit == No
7. Click 'Add it!' button

Usage
===
python mint_bitcoin_sync.py "mint.com-login" "mint.com-password" "public-bitcoin-address"
