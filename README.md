mint-bitcoin-sync
=================

Python script that will update mint.com with current bitcoin value in USD of specified bitcoin addresses

Linux Requirements
===
<pre>
sudo pip install pyquery
</pre>

Mac OSX Requirements
===
<pre>
sudo easy_install pip
export CC='/usr/bin/gcc'
sudo -E pip install pyquery
</pre>

Windows Requirements
===
* Need to install Python 2.7 (http://www.python.org/)
* Install distribute from prebuilt binary (http://www.lfd.uci.edu/~gohlke/pythonlibs/#distribute)
* Install pip from prebuilt binary (http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip)
* Install lxml from prebuilt binary (http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)
* Open command prompt and run: 
<pre>
c:\Python27\Scripts\pip.exe install pyquery
</pre>

Mint.com Setup
===
1. On Mint.com, a new "Other" account needs to be added for bitcoins 
2. Select 'Money (or Debt)' radio button
3. Pick 'Cash (Positive)' from dropdown and click 'Next' button
4. What would you like to call it? Set it to 'Bitcoin'
5. How much is it worth? Set it to '1' (script will update it to correct value when run)
6. Is this associated with a loan, mortgage, or line of credit == No
7. Click 'Add it!' button

Usage
===
python mint_bitcoin_sync.py "mint.com-login" "mint.com-password" "public-bitcoin-addresses-comma-separated"
