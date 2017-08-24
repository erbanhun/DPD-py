#-*-coding:utf-8 -*-
import numpy as np
import scipy.io
#from numpy import *
import matplotlib.pyplot as plt
""" xx.mat file input
"""
data = scipy.io.loadmat('PA.mat')
print(data.keys())
#print(data['PA_in'])
#print(np.shape(data['PA_in']))
PA_in = data['PA_in'][130: 7030]
PA_out = data['PA_out'][115: 7015]
plt.figure(1)
plt.subplot(211)
plt.plot(np.abs(PA_in), 'r', np.abs(PA_out), 'b') ## photo
print("==============")

"""
    shift and aligned data ================
"""
PA_in = np.reshape(PA_in, len(PA_in))
PA_out = np.reshape(PA_out, len(PA_out))
CORR = np.correlate(np.abs(PA_in), np.abs(PA_out), "full") ## calc corss-correlation

I = np.shape(CORR)
## find max num in CORR & calculate num of lags
max_corr = CORR[1]
k = 1
for i in range( 2, I[0]):
    if (CORR[i] > max_corr):
        max_corr = CORR[i]
        k = i

k = len(PA_in) - k -1
print("shift num: ", k)
## shift the data to aligned
if k>=0:
    PA_out = PA_out[1+k: np.shape(PA_out)[0]]
    PA_in = PA_in[1 : len(PA_out)+1]
else:
    PA_in = PA_in[1-k: np.shape(PA_in)[0]]
    PA_out = PA_out[1 : len(PA_in)+1]

print(len(PA_in), len(PA_out))

plt.figure(2)
plt.plot(np.abs(PA_in), 'r', np.abs(PA_out), 'b')
"""
    Pic
    1. AM_AM
    2. AM_PM
"""
plt.figure(3)
plt.plot(np.abs(PA_in), np.abs(PA_out), 'r.')
plt.figure(4)
plt.plot(np.abs(PA_in), np.angle(PA_out / PA_in) *180 / np.pi, 'b.')

"""
    DPD ==================
    1. input parameter of models
    2. construct H modle of PA & calculate Y_pre & NMSE
    3. construct H_inv model of PA & calculate X_pre
"""
