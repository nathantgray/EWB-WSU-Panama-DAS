# EWB-WSU-Panama-DAS
Functions for EWB-WSU Panama project DAS

Things are a bit of a mess in the current state.

I have included csv's with for each of the sensors I found usefull for the period of time after the first day of data to the last day that the voltage sensor was functioning. I chose to ignore the first day since not everything was completely up and running that day. However you may want to download that data as well. I have included the url's needed to download each of the sensors' data. Before using the URLs you will want to change the time period to match what you want. 
## To select the days you want data for:
1. Count the number of days before today that you want the data to begin and replace the number 77 with your number.
2. Count the number of days before today that you want the data to stop and replace the number 60 with your number.
We unfortunately can't use absolute date's due to an bug with the backend that handles the URLs. Let me know if you get it to work.

Voltage: http://kw4h.org:8080/render/?target=scale(05011.AD01.Pump_Voltage,801)&format=csv&from=-77d&until=-60d
Current: http://kw4h.org:8080/render/?target=scale(offset(05011.AD02.Pump_Current,-2.59),45)&format=csv&from=-77d&until=-60d
9V_CT_Supply: http://kw4h.org:8080/render/?target=scale(05011.AD03.9V_CT_Supply,1)&format=csv&from=-77d&until=-60d
Data_Logger_DC_Bus: http://kw4h.org:8080/render/?target=scale(05011.AD04.Data_Logger_DC_Bus,4)&format=csv&from=-77d&until=-60d
Pyranometer: http://kw4h.org:8080/render/?target=scale(05011.AD05.Pyranometer,400)&format=csv&from=-77d&until=-60d
Outside Temperature: http://kw4h.org:8080/render/?target=scale(05011.AD12.*,1)&format=csv&from=-77d&until=-60d
DAS Temperature: http://kw4h.org:8080/render/?target=scale(05011.AD11.*,1)&format=csv&from=-77d&until=-60d
Total Gallons of Water Into Tanks: http://kw4h.org:8080/render/?target=05011.PU03.*&format=csv&from=-77d&until=-60d
Total Gallons of Water Out of Tanks: http://kw4h.org:8080/render/?target=05011.PU04.*&format=csv&from=-77d&until=-60d

The python file you may find the most interesting will be Photovoltaics.py. This is a class I created to model solar panels. I specifically tuned the parameters to match the I-V curve provided by the manufacuturer for our panels. The class provides methods for getting the voltage, current, or maximum power point for the modeled panels.

## Other important Notes:

The raw current data is highly dependent on the temperature of the sensor. 
Use this equation to correct it;
temp0 = 25
current_cal = current + 0.2*(temp - temp0)

The pyranometer data clips irradiance data to no more than 730 W/m^2.
You can use the irradiance data from the weather station to correct it, however this is made difficult because the weather station data is spaced out by 15 minutes.

## Questions and ideas I have for analysing data:

* (done) Use Pyranometer and Voltage to calculated current and compare to measured
* (done partial) Calculate water level in tanks and calculated how much overflows
* (done partial) Track daily water use
* (Started) Compare pump output with Grundfos data for the 11-SQF-2
* Calculate if there is excess power available that could be used for other projects in the future such as a cellphone charging station
* Current vs. Irradiance
* Efficiency vs. flow rate


## How Time stamps compare between different sources:

PDT -             UTC-7    e.g. 4:00 AM 

Panama time -     UTC-5    e.g. 6:00 AM 

Grafana graphs -  UTC-9    e.g. 2:00 AM 

CSVs downloaded - UTC-0    e.g. 11:00 AM 
