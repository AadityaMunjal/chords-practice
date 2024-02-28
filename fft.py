import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

plt.rcParams["figure.dpi"] = 100
plt.rcParams["figure.figsize"] = (9, 7)

sampFreq, sound = wavfile.read("Piano C Major2.wav")

print(sound.dtype, sampFreq)

sound = sound / 2.0**15


length_in_s = sound.shape[0] / sampFreq

time = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s

# single channel
signal = sound[:, 0]
fft_spectrum = np.fft.rfft(signal)
freq = np.fft.rfftfreq(signal.size, d=1.0 / sampFreq)

fft_spectrum_abs = np.abs(fft_spectrum)

fft_spectrum_abs_threshed = np.array([])
threshed_frequency_amplitude = np.array([])

ampl_cuttoff_thresh = 100
for i, f in enumerate(fft_spectrum_abs):
    if f > ampl_cuttoff_thresh:  # looking at amplitudes of the spikes higher than 350

        fft_spectrum_abs_threshed = np.append(fft_spectrum_abs_threshed, freq[i])
        threshed_frequency_amplitude = np.append(threshed_frequency_amplitude, f)


# plt.plot(fft_spectrum_abs_threshed[:2500], threshed_frequency_amplitude[:2500])
# plt.xlabel("frequency, Hz")
# plt.ylabel("Amplitude, units")
# plt.show()


def weighted_frequency_merge(frequencies, amplitudes):
    MAX_VARIANCE = 10

    curr_freq_arr = np.array([])
    curr_ampl_arr = np.array([])

    note_freqs = np.array([])

    for idx, val in enumerate(frequencies):
        freq, ampl = val, amplitudes[idx]
        curr_freq_arr = np.append(curr_freq_arr, freq)
        curr_ampl_arr = np.append(curr_ampl_arr, ampl)
        curr_freq_variance = np.var(curr_freq_arr)

        if curr_freq_variance > MAX_VARIANCE:
            # remove the last added element
            curr_freq_arr = np.delete(curr_freq_arr, -1)
            curr_ampl_arr = np.delete(curr_ampl_arr, -1)

            weights = curr_ampl_arr**2
            freq_mean_val = np.average(curr_freq_arr, weights=weights)
            note_freqs = np.append(note_freqs, freq_mean_val)

            # reset arrays for next note
            curr_freq_arr = np.array(
                [
                    freq,
                ]
            )
            curr_ampl_arr = np.array(
                [
                    ampl,
                ]
            )

    # add last note
    weights = curr_ampl_arr**2
    note_freqs = np.append(note_freqs, np.average(curr_freq_arr, weights=weights))

    return note_freqs


grouped_freqs = weighted_frequency_merge(
    fft_spectrum_abs_threshed, threshed_frequency_amplitude
)

print(grouped_freqs)


def convert_frequencies(note_freqs):
    # A4 = 440 Hz
    A4 = 440
    C0 = A4 * 2 ** (-4.75)
    name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    h = 12 * np.log2(note_freqs / C0)
    octave = np.floor(h / 12)
    n = np.floor(h) % 12
    return name[int(n)], int(octave)


for freq in grouped_freqs:
    note, octave = convert_frequencies(freq)
    print(f"{note}{int(octave)}")
