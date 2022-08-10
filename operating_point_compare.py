from Photovoltaics import *
import numpy as np
import pandas as pd

if __name__ == "__main__":
	print('run')
	file_name = "consolidated_data2.csv"
	df = pd.read_csv(file_name)
	pv = Photovoltaics(38.7, 9.42, 32.1, 8.92, 285, 1.00, 60)
	pvarray = Photovoltaics(voc=5 * 38.7, isc=9.42, vmp=5 * 32.1, imp=8.92, pmax=5 * 285, n=1.00, nseries=60 * 5)
	# pvarray.Rs = pvarray.Rs  #+ 2/300 # add 2 ohms for line losses (1ohm/1000ft for 2 wires)

	pvarray.a_parameter = pvarray.a_parameter
	temp = 273.15 + 27
	flux = 672
	v_meas = 137.77
	i_meas = 5.94
	#print(pvarray.current(pvarray.voc, 300, 1000))
	#print(pvarray.current(pvarray.vmp, 300, 1000))
	varray = np.linspace(0, pvarray.voc, 100)
	I = np.zeros(100)
	for index, v in enumerate(varray):
		I[index] = pvarray.current(v, temp, flux)
	plt.plot(varray, I, label='Model')
	p = varray*I
	pmax = max(p)
	vmp_model = varray[np.argmax(p)]
	imp_model = I[np.argmax(p)]
	print(vmp_model)
	plt.plot(vmp_model, imp_model, label='MPP', marker='o')
	plt.plot(v_meas, i_meas, label='Operating Point', marker='x')
	#plt.plot(139.374,7.560, label='actual', marker='x')
	#plt.plot(139.374,7.560, label='actual', marker='x')
	#plt.plot(139.374,7.2, label='actual', marker='x')
	plt.axis([0,225, 0, 10])
	plt.title('Array Model')
	plt.legend()
	plt.show()
	print(pvarray.voltage(0, temp, flux))
	print(pvarray.mpp_p(df['temp']+273.15, df['flux']))
	print('done')