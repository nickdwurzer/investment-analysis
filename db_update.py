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

def update_all():
    #get all tickers, loop through update_table()
    pass
def update_table():
    #get_last_trade_day() for the ticker
    #cast date appropiately
    #si.get_data()
    #merge data into table
    #catch weird cases
    #   -company isn't trading anymore
    #   -company still trading, but no knew data (weekend)
    #   -company no longer on yahoofinance
    pass
#remember that a comapanies very first trading day is the first enty in the table
#sp_500 tickers not working
def main():
    dow_tickers = si.tickers_dow()
    #print(dow_tickers[0])
    last_trade_day = get_last_trade_day("historical_price.db", dow_tickers[0])
    #date format for grabbing price data
    #print(dt.date.today().strftime("%m/%d/%Y"))
    last_trade_day = last_trade_day[:4]+"/"+last_trade_day[5:7]+"/"+str(int(last_trade_day[8:10])+1)#correct string representation-add one day so no overlap
    #print(last_trade_day)
    print(si.get_data(dow_tickers[0], start_date=last_trade_day))

if __name__ == "__main__":
    main()