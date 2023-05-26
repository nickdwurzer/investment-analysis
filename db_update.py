#!./venv/bin/python
import yahoo_fin.stock_info as si
import pandas as pd
import datetime as dt
import sqlite3 as sql3

#retuns the last trading day in the database for a company.
def get_last_trade_day(database, ticker):
    conn = sql3.connect(database)
    cursor = conn.cursor()
    result = cursor.execute('SELECT "index" FROM ' + ticker + ' ORDER BY "index" DESC LIMIT 1')
    #returned date has type string
    return result.fetchall()[0][0]

def main():
    dow_tickers = si.tickers_dow()
    #print(dow_tickers[0])
    get_last_trade_day("historical_price.db", dow_tickers[0])

if __name__ == "__main__":
    main()