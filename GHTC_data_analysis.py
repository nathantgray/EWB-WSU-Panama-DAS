import pandas as pd
import matplotlib.pyplot as plt
das_file_name = "DAS_functionalDays.csv"
weather_file_name = "weather_station_6-28_through_7-11.csv"
das_df = pd.read_csv(das_file_name)
w_df = pd.read_csv(weather_file_name)

print(das_df.head())
das_df.set_axis(['utc_time', 'current', 'voltage', 'flux', 'temp', 'das_temp', 'gal_in', 'gal_out'], axis=1, inplace=True)
# Format time stamps as datetime class and set as index
das_df = das_df.assign(time=pd.to_datetime(das_df['utc_time'] + " -0000", format="%m/%d/%Y %H:%M %z"))
das_df.set_index('time', inplace=True)
# First calibrate current
das_df = das_df.assign(current_cal=das_df['current'] + 0.2*(das_df['temp'] - 25))
print(das_df.head())
# current_cal[i] = current[i] +0.2*(temp[i] - temp0)
# Calculate Power
das_df = das_df.assign(power=das_df['current_cal']*das_df['voltage'])
# Calculate Flow Rate
das_df['gal_in'].interpolate(method='time', inplace=True)
das_df = das_df.assign(in_rate=das_df['gal_in'].diff())

# Calculate W/GPM
das_df = das_df.assign(power_to_flowrate=das_df['power']/das_df['in_rate'])

# Other relationships
das_df.plot(kind='scatter', x='flux', y='power')

# Add weather station data processing
w_df = w_df.assign(time=pd.to_datetime(w_df['Timestamp'] + " -0500", format="%m/%d/%Y %H:%M %z"))
w_df.set_index('time', inplace=True)
print(w_df.head())

# Synchronize das with weather data
w_df = w_df.resample('1Min').interpolate(method='spline', order=3)

plt.show()
#das_df = das_df.assign(in_rate=das_df[])

