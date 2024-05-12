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
    date = result.fetchall()[0][0]
    conn.close()
    return date

def update_all():
    dow_tickers = si.tickers_dow()
    nasdaq_tickers = si.tickers_nasdaq()
    sp500_tickers = si.tickers_sp500()
    # bug for ftse tickers
    # ftse100_tickers = si.tickers_ftse100()
    # ftse250_tickers = si.tickers_ftse250()
    nifty50_tickers = si.tickers_nifty50()
    niftybank_tickers = si.tickers_niftybank()
    other_tickers = si.tickers_other()
    tickers = dow_tickers + nasdaq_tickers + sp500_tickers + nifty50_tickers + niftybank_tickers + other_tickers
    for ticker in tickers:
        update_table(ticker)

def update_table(database, ticker):
    last_trade_day = get_last_trade_day("historical_price.db", ticker)
    # Format date and add one day so that there is no overlap
    last_trade_day = last_trade_day[:4]+"/"+last_trade_day[5:7]+"/"+str(int(last_trade_day[8:10])+1)
    try:
        data = si.get_data(ticker, start_date=last_trade_day)
        conn = sql3.connect(database)
        data.to_sql(ticker, conn, if_exists='append')
        conn.close()
    except AssertionError:
        print("Error retrieving data for ticker " + ticker)

#remember that a comapanies very first trading day is the first entity in the table
def main():
    #update_all()
    # update_table("historical_price.db", si.tickers_dow()[0])
    # conn = sql3.connect("historical_price.db")
    # cursor = conn.cursor()
    # result = cursor.execute('SELECT * FROM ' + si.tickers_dow()[0] + ' ORDER BY "index"')
    # print(result.fetchall())
    # conn.close()
    #TODO remove last 10 rows of 'AAPL' ticker, update was incorrect.
    #TODO convert retrieved_date and last_trade_day to a datetime and compare them.
    #TODO only update table if retrieved_date >= last_trade_date
    #This is because get_data can return data before start_date
    last_trade_day = get_last_trade_day("historical_price.db", 'AAPL')
    last_trade_day = last_trade_day[:4]+"/"+last_trade_day[5:7]+"/"+str(int(last_trade_day[8:10])+1)
    data = si.get_data("AAPL", start_date=last_trade_day)
    print(last_trade_day)
    retrieved_date = str(data.iloc[0].name)
    retrieved_date = retrieved_date[:4]+"/"+retrieved_date[5:7]+"/"+retrieved_date[8:10]
    print(retrieved_date)

if __name__ == "__main__":
    main()