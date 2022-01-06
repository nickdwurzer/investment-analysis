#!/usr/bin/env python3
import yahoo_fin.stock_info as si
import pandas as pd

def main():
	
	dow_tickers = si.tickers_dow()
	#financials_dict = si.get_financials(dow_tickers[0], yearly = True, quarterly = False)
	#print(type(financials_dict["yearly_income_statement"]))
	print_financials_of_list(dow_tickers)
	#print_index_tables()

#This function prints the Balance Sheet, Income Statement and Statement of Cash flows for all tickers passed into the function
def print_financials_of_list(index):
	for i in index:
		financials = si.get_financials(i, yearly = True, quarterly = False)
		print(i,financials, "\n", sep = "\n")	


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

if __name__ == "__main__":
	main()
