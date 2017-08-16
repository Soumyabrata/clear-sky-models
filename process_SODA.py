import numpy as np
import csv
import datetime 
from datetime import timedelta


def process_SODA(CSV_file):

	# Weather station data
	# read the input file
	with open(CSV_file) as f: #f is a file header
		reader = csv.reader(f, delimiter=",")
		d = list(reader) # d is a list of list here.
	
	wo_header = []
	for i in d:
		if i[0][0][0]!='#':
			wo_header.append(i)


	solar_array = []
	datetime_array = []

	for line in wo_header:
		y = line[0].strip().split(";")
		GHI_item = float(y[2])
		solar_array.append(GHI_item)

		time_stamp = y[0]
		dt = time_stamp.strip().split("/")
		dt2 = dt[0]
		dt3 = dt2.strip().split("T")
		dt4 = dt3[1]
		dt5 = dt4.strip().split(":")

		hour_item = int(dt5[0])
		min_item = int(dt5[1])

		dt6 = dt5[2]
		dt7 = dt6.strip().split(".")
		sec_item = int(dt7[0])


		day3 = dt3[0]
		day4 = day3.strip().split("-")

		year_item = int(day4[0])
		month_item = int(day4[1])
		day_item = int(day4[2])

		sw = datetime.datetime(year_item,month_item,day_item,hour_item,min_item,sec_item)

		date_n_time_item = sw + timedelta(hours=8)
		datetime_array.append(date_n_time_item)


	solar_array = np.array(solar_array)



	return(datetime_array,solar_array)
