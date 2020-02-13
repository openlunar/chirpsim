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
lo_f = 150

# de-mix lo
phase = 0

size = 30000

x = np.linspace(0.0, t_max, size)
shifted_x = np.zeros(size)
shifted_lo = np.zeros(size)

signal = np.zeros(size)
encode_lo = np.zeros(size)
output = np.zeros(size)

decode_lo = np.zeros(size)
unmixed = np.zeros(size)
unmixed_uncorrected = np.zeros(size)

delta_t = t_max / size

f_scan = 0
angle = 0

doppler = 0.1

for index, t in np.ndenumerate(x):

    f = f_min + f_scan % (f_max - f_min)

    signal[index] = np.sin(angle)
    encode_lo[index] = np.sin(t*2*np.pi*lo_f)
    output[index] = signal[index] * encode_lo[index]

    shifted_x[index] = t * (1+doppler)

    angle = angle + delta_t*2*np.pi*f
    f_scan = (f_scan + delta_t*f_rate)

shifted_output = np.interp(shifted_x, x, output)
phase_offset = phase * 2 * np.pi

for index, t in np.ndenumerate(x):
    
    decode_lo[index] = np.sin(t*2*np.pi*lo_f*(1+doppler) + phase_offset)
    unmixed[index] = shifted_output[index] / decode_lo[index] if decode_lo[index] else 0
    unmixed_uncorrected[index] = shifted_output[index] / encode_lo[index] if encode_lo[index] else 0

# fft setup and plotting
fft_size = size*10
Y_signal = np.abs(np.fft.rfft(signal, n=fft_size))
Y_encode_lo = np.abs(np.fft.rfft(encode_lo, n=fft_size))
Y_output = np.abs(np.fft.rfft(output, n=fft_size))
Y_shifted_output = np.abs(np.fft.rfft(shifted_output, n=fft_size))
Y_unmixed = np.abs(np.fft.rfft(unmixed, n=fft_size))
f = np.fft.rfftfreq(fft_size, delta_t)

plt.plot(f, Y_signal)
plt.xscale('log')
plt.plot(f, Y_encode_lo, 'tab:orange')
plt.xscale('log')
plt.plot(f, Y_output, 'tab:green')
plt.xscale('log')
plt.plot(f, Y_shifted_output, 'tab:red')
plt.xscale('log')
plt.plot(f, Y_unmixed, 'tab:cyan')
plt.xscale('log')
plt.xlim(10, 300)

# time domain plotting
fig, axs = plt.subplots(6, 1)
axs[0].plot(x, signal)
axs[0].set_title('Chirp ' + str(f_center) + 'hz center, ' + str(bw) + 'hz BW')
axs[1].plot(x, encode_lo, 'tab:orange')
axs[1].set_title('LO ' + str(lo_f) + 'hz')
axs[2].plot(x, output, 'tab:green')
axs[2].set_title('Mixed Signal')
axs[3].plot(x, shifted_output, 'tab:red')
axs[3].set_title('Mixed Signal w/ ' + str(doppler*100) + '% Doppler Shift')
axs[4].plot(x, unmixed, 'tab:cyan')
axs[4].set_title('De-Mixed Signal w/ Shifted LO')
axs[5].plot(x, unmixed_uncorrected, 'tab:cyan')
axs[5].set_title('De-Mixed Signal w/ Original LO')

for ax in axs.flat:
    ax.set(xlabel='Time (Seconds)', ylabel='Amplitude')
    ax.label_outer() # Hide x labels and tick labels for top plots and y ticks for right plots.
    ax.set_ylim(-1, 1)

plt.ylim(-1, 1)
plt.tight_layout()
plt.show()
