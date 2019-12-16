from math import exp, log
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.special import lambertw
class Photovoltaics:
	def __init__(self, voc, isc, vmp, imp, pmax, n, nseries):
		self.voc = voc
		self.isc = isc
		self.vmp = vmp
		self.imp = imp
		self.wmp = pmax
		self.k = 1.380649*10**-23 # J/K Boltzmann constant
		self.q = 1.602176634*10**-19 # C elementary charge
		self.h = 6.626*10**-34 # joule s  Planck's constant
		self.c = 2.998*10**8 # m/s Speed of light
		self.n = n
		self.eg = 1.15 # eV band gap energy https://www.researchgate.net/publication/256598615_Saturation_current_in_solar_cells_-_An_analysis
		self.area = 122.861 # cm^2 cell area
		self.nseries = nseries
		self.a_parameter = 2.3349*10**7
		self.Rs = 0.00382
		self.Rsh = 1e6

	def current(self, volts, temp, flux):
		V = volts
		T = temp
		k = self.k
		q = self.q
		n = self.n
		I_L = self.isc*flux/1000
		V_T = k*T/q
		ns = self.nseries # number of cells in series
		Vc = V/ns # cell voltage
		Rs = self.Rs
		Rsh = self.Rsh
		I0 = self.a_parameter*self.area * exp(-self.eg/V_T)
		if Rs == 0:
			Iout = I_L - I0*(exp(Vc/(n*V_T))-1) - Vc/Rsh
		else:
			term1 = ((I_L + I0) - Vc/Rsh)/(1+Rs/Rsh)
			term2 = -n*V_T/Rs
			term3 = I0*Rs/(n*V_T*(1+Rs/Rsh))
			term4 = Vc/(n*V_T)
			term5 = (1-Rs/(Rs+Rsh))
			term6 = (I_L+I0)*Rs/(n*V_T*(1+Rs/Rsh))
			Iout = term1 + term2*np.real(lambertw(term3*exp(term4*term5+term6)))
		return Iout

	def voltage(self, current, temp, flux):
		I = current
		T = temp
		k = self.k
		q = self.q
		n = self.n
		ns = self.nseries # number of cells in series
		V_T = k*T/q
		I_L = self.isc*flux/1000
		I0 = self.a_parameter*self.area * exp(-self.eg/V_T)
		Rs = self.Rs
		Rsh = self.Rsh

		term1 = (I_L + I0)*Rsh
		term2 = -I*(Rs + Rsh)
		term3 = -n*V_T
		term4 = I0*Rsh/(n*V_T)
		term5 = (I_L + I0 - I)*Rsh/(n*V_T)
		try:
			Vout = ns*(term1 + term2 + term3*np.real(lambertw(term4*exp(term5))))
		except:
			print('Ignoring shunt resistance')
			Vout = ns*(n*V_T*log((I_L - I)/I0 + 1) - I*Rs)
		return Vout

	def mpp(self, temp, flux):
		res = 100
		v_space = np.linspace(0, self.voc, res)
		i_space = np.zeros(res)
		for index, v in enumerate(v_space):
			i_space[index] = self.current(v, temp, flux)
		p = v_space*i_space
		pmax = max(p)
		vmp_model = v_space[np.argmax(p)]
		imp_model = i_space[np.argmax(p)]
		return [vmp_model, imp_model]

	def mpp_p(self, temp, flux, resistance = 2):
		res = 100
		v_space = np.linspace(0, self.voc, res)
		i_space = np.zeros(res)
		for n in range(res):
			v_space[n] = v_space[n] - i_space[n]*resistance
		for index, v in enumerate(v_space):
			i_space[index] = self.current(v, temp, flux)
		p = v_space*i_space
		pmax = max(p)
		return pmax
# if __name__ == "__main__":
# 	print('run')
# 	pv = Photovoltaics(38.7, 9.42, 32.1, 8.92, 285, 1.00, 60)
# 	pvarray = Photovoltaics(5*38.7, 9.42, 5*32.1, 8.92, 5*285, 1.00, 60*5)
# 	pvarray.Rs = pvarray.Rs #+ 2/300 # add 2 ohms for line losses (1ohm/1000ft for 2 wires)
# 	temp = 274.15 + 30
# 	flux = 191
# 	#print(pvarray.current(pvarray.voc, 300, 1000))
# 	#print(pvarray.current(pvarray.vmp, 300, 1000))
# 	varray = np.linspace(0, pvarray.voc, 100)
# 	I = np.zeros(100)
# 	for index, v in enumerate(varray):
# 		I[index] = pvarray.current(v, temp, flux)
# 	plt.plot(varray, I, label='Model')
# 	p = varray*I
# 	pmax = max(p)
# 	vmp_model = varray[np.argmax(p)]
# 	imp_model = I[np.argmax(p)]
# 	print(vmp_model)
# 	plt.plot(vmp_model, imp_model, label='MPP', marker='o')
# 	plt.plot(139.374,7.335, label='Operating Point', marker='x')
# 	#plt.plot(139.374,7.560, label='actual', marker='x')
# 	#plt.plot(139.374,7.560, label='actual', marker='x')
# 	#plt.plot(139.374,7.2, label='actual', marker='x')
# 	plt.axis([0,225, 0, 10])
# 	plt.title('Array Model')
# 	plt.legend()
# 	plt.show()
# 	print(pvarray.voltage(0, temp, flux))
# 	print('done')
