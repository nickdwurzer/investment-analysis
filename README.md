# investment-analysis
This repo is for everything related to comparing and analyzing stocks and stock data.  It is intended for educational purposes only.

Currently this project aims to experiment and see what financial data can be gathered and analysed using open-source code.

The end goal is store much of this data in a local database and produce some analysis on the data which could be displayed locally or on the web.

y_fin1.py uses the python libraries <a href="http://theautomatic.net/yahoo_fin-documentation/"> yahoo_fin</a> and <a href="https://pandas.pydata.org/"> pandas</a>.  Further exploration will use the python library <a href="https://pypi.org/project/yfinance/"> yfinance</a>.

Currently y_fin1.py has functions which can:
  
<i>-Gather data price data from about 20,000 publicly listed companies
-Store this data in a database
-Add new columns to the data (Ex. Moving Average)</i>

Further work is aimed at implimenting two trading strategies and back-testing them to determine their effectiveness.  The first strategy is momentum based and the second is based on the idea of a "magic formula" which weights different attributes of companies and takes the companies that scored highest based on the sum of those weighted values.
