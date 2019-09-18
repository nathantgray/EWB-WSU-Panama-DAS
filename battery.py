from math import exp
import numpy as np
# https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4544139&tag=1
# https://ieeexplore.ieee.org/document/5733387/references#references
class Battery:
	def __init__(self):
		V0 = 12.6463 	# battery constant voltage
		K = 0.33  		# polarisation voltage
		Q = 1.2*5 		# battery capacity (Ah)
		A = 0.66  		# exponential zone amplitude (V)
		B = 2884.61  	# exponential zone time constant inverse (Ah)−1
		R = 0.25        # internal resistance(Ω)
		dt = 1/60       # hours
		ib = np.array([0, -179])
		Vb = V0 - R*ib[0] - K*(Q/(Q + sum(ib*dt))) + A*exp(B*sum(ib*dt))
		SOC = 100*(1 + sum(ib*dt)/Q)
		print(Vb)
		print(SOC)


if __name__ == "__main__":
	bat = Battery()
