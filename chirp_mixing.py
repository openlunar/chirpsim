import numpy as np
import matplotlib.pyplot as plt

t_max = 1

# chirp signal characteristics
bw = 50
f_center = 50
f_min = f_center - 0.5 * bw
f_max = f_center + 0.5 * bw
f_rate = 150

# lo characteristics
lo_f = 100

size = 10000

x = np.linspace(0.0, t_max, size)
signal = np.zeros(size)
lo = np.zeros(size)
output = np.zeros(size)

delta_t = t_max / size

f_scan = 0
angle = 0

for index, t in np.ndenumerate(x):

    f = f_min + f_scan % (f_max - f_min)

    signal[index] = np.sin(angle)
    lo[index] = np.sin(t*2*np.pi*lo_f)

    output[index] = signal[index] * lo[index]

    angle = angle + delta_t*2*np.pi*f
    f_scan = (f_scan + delta_t*f_rate)




ax1 = plt.subplot(311)
plt.plot(x, signal)

ax2 = plt.subplot(312, sharex=ax1)
plt.plot(x, lo)

ax3 = plt.subplot(313, sharex=ax2)
plt.plot(x, output)

plt.show()
