#!/usr/bin/python
# Rate_Error_Vs_Temp.py
# For HO2 + NO 1 sigma
import matplotlib.pyplot as plt
import numpy as np

f_298 =  1.15
g     =  20
A     =  3.3*10E-12
E_R   = -270
K     =  0

temperature_range=[200,210,220,350]

for temperature in temperature_range :
   K[temperature] = A*np.exp(-E_R/temperature)  
   if temperature > 298:
      Upper_bound[temperature] = K[temperature] * (1+ (f_298 * np.exp(g * ( (1/temperature) - (1/298)))) )
      Lower_bound[temperature] = K[temperature] * (1- (f_298 * np.exp(g * ( (1/temperature) - (1/298)))))
   elif temperature < 298:
      Upper_bound[temperature] = K[temperature] * (1+ (f_298 * np.exp(g * ( (1/temperature) - (1/298)))) )
      Lower_bound[temperature] = K[temperature] * (1- (f_298 * np.exp(g * ( (1/temperature) - (1/298)))))

plt.plot(temperature_range, Upper_bound, Lower_bound )
plt.show()
   
