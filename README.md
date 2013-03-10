mint-bitcoin-sync
=================

Python script that will update mint.com with bitcoin balance of a specified bitcoin address

Linux Requirements
===
* pip install pyquery

Windows Requirements
===
* Need to install Python 2.7 (http://www.python.org/getit/)
* Install distribute from prebuilt binary (http://www.lfd.uci.edu/~gohlke/pythonlibs/#distribute)
* Install pip from prebuilt binary (http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip)
* Install lxml from prebuilt binary (http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)
* c:\Python27\Scripts\pip.exe install pyquery

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
