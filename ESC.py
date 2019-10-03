from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import math

t=2   #sample freq= 500=250
N = 500
filterorder = 2;
fs = 5
phase = 0
omega = 5*2*math.pi
dt =0.02
n = [2 * math.pi * fs * t / N for t in range(N)]
x = [math.sin(i) for i in n]
x1 = [math.sin(i*10) for i in n]
xx=[]
for i in range(len(x)):
    xx.append(x[i] + x1[i])

axis_x = np.linspace(0, 1, num=N)
plt.plot(axis_x, xx)
plt.title("5Hz sinswape")
plt.axis('tight')
plt.show()

b, a = signal.butter(filterorder, 0.09, 'highpass')

HPFhis = np.zeros(filterorder+1, dtype = float)
Yout = np.zeros(filterorder+1, dtype = float)
x_passed = np.zeros(len(xx), dtype=float)


for i in range(len(xx)):

    for k in range(1,filterorder+1):
        Yout[k-1] = Yout[k]
        HPFhis[k-1] = HPFhis[k]
     # should using Yout[fiterorder] = J(y_f,y_p,y_i) as input
    Yout[filterorder]=xx[i]
    HPFnew= 0

    for j in range(1,filterorder+2):
        HPFnew = HPFnew + b[j-1]*Yout[filterorder + 1 - j]

    for j in range(2,filterorder+2):
        HPFnew = HPFnew - a[j-1]*HPFhis[filterorder + 1 - j]

    HPFhis[filterorder] = HPFnew
    t_now = t_now+dt
    dr =  HPFnew*math.sin(omega*t_now+phase)

sf = signal.filtfilt(b, a, xx)
plt.subplot(2,1,1)
plt.plot(axis_x,sf)
plt.subplot(2,1,2)
plt.plot(axis_x, x_passed)
plt.title("highpass")
plt.axis('tight')
plt.show()

print(a,b)