from Photovoltaics import *
import pandas as pd
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
# http://kw4h.org:8080/render/?target=scale(offset(05011.AD02.Pump_Current,-2.59),45)&format=csv&from=-70d&until=-54d
import numpy as np
if __name__ == "__main__":
	print('run')

	volt_dir = "Voltdata_functioningDays.csv"
	solar_dir = "pyranometer_functioningDays.csv"
	temp_dir = "temp_functioningDays.csv"
	dasT_dir = "DAST_functioningDays.csv"
	current_dir = "current_functioningDays.csv"
	weather_dir = "WeatherStationIrradiance_functioningDays.csv"
	volt_df = pd.read_csv(volt_dir)
	solar_df = pd.read_csv(solar_dir)
	temp_df = pd.read_csv(temp_dir)
	dasT_df = pd.read_csv(temp_dir)
	current_df = pd.read_csv(current_dir)
	weather_df = pd.read_csv(weather_dir)
	volts = volt_df.iloc[:,2]
	irradiance = solar_df.iloc[:,2]
	temp = temp_df.iloc[:,2]
	dasT = temp_df.iloc[:,2]
	current = current_df.iloc[:,2]
	pv = Photovoltaics(38.7, 9.42, 32.1, 8.92, 285, 1.00, 60)
	pvarray = Photovoltaics(5 * 38.7, 9.42, 5 * 32.1, 8.92, 5 * 285, 1.00, 60 * 5)
	temp0 = 25
	N = len(temp)
	Icalc = np.zeros(shape=(N,1))
	coef = np.zeros(shape=(N, 1))
	line = np.zeros(shape=(N, 1))
	current_cal = np.zeros(shape=(N, 1))
	for i in range(N):

		current_cal[i] = current[i] + 0.2*(temp[i] - temp0)
		Icalc[i] = pvarray.current(volts[i], 274.15 + temp[i], irradiance[i])
		dT = temp[i]-temp0
		# try:
		# 	coef[i] = current[i]/(temp[i]-temp0)
		# except:
		# 	coef[i] = np.nan
		line[i] = -0.2
	coef_ave = np.mean(coef)
	print(coef_ave)
	#plt.plot(range(N), coef, range(N), line)
	plt.plot(range(N), Icalc, range(N), current_cal, range(N), current)
	plt.show()
