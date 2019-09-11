from Photovoltaics import *
import numpy as np


if __name__ == "__main__":
	print('run')
	pv = Photovoltaics(38.7, 9.42, 32.1, 8.92, 285, 1.00, 60)
	pvarray = Photovoltaics(5*38.7, 9.42, 5*32.1, 8.92, 5*285, 1.00, 60*5)
	pvarray.Rs = pvarray.Rs #+ 2/300 # add 2 ohms for line losses (1ohm/1000ft for 2 wires)
	temp = 274.15 + 30
	flux = 191
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
	plt.plot(139.374,7.335, label='Operating Point', marker='x')
	#plt.plot(139.374,7.560, label='actual', marker='x')
	#plt.plot(139.374,7.560, label='actual', marker='x')
	#plt.plot(139.374,7.2, label='actual', marker='x')
	plt.axis([0,225, 0, 10])
	plt.title('Array Model')
	plt.legend()
	plt.show()
	print(pvarray.voltage(0, temp, flux))
	print('done')