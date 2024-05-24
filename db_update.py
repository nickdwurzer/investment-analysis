#!./venv/bin/python
import yahoo_fin.stock_info as si
import pandas as pd
from datetime import datetime as dt
import sqlite3 as sql3
import requests

#retuns the last trading day in the database for a company.
def get_last_trade_day(database, ticker):
    conn = sql3.connect(database)
    cursor = conn.cursor()
    try:
        result = cursor.execute('SELECT "index" FROM ' + ticker + ' ORDER BY "index" DESC LIMIT 1')
        date = result.fetchall()[0][0]
        conn.close()
        return date
    except sql3.OperationalError as e:
        print(e)
        return None

def update_all(database):
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
    for i in range(len(tickers)):
        if i % 10 == 0:
            print(f"Updated {i} of {len(tickers)} stocks.")
        update_table(database, tickers[i])

def update_table(database, ticker):
    last_trade_day = get_last_trade_day("historical_price.db", ticker)
    #TODO if table doesn't exist yet, but data can be retrieved, make a new table.
    if(last_trade_day):
        # Format date and add one day so that there is no overlap
        #TODO change to datetime and increase by one day
        last_trade_day_si = last_trade_day[:4]+"/"+last_trade_day[5:7]+"/"+str(int(last_trade_day[8:10])+1)
        last_trade_day = dt.fromisoformat(str(last_trade_day))
        try:
            data = si.get_data(ticker, start_date=last_trade_day_si)
            retrieved_date = str(data.iloc[0].name)
            retrieved_date = dt.fromisoformat(retrieved_date)
            if retrieved_date > last_trade_day:
                conn = sql3.connect(database)
                data.to_sql(ticker, conn, if_exists='append')
                conn.close()
            else:
                print("Incorrect start date of reteived data.")
        except AssertionError:
            #TODO give more helpful message
            print("Error retrieving data for ticker " + ticker)
        except KeyError:
            #TODO give more helpful message
            print("Error retrieving data for ticker " + ticker)
        except requests.exceptions.ChunkedEncodingError:
            #TODO give more helpful message
            print("Error retrieving data for ticker " + ticker)

#remember that a comapanies very first trading day is the first entity in the table
def main():
    update_all("historical_price.db")

if __name__ == "__main__":
    main()