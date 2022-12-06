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
		self.better_result = pd.read_sql(s, db_conn, "index")
		self.result = db_conn.execute(s).fetchall()
		self.first_index = self.result[0][0]
		self.last_index = self.result[len(self.result)-1][0]

	def create_rolling_average(self):
		print(self.better_result.rolling("210D").mean())
		print(self.better_result)

	def compute_average(q):
		total = 0
		for i in range(len(q)):
			next_item = q.popleft()
			total = total + next_item[1]
			q.append(next_item)
		return total/len(q)

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
