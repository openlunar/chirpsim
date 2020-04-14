import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfilt
import argparse

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], btype='band', output='sos')
    return sos

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    sos = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sosfilt(sos, data)
    return y

def main(args):
    # total simulation time
    t_max = args.t_max
    
    # chirp signal characteristics
    bw = args.bw
    f_center = args.f_center
    f_min = f_center - 0.5 * bw
    f_max = f_center + 0.5 * bw
    f_rate = args.f_rate
    
    # doppler shift
    doppler = args.doppler/100.0  # >=0, 0 = 0%, 1 = 100%
    
    # lo characteristics
    lo_f = args.lo_f  # hz
    lo_f_shifted = lo_f + (lo_f + f_center)*doppler
    
    # phase shift of de-mixing lo
    phase = args.phase/360.0  # 0-1, 0 = 0 deg, 1 = 360 deg
    
    # number of timesteps
    size = args.size
    
    # end-filter params
    lowcut_shifted = (lo_f + f_min)*(1+doppler) - lo_f_shifted
    highcut_shifted = (lo_f + f_max)*(1+doppler) - lo_f_shifted
    lowcut_uncorrected = (lo_f + f_min)*(1+doppler) - lo_f
    highcut_uncorrected = (lo_f + f_max)*(1+doppler) - lo_f
    
    x = np.linspace(0.0, t_max, size)
    shifted_x = np.zeros(size)
    #shifted_lo = np.zeros(size)
    
    signal = np.zeros(size)
    lo = np.zeros(size)
    output = np.zeros(size)
    
    decode_lo = np.zeros(size)
    demixed = np.zeros(size)
    demixed_uncorrected = np.zeros(size)
    
    delta_t = t_max / size
    fs = 1/delta_t
    
    f_scan = 0
    angle = 0
    
    for index, t in np.ndenumerate(x):
    
        f = f_min + f_scan % (f_max - f_min)
    
        signal[index] = np.sin(angle)
        lo[index] = np.sin(t*2*np.pi*lo_f)
        output[index] = signal[index] * lo[index]
    
        shifted_x[index] = t * (1+doppler)
    
        angle = angle + delta_t*2*np.pi*f
        f_scan = (f_scan + delta_t*f_rate)
    
    output_filtered = butter_bandpass_filter(output, lo_f + f_min, lo_f + f_max, fs, order=6)
    output_filtered = output_filtered/max(abs(output_filtered))
    
    shifted_output = np.interp(shifted_x, x, output_filtered, right=0)
    phase_offset = phase * 2 * np.pi
    
    for index, t in np.ndenumerate(x):
        
        decode_lo[index] = np.sin(t*2*np.pi*(lo_f_shifted) + phase_offset)
        demixed[index] = shifted_output[index] * decode_lo[index]
        demixed_uncorrected[index] = shifted_output[index] * lo[index]
    
    demixed_filtered = butter_bandpass_filter(demixed, lowcut_shifted, highcut_shifted, fs, order=6)
    demixed_filtered = demixed_filtered/max(abs(demixed_filtered))
    demixed_uncorrected_filtered = butter_bandpass_filter(demixed_uncorrected, lowcut_uncorrected, highcut_uncorrected, fs, order=6)
    demixed_uncorrected_filtered = demixed_uncorrected_filtered/max(abs(demixed_uncorrected_filtered))
    
    # fft setup and plotting
    fft_size = size*10
    Y_signal = np.abs(np.fft.rfft(signal, n=fft_size))
    Y_encode_lo = np.abs(np.fft.rfft(lo, n=fft_size))
    Y_output = np.abs(np.fft.rfft(output_filtered, n=fft_size))
    Y_shifted_output = np.abs(np.fft.rfft(shifted_output, n=fft_size))
    Y_demixed_filtered = np.abs(np.fft.rfft(demixed_filtered, n=fft_size))
    Y_demixed_uncorrected_filtered = np.abs(np.fft.rfft(demixed_uncorrected_filtered, n=fft_size))
    f = np.fft.rfftfreq(fft_size, delta_t)
    
    plt.plot(f, Y_signal)
    plt.plot(f, Y_encode_lo, 'tab:orange')
    plt.plot(f, Y_output, 'tab:green')
    plt.plot(f, Y_shifted_output, 'tab:red')
    plt.plot(f, Y_demixed_filtered, 'tab:purple')
    plt.plot(f, Y_demixed_uncorrected_filtered, 'tab:cyan')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(f_min/10, f_max*10)
    
    # time domain plotting
    fig, axs = plt.subplots(8, 1, constrained_layout=True)
    axs[0].plot(x, signal)
    axs[0].set_title('Chirp ' + str(f_center) + 'hz center, ' + str(bw) + 'hz BW')
    axs[1].plot(x, lo, 'tab:orange')
    axs[1].set_title('LO ' + str(lo_f) + 'hz')
    axs[2].plot(x, output_filtered, 'tab:green')
    axs[2].set_title('Mixed Signal')
    axs[3].plot(x, shifted_output, 'tab:red')
    axs[3].set_title('Mixed Signal w/ ' + str(doppler*100) + '% Doppler Shift')
    axs[4].plot(x, demixed, 'tab:purple')
    axs[4].set_title('De-Mixed Signal (doppler corrected LO)')
    axs[5].plot(x, demixed_filtered, 'tab:purple')
    axs[5].set_title('^ w/ BP Filter')
    axs[6].plot(x, demixed_uncorrected, 'tab:cyan')
    axs[6].set_title('De-Mixed Signal (original LO)')
    axs[7].plot(x, demixed_uncorrected_filtered, 'tab:cyan')
    axs[7].set_title('^ w/ BP Filter')
    
    for ax in axs.flat:
        ax.set(xlabel='Time (Seconds)', ylabel='Amplitude')
        ax.label_outer() # Hide x labels and tick labels for top plots and y ticks for right plots.
        ax.set_ylim(-1, 1)
    
    plt.ylim(-1, 1)
    plt.tight_layout(w_pad=0, h_pad=0)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-t', '--t-maxx', type=float, dest='t_max', default=1.0,
                        help='total simulation time')
    parser.add_argument('-s', '--time-steps', type=int, dest='size', default=300000,
                        help='number of timesteps')
    parser.add_argument('-d', '--doppler', type=float, dest='doppler', default=25.0,
                        help='amount of doppler shifting to apply to the chirp signal, in percent')

    chirp_chars = parser.add_argument_group('chirp_chars', 'chirp signal characteristics')
    chirp_chars.add_argument('-bw', '--bandwidth', type=float, dest='bw', default=100.0,
                        help='bandwidth of the chirp signal, in hz')
    chirp_chars.add_argument('-fc', '--center-frequency', type=float, dest='f_center', default=200.0,
                        help='center frequency of the chirp signal, in hz')
    chirp_chars.add_argument('-fr', '--frequency-rate', type=float, dest='f_rate', default=300.0,
                        help='rate that the chirp spans its bandwidth, in hz/s')
    
    lo_chars = parser.add_argument_group('lo_chars', 'lo signal characteristics')
    lo_chars.add_argument('-lf', '--lo-frequency', type=float, dest='lo_f', default=600.0,
                        help='frequency of the lo signal, in hz')
    lo_chars.add_argument('-lp', '--lo-phase', type=float, dest='phase', default=90.0,
                        help='phase shift of the demixing lo, from the mixing lo, in deg')
    
    args = parser.parse_args()
    main(args)