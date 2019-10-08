import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

das_file_name = "DAS_functionalDays.csv"
weather_file_name = "weather_station_6-28_through_7-11.csv"
das_df = pd.read_csv(das_file_name)
w_df = pd.read_csv(weather_file_name)

print(das_df.head())
das_df.set_axis(['utc_time', 'current_raw', 'voltage', 'flux', 'temp', 'das_temp', 'gal_in', 'gal_out'], axis=1, inplace=True)
# Format time stamps as datetime class and set as index
das_df = das_df.assign(time=pd.to_datetime(das_df['utc_time'] + " -0000", format="%m/%d/%Y %H:%M %z"))
das_df.set_index('time', inplace=True)
# First calibrate current
das_df = das_df.assign(current_cal=das_df['current_raw'] + 0.2*(das_df['temp'] - 25))
print(das_df.head())
# current_cal[i] = current[i] +0.2*(temp[i] - temp0)
# Calculate Power
das_df = das_df.assign(power=das_df['current_cal']*das_df['voltage'])
# Calculate Flow Rate
das_df['gal_in'].interpolate(method='time', inplace=True)
das_df = das_df.assign(in_rate=das_df['gal_in'].diff())
das_df = das_df.assign(out_rate=das_df['gal_out'].diff())

# Calculate W/GPM
das_df = das_df.assign(power_to_flowrate=das_df['power']/das_df['in_rate'])

# Calculate voltage at pump
ohms_per_ft = 0.0009989  # Ohms/ft
length = 750  # ft
resistance_per_wire = ohms_per_ft*length
r_circuit = 2*resistance_per_wire
das_df = das_df.assign(pump_voltage=das_df['voltage']-das_df['current_cal']*r_circuit)
das_df = das_df.assign(vdrop=das_df['current_cal']*r_circuit)
das_df = das_df.assign(pump_power=das_df['pump_voltage']*das_df['current_cal'])
das_df = das_df.assign(power_loss=das_df['power']-das_df['pump_power'])


# Add weather station data processing
w_df = w_df.assign(time=pd.to_datetime(w_df['Timestamp'] + " -0500", format="%m/%d/%Y %H:%M %z"))
w_df.set_index('time', inplace=True)
# print(w_df.head())

# Synchronize das with weather data
# w_df.plot(kind='scatter', y='W/m^2 Solar Radiation')
# print(w_df.head())
# w_df.plot(kind='line', y='W/m^2 Solar Radiation')
df = das_df.join(w_df.resample('1Min').asfreq(), how='outer')
df_up = das_df.join(w_df.resample('1Min').interpolate('time'), how='outer')
df_dwn = das_df.join(w_df, how='right')

# Other relationships
# das_df.plot(kind='scatter', x='flux', y='power')
# df_dwn.plot.scatter(x='flux', y='W/m^2 Solar Radiation')
# df_dwn.plot.scatter(x='W/m^2 Solar Radiation', y='power')
# ax = df_dwn.plot.scatter(x='W/m^2 Solar Radiation', y='current_raw', c='red', label="raw current")
# df_dwn.plot.scatter(x='W/m^2 Solar Radiation', y='current_cal', c='blue', label="calibrated current", ax=ax)
# df_dwn.plot.scatter(x='W/m^2 Solar Radiation', y='voltage')
# df_dwn.plot.line(y='power')
# ax = df_dwn.plot.scatter(x='flux', y='current_raw', c='red', label='raw current')
# df_dwn.plot.scatter(x='flux', y='current_cal', c='blue', label='calibrated current', marker='x', ax=ax, )
# df_dwn.plot.scatter(x='flux', y='voltage')
# df_dwn.plot.scatter(x='voltage', y='current_cal', c='W/m^2 Solar Radiation', colormap='viridis')
# df_dwn.plot.scatter(x='voltage', y='current_cal', c='flux', colormap='viridis')
# df.plot.scatter(x='voltage', y='current_cal', c='flux', colormap='viridis')
# df.plot.scatter(x='voltage', y='power', c='flux', colormap='viridis')
# df_dwn.plot.line(y=['flux', 'W/m^2 Solar Radiation'])
# df.plot.scatter(x='power', y='in_rate', xlim=[0, 1400], ylim=[0, 15])
# plt.ylabel('Pump Flow Rate (gpm)')
# plt.xlabel('Solar Power (W)')
# plt.title('Flow Rate vs. Power')
df_2 = df.loc[df['pump_power'] > 30]
df_2 = df_2.loc[0 < df['in_rate']]
df_2 = df_2.loc[df['in_rate'] < 15]
ax = df_2.plot.scatter(x='pump_power', y='in_rate', xlim=[0, 1300], ylim=[0, 15])
plt.ylabel('Pump Flow Rate (gpm)')
plt.xlabel('Pump Power (W)')
plt.title('Flow Rate vs. Power')
x = df_2['pump_power']
xroot = x**(1/2)
x2 = x**2
x3 = x**3
X = pd.DataFrame(data={'x':x, 'xroot':xroot})
X = sm.add_constant(X)
y = df_2['in_rate']
model = sm.OLS(y, X, missing='drop').fit()
ax.plot(model.model.exog[:, 1], model.fittedvalues, 'r.')
print(model.summary())
plt.show()
df.to_csv('consolidated_data.csv')
df_dwn.to_csv('consolidate_downsample.csv')

