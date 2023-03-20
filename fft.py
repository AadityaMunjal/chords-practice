import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (9, 7)

sampFreq, sound = wavfile.read('C2 Note.wav')

print(sound.dtype, sampFreq)

sound = sound / 2.0**15


length_in_s = sound.shape[0] / sampFreq
print("length ", length_in_s)


# plt.subplot(2,1,1)
# plt.plot(sound[:,0], 'r')
# plt.xlabel("left channel, sample #")
# plt.subplot(2,1,2)
# plt.plot(sound[:,1], 'b')
# plt.xlabel("right channel, sample #")
# plt.tight_layout()
# plt.show()

time = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s

# plt.subplot(2,1,1)
# plt.plot(time, sound[:,0], 'r')
# plt.xlabel("time, s [left channel]")
# plt.ylabel("signal, relative units")
# plt.subplot(2,1,2)
# plt.plot(time, sound[:,1], 'b')
# plt.xlabel("time, s [right channel]")
# plt.ylabel("signal, relative units")
# plt.tight_layout()
# plt.show()

# single channel
signal = sound[:,0]

# plt.plot(time[6000:7000], signal[6000:7000])
# plt.xlabel("time, s")
# plt.ylabel("Signal, relative units")
# plt.show()

fft_spectrum = np.fft.rfft(signal)
freq = np.fft.rfftfreq(signal.size, d=1./sampFreq)

fft_spectrum_abs = np.abs(fft_spectrum)

# plt.plot(freq, fft_spectrum_abs)
# plt.xlabel("frequency, Hz")
# plt.ylabel("Amplitude, units")
# plt.show()

# plt.plot(freq[:2500], fft_spectrum_abs[:2500])
# plt.xlabel("frequency, Hz")
# plt.ylabel("Amplitude, units")
# plt.show()

fft_spectrum_abs_threshed = np.array([])
threshed_frequency_amplitude = np.array([])

for i,f in enumerate(fft_spectrum_abs):
    if f > 350: #looking at amplitudes of the spikes higher than 350 

        # print('frequency = {} Hz with amplitude {} '.format(np.round(freq[i],1),  np.round(f)))

        fft_spectrum_abs_threshed = np.append(fft_spectrum_abs_threshed, freq[i])
        threshed_frequency_amplitude = np.append(threshed_frequency_amplitude, f)
print(fft_spectrum_abs_threshed)


def merge_similar_elements(frequencies, amplitudes):
    
    MAX_VARIANCE = 10

    merged_arr = np.array([])
    curr_freq_arr = np.array([])
    curr_ampl_arr = np.array([])

    for idx, val in enumerate(frequencies):
      freq, ampl = val, amplitudes[idx]
      curr_freq_arr = np.append(curr_freq_arr, freq)
      curr_ampl_arr = np.append(curr_ampl_arr, ampl)
      curr_freq_variance = np.var(curr_freq_arr)

      if curr_freq_variance > MAX_VARIANCE:
          # remove the last added element 
          curr_freq_arr = np.delete(curr_freq_arr, -1)
          curr_ampl_arr = np.delete(curr_ampl_arr, -1)

          freq_mean_val = np.mean(curr_freq_arr)
          ampl_mean_val = np.mean(curr_ampl_arr)

          merged_arr = np.append(merged_arr, np.array([freq_mean_val, ampl_mean_val]))
          curr_freq_arr = np.array([freq,])
          curr_ampl_arr = np.array([ampl,])

    
    merged_arr = np.append(merged_arr, np.array([np.mean(curr_freq_arr), np.mean(curr_ampl_arr)]))

    return merged_arr.reshape((len(merged_arr)//2, 2))



grouped_freqs = merge_similar_elements(fft_spectrum_abs_threshed, threshed_frequency_amplitude)
print(grouped_freqs)

# [[freq, ampl]]

# C Major
# [[261.         616.94534288]
#  [329.16666667 546.15757295]
#  [391.66666667 495.8582191 ]]

# C4 Note
# [[261.22222222 671.9677272 ]]