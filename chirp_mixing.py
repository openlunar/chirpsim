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

size = 20000

x = np.linspace(0.0, t_max, size)
shifted_x = np.zeros(size)
shifted_lo = np.zeros(size)

signal = np.zeros(size)
encode_lo = np.zeros(size)
output = np.zeros(size)

decode_lo = np.zeros(size)
decoded = np.zeros(size)

delta_t = t_max / size

f_scan = 0
angle = 0

doppler = 0.001

for index, t in np.ndenumerate(x):

    f = f_min + f_scan % (f_max - f_min)

    signal[index] = np.sin(angle)
    encode_lo[index] = np.sin(t*2*np.pi*lo_f)
    output[index] = signal[index] * encode_lo[index]

    shifted_x[index] = t * (1+doppler)

    angle = angle + delta_t*2*np.pi*f
    f_scan = (f_scan + delta_t*f_rate)

shifted_output = np.interp(shifted_x, x, output)

for index, t in np.ndenumerate(x):
    
    decode_lo[index] = np.sin(t*2*np.pi*lo_f*(1+doppler))
    decoded[index] = shifted_output[index] / decode_lo[index] if decode_lo[index] else 0


# ax1 = plt.subplot(511)
# ax1.set_title("kdj")
# plt.plot(x, signal)
#
# ax2 = plt.subplot(512, sharex=ax1, title="kjdfgndf")
# plt.plot(x, encode_lo)
#
# ax3 = plt.subplot(513, sharex=ax2)
# plt.plot(x, output)
#
# ax4 = plt.subplot(514, sharex=ax3)
# plt.plot(x, shifted_output)
#
# ax5 = plt.subplot(515, sharex=ax4)
# plt.plot(x, decoded)


fig, axs = plt.subplots(5, 1)
axs[0].plot(x, signal)
axs[0].set_title('Axis [0,0]')
axs[1].plot(x, encode_lo, 'tab:orange')
axs[1].set_title('Axis [0,1]')
axs[2].plot(x, output, 'tab:green')
axs[2].set_title('Axis [1,0]')
axs[3].plot(x, shifted_output, 'tab:red')
axs[3].set_title('Axis [1,1]')
axs[4].plot(x, decoded, 'tab:red')
axs[4].set_title('Axis [1,1]')


for ax in axs.flat:
    ax.set(xlabel='x-label', ylabel='y-label')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

plt.ylim(-1,1)

plt.show()
