#!/usr/bin/env python3
import yahoo_fin.stock_info as si
import pandas as pd
import sqlalchemy as sqla
import add_moving_average as ama

def main():
	eng = sqla.create_engine("sqlite:////Users/nicholaswurzer/finance/yahoo_fin/historical_price.db", echo = False)
	ma = ama.moving_average(eng, 'AAPL')
	ma.create_moving_average()
	ma.create_rolling_average()
	#db_to_csv("/Users/nicholaswurzer/finance/yahoo_fin/historical_price.db", "/Users/nicholaswurzer/finance/csv/")
	#dow_tickers = si.tickers_dow()
	#nasdaq_tickers = si.tickers_nasdaq()
	#sp500_tickers = si.tickers_sp500()
	#ftse100_tickers = si.tickers_ftse100()
	#ftse250_tickers = si.tickers_ftse250()
	#nifty50_tickers = si.tickers_nifty50()
	#niftybank_tickers = si.tickers_niftybank()
	#other_tickers = si.tickers_other()
	#print("dow ", len(dow_tickers), "nasdaq ", len(nasdaq_tickers),"sp500 ", len(sp500_tickers),"ftse100 ", len(ftse100_tickers), "ftse250 ", len(ftse250_tickers), "nifty50 ", len(nifty50_tickers), "other ", len(other_tickers))
	#create_tables(other_tickers, frequency = "1d")
	#dow_tickers_price_history = get_historical_price_of_list(dow_tickers, "1d", "01/01/2000", "01/10/2000")
	#print(dow_tickers_price_history)
	#create_test_tables(dow_tickers, "1d", "01/03/2000", "01/04/2000", "/test_1tick_1day.db", 1)
	#create_test_tables(dow_tickers, "1d", "01/03/2000", "01/04/2000", "/test_10tick_1day.db", 10)
	#financials_dict = si.get_financials(dow_tickers[0], yearly = True, quarterly = False)
	#print(type(financials_dict["yearly_income_statement"]))
	#print_financials_of_list(dow_tickers)
	#print_index_tables()
	#create_database(get_financials_of_list(financials_dict))

def get_historical_price_of_list(tickers, interval, start, end):
	my_data = pd.DataFrame()
	for i in tickers:
		try:
			#print(type(my_data.size.item()))
			my_data = pd.concat([my_data, si.get_data(i, interval = interval, start_date = start, end_date = end)], axis = 1, ignore_index = True)
		except AssertionError:
			#raised when data doesn't exist for that date range
			pass
	#print(my_data)
	return my_data

#This function prints the Balance Sheet, Income Statement and Statement of Cash flows for all tickers passed into the function
def print_financials_of_list(index):
	for i in index:
		financials = si.get_financials(i, yearly = True, quarterly = False)
		print(i,financials, "\n", sep = "\n")	

#TODO description
def get_financials_of_list(index):
	for i in index:
		financials = si.get_financials(i, yearly = True, quarterly = False)
	return financials

#This function prints all of the index tables which yahoo_fin is able to scrape
def print_index_tables():
	print("DOW",si.tickers_dow(True), sep = "\n")
	print("FTSE100",si.tickers_ftse100(True), sep = "\n")
	print("FTSE250",si.tickers_ftse250(True), sep = "\n")
	print("IBOVESPA",si.tickers_ibovespa(True), sep = "\n")
	print("NASDAQ",si.tickers_nasdaq(True), sep = "\n")
	print("NIFTY50",si.tickers_nifty50(True), sep = "\n")
	print("NIFTYBANK",si.tickers_niftybank(), sep = "\n")
	print("OTHER",si.tickers_other(True), sep = "\n")
	print("S&P500",si.tickers_sp500(True), sep = "\n")

#TODO description
def create_database(my_dataframe):
	print("creating database...")
	sqlengine = sqla.create_engine('sqlite://', echo = False)
	my_dataframe.to_sql("financials", con = sqlengine)
	print(sqlengine.execute("SELECT * FROM financials").fetchall())
	sqlengine.dispose()

#TODO description
def create_tables(tickers, frequency):
	sqlengine = sqla.create_engine("sqlite:////Users/nicholaswurzer/finance/yahoo_fin/historical_price.db", echo = False)
	for i in tickers:
		print(i)
		try:
			ticker_price_history = si.get_data(i, interval = frequency, index_as_date = True)
		except AssertionError:
			#didn't return any data
			pass
		except KeyError:
			print("key error occurred")
		try:
			ticker_price_history.to_sql(i, con = sqlengine, if_exists = "replace")
		except UnboundLocalError:
			pass
		#print(sqlengine.execute("SELECT * FROM " + i).fetchall())
		sqlengine.dispose()

#TODO description
def create_test_tables(tickers, interval, start, end, file, num_ticks):
	sqlengine = sqla.create_engine("sqlite:////Users/nicholaswurzer/finance/yahoo_fin" + file, echo = False)
	for i in range(num_ticks):
		try:
			ticker_price_history = si.get_data(tickers[i], interval = interval, start_date = start, end_date = end)
		except AssertionError:
			#didn't return any data
			num_ticks = num_ticks + 1
			pass
		ticker_price_history.to_sql(tickers[i], con = sqlengine)
		#print(sqlengine.execute("SELECT * FROM " + i).fetchall())
		sqlengine.dispose()

def db_to_csv(path_to_db, path_to_csv):
	sqlengine = sqla.create_engine("sqlite:///" + path_to_db, echo = False)
	with sqlengine.connect() as conn:
		for table_name in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
			table = pd.read_sql_query("SELECT * FROM '" + table_name["name"] + "'", conn)
			table.to_csv(path_to_csv + table_name["name"] + ".csv")
	sqlengine.dispose()
	

if __name__ == "__main__":
	main()
