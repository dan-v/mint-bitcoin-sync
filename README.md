mint-bitcoin-sync
=================

Python script that will update mint.com with bitcoin balance at specified address

Requirements
===
1. pip install pyquery
2. On Mint.com, a new "Other" account needs to be added for bitcoins 
 a. Select 'Money (or Debt)' radio button
 b. Pick 'Cash (Positive)' from dropdown and click 'Next' button
 c. What would you like to call it? == Bitcoin
 d. How much is it worth == 0 (script will update it to correct value)
 e. Is this associated with a loan, mortgage, or line of credit == No
 f. Click 'Add it!' button

Usage
===
python mint_bitcoin_sync.py "mint.com-login" "mint.com-password" "public-bitcoin-address"
