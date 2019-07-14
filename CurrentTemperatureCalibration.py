from Photovoltaics import *
import pandas as pd
import urllib.request
import matplotlib.pyplot as plt

import numpy as np
if __name__ == "__main__":
	print('run')
	date_range = 2
	volt_url = 'http://kw4h.org:8080/render/?target=scale(05011.AD01.Pump_Voltage,801)&format=csv&from=-' + str(date_range) + 'd'
	solar_url = 'http://kw4h.org:8080/render/?target=scale(05011.AD05.Pyranometer,400)&format=csv&from=-' + str(date_range) + 'd'
	temp_url = 'http://kw4h.org:8080/render/?target=scale(05011.AD12.Temp_In_Water_Tank,1)&format=csv&from=-' + str(date_range) + 'd'
	dasT_url = 'http://kw4h.org:8080/render/?target=scale(05011.AD11.*,1)&format=csv&from=-' + str(date_range) + 'd'
	current_url = 'http://kw4h.org:8080/render/?target=scale(offset(05011.AD02.Pump_Current,-2.59),45)&format=csv&from=-' + str(date_range) + 'd'
	volt_dir_obj = urllib.request.urlretrieve(volt_url)
	solar_dir_obj = urllib.request.urlretrieve(solar_url)
	temp_dir_obj = urllib.request.urlretrieve(temp_url)
	dasT_dir_obj = urllib.request.urlretrieve(temp_url)
	current_dir_obj = urllib.request.urlretrieve(current_url)
	volt_dir = volt_dir_obj[0]
	solar_dir = solar_dir_obj[0]
	temp_dir = temp_dir_obj[0]
	dasT_dir = temp_dir_obj[0]
	current_dir = current_dir_obj[0]
	volt_df = pd.read_csv(volt_dir)
	solar_df = pd.read_csv(solar_dir)
	temp_df = pd.read_csv(temp_dir)
	dasT_df = pd.read_csv(temp_dir)
	current_df = pd.read_csv(current_dir)
	volts = volt_df.iloc[:,2]
	irradiance = solar_df.iloc[:,2]
	temp = temp_df.iloc[:,2]
	dasT = temp_df.iloc[:,2]
	current = current_df.iloc[:,2]
	pv = Photovoltaics(38.7, 9.42, 32.1, 8.92, 285, 1.00, 60)
	pvarray = Photovoltaics(5*38.7, 9.42, 5*32.1, 8.92, 5*285, 1.00, 60*5)
	temp0 = 25
	N = len(temp)
	Icalc = np.zeros(shape=(N,1))
	coef = np.zeros(shape=(N, 1))
	line = np.zeros(shape=(N, 1))
	for i in range(N):
		Icalc[i] = pvarray.current(volts[i], 274.15 + temp[i], irradiance[i])
		dT = temp[i]-temp0
		try:
			coef[i] = current[i]/(dasT[i]-temp0)
		except:
			coef[i] = NULL
		line[i] = -0.2
	plt.plot(range(N), current, range(N), coef, range(N), line)
	plt.show()