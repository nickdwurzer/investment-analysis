#!usr/bin/env python3
import pandas as pd
import sqlalchemy as sqla
import datetime as dt
from collections import deque
import statistics

class moving_average:
	def __init__(self, db_conn, table):
		metadata = sqla.MetaData()
		meta_table = sqla.Table(table, metadata,
			sqla.Column("index", sqla.DateTime, primary_key = True),
			sqla.Column("open", sqla.Float()),
			sqla.Column("high", sqla.Float()),
			sqla.Column("low", sqla.Float()),
			sqla.Column("close", sqla.Float),
			sqla.Column("adjclose", sqla.Float()),
			sqla.Column("volume", sqla.BigInteger),
			sqla.Column("ticker", sqla.String(20)))
		s = sqla.select(meta_table.c.index, meta_table.c.close)
		self.result = pd.read_sql(s, db_conn, "index")
		self.old_result = db_conn.execute(s).fetchall()
		self.first_index = self.result.index[0]
		self.last_index = self.result.index[len(self.result)-1]
		
		print(self.first_index, self.last_index)

	def get_buy_sell_signals(self, short_MA, long_MA):
		buy = False
		sell = False
		profit_list = []
		time_period_list = []
		for i in range(1, len(short_MA)):
			if((short_MA.iat[i-1, 0] < long_MA.iat[i-1, 0]) and (short_MA.iat[i, 0] > long_MA.iat[i, 0])):
				#print(short_MA.iat[i-1, 0], long_MA.iat[i-1, 0], short_MA.iat[i, 0], long_MA.iat[i, 0], i)
				buy_price = self.result.iat[i, 0]
				buy_index = i
				buy = True
			if((short_MA.iat[i-1, 0] > long_MA.iat[i-1, 0]) and (short_MA.iat[i, 0] < long_MA.iat[i, 0]) and buy):
				sell_price = self.result.iat[i, 0]
				sell_index = i
				sell = True
			if(buy and sell):
				buy = False
				sell = False
				profit = (sell_price - buy_price)/buy_price*100
				time_period = sell_index - buy_index
				profit_list.append(profit)
				time_period_list.append(time_period)
				print("profit = "+ str(profit) + "% over " + str(time_period) + "days")

		#print("average_profit = " + str(sum(profit_list)/len(profit_list)) + " average time period = " + str(sum(time_period_list)/len(time_period_list)))
		return [profit_list, time_period_list]

	def create_rolling_average(self, window):
		return self.result.rolling(str(window) +"D").mean()

	def compute_average(q):
		total = 0
		for i in range(len(q)):
			next_item = q.popleft()
			total = total + next_item[1]
			q.append(next_item)
		return total/len(q)

	#deprecated since disvoery of rolling() method
	def create_moving_average(self):
		#create a list of days to iterate through
		tdelta_1d = dt.timedelta(days = 1)
		days_length = (self.last_index - self.first_index) / tdelta_1d
		temp_date = self.first_index
		days = []
		for i in range(int(days_length + 1)):
			days.append(temp_date)
			temp_date += tdelta_1d

		moving_start = self.first_index
		moving_end = self.first_index + dt.timedelta(weeks = 30)
		#print("moving_start: ",moving_start,"moving_end: ", moving_end)
		q = deque()
		next_pushed = 0
		next_popped = 0
		#move moving average by one
		for i in range(len(days) - int((moving_start - moving_end) / tdelta_1d)):
			#pop next items off
			while(self.result[next_popped][0] < moving_start):
				temp = q.popleft()
				next_popped += 1
			
			#push next items on
			try:
				#might be cleaner to check for the existence of the next item in the list here rather than the try-except
				while(self.result[next_pushed][0] < moving_end):
					q.append(self.result[next_pushed])
					next_pushed += 1
					#print("next pushed: ",next_pushed, "length of result: ", len(self.result))
			except(IndexError):
				#print(q)
				#need to run average here once more
				break;
			#calculate average here
			moving_start += tdelta_1d
			moving_end += tdelta_1d
			#print(q, len(q), f"moving_start: {moving_start}", f"moving_end: {moving_end}", sep = "\n")
			#print(self.result[0], self.result[len(self.result) - 1])
			print(statistics.mean([i.close for i in q]))

if __name__ == "__main__":
	main()
