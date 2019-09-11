from Photovoltaics import *
import pandas as pd
from scipy.interpolate import interp1d
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
from datetime import datetime
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

volts = volt_df.iloc[:, 2]
das_flux = solar_df.iloc[:, 2]
temp = temp_df.iloc[:, 2]
dasT = temp_df.iloc[:, 2]
current = current_df.iloc[:, 2]
temp0 = 25
current_cal = current + 0.2*(temp - temp0)
station_flux = weather_df.iloc[:, 1]
pv = Photovoltaics(38.7, 9.42, 32.1, 8.92, 285, 1.00, 60)
pvarray = Photovoltaics(5 * 38.7, 9.42, 5 * 32.1, 8.92, 5 * 285, 1.00, 60 * 5)

t_das = pd.Series(index=range(temp.shape[0]))
for i, t_das_str in enumerate(temp.iloc[:, 1]):
	t_das[i] = datetime.strptime(t_das_str + " -0000", "%Y-%m-%d %H:%M:%S %z")
station_flux_interp = interp1d()

tstart_str = weather_df.iloc[0, 0] + " -0500"
tstop_str = weather_df.iloc[-1, 0] + " -0500"
tstart = datetime.strptime(tstart_str, "%m/%d/%Y %H:%M %z")
tstop = datetime.strptime(tstop_str, "%m/%d/%Y %H:%M %z")
temp_15 = pd.Series(index=range(station_flux.shape[0]))
current_15 = pd.Series(index=range(station_flux.shape[0]))
volt_15 = pd.Series(index=range(station_flux.shape[0]))
das_flux_15 = pd.Series(index=range(station_flux.shape[0]))

j = -1
k = 0
for i in range(int((temp.shape[0]-8))):
	t = temp_df.iloc[i, 1]
	utc = datetime.strptime(t + " -0000", "%Y-%m-%d %H:%M:%S %z")
	if utc == tstart:
		j = 0
		k = i
	if j > -1:
		t = temp_df.iloc[k, 1]
		tnow = datetime.strptime(t + " -0000", "%Y-%m-%d %H:%M:%S %z")
		if tnow >= tstop or k + 8 > temp.shape[0]:
			break
		temp_15[j] = np.nanmean(temp[np.array(range(k - 7, k + 8))])
		current_15[j] = np.nanmean(current_cal[np.array(range(k - 7, k + 8))])
		volt_15[j] = np.nanmean(volts[np.array(range(k - 7, k + 8))])
		das_flux_15[j] = np.nanmean(das_flux[np.array(range(k - 0, k + 1))])
		j = j + 1
		k = k + 15


# plt.plot(das_flux, weather_df[:, 1])
mpp_model = pd.Series(index=range(station_flux.shape[0]))
for i in range(temp_15.shape[0]):
	vmp, imp = pvarray.mpp(temp_15[i], station_flux[i])
	mpp_model[i] = vmp*imp
plt.scatter(station_flux, current_15*volt_15)
plt.scatter(station_flux, mpp_model)
plt.show()
