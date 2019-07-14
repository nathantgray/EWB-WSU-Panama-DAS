from Photovoltaics import *
import pandas as pd
import numpy as np
if __name__ == "__main__":
	print('run')

	pv = Photovoltaics(38.7, 9.42, 32.1, 8.92, 285, 1.00, 60)
	pvarray = Photovoltaics(5*38.7, 9.42, 5*32.1, 8.92, 5*285, 1.00, 60*5)
	file = "DAS_temp-rad-volt.xlsx"
	df = pd.read_excel(file, sheet_name='Sheet4', header=0, index_col=0)
	#writer = pd.ExcelWriter(file)
	print("Column headings:")
	print(df.columns)

	volts = df['Volts']
	irradiance = df['Irradiance']
	temp = df['Temp']
	N = len(df['Volts'])
	Icalc = np.zeros(shape=(N,1))
	#Icalc = pvarray.current(volts, 274.15 + temp, irradiance)
	for i in range(N):
		Icalc[i] = pvarray.current(volts[i], 274.15 + temp[i], irradiance[i])
		#print(Icalc[i])
	df['Calculated Current'] = Icalc
	df.to_excel(file, sheet_name='Sheet4')
