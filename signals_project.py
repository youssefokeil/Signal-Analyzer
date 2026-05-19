# importing packages
import numpy as np
from scipy.fft import  rfft,irfft
from scipy.fft import  rfftfreq
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.signal import butter,filtfilt, iirnotch, freqz
# importing signal used to make sine wave
from Signal_Generator_class import Signal 
import librosa
from pydub import AudioSegment


BANDWIDTH = 5

# helper function to save plots 
def save_and_show():
    title = plt.gca().get_title()
    filename = title.lower().replace(' ', '_') + '.png'
    plt.savefig(f'./figures/{filename}', dpi=150, bbox_inches='tight')
    plt.show()

#import MP3 file
mp3_path=f"./mp3_files/names_400hz_noise.mp3"
signal_mp3, Fs=librosa.load(mp3_path,sr=None, mono=True)
plt.plot(signal_mp3)
plt.xlabel('Time[sec]')
plt.ylabel('Amplitude')
plt.title('Audio Signal Time Domain')
save_and_show()

print(Fs)


# applying real fast fourier transform
def real_fourier(signal,sampling_freq):
    N= len(signal)
    normalize= N/2
    rfourier=rfft(signal)
    rfourier_xf = rfftfreq(N, 1.0/sampling_freq)
    rfourier_yf = np.abs(rfourier)/normalize

    mask = (rfourier_xf >= 100) & (rfourier_xf <= 2000)
    peak_freq = rfourier_xf[mask][np.argmax(rfourier_yf[mask])]
    
    return rfourier_xf, rfourier_yf, peak_freq


# plotting fourier transformed signal
xf,yf, peak_freq=real_fourier(signal_mp3,Fs)
plt.plot(xf,yf)
plt.xlabel('Frequency[Hz]')
plt.ylabel('Amplitude')
plt.title('Audio Signal Frequency Domain')
save_and_show()

mask = (xf >= 350) & (xf <= 450)
plt.plot(xf[mask], yf[mask], label=peak_freq)
plt.title('Zoomed around 400 Hz')
plt.legend()
save_and_show()

# ideal notch filter
def ideal_notch_filter(signal, notch_freq, sampling_freq, bandwidth=10, num_harmonics=1): # add harmonics as optional
    N = len(signal)
    fft_signal = rfft(signal)
    freqs = rfftfreq(N, 1.0/sampling_freq)

    print(f"For Bandwidth={BANDWIDTH}")
    # zero out bins within bandwidth around notch frequency
    for i in range(1, num_harmonics + 1):
        harmonic = notch_freq * i
        mask = (freqs >= harmonic - bandwidth/2) & (freqs <= harmonic + bandwidth/2)
        fft_signal[mask] = 0
        print(f"Zeroed harmonic {i}: {harmonic:.2f} Hz")
    
    # inverse FFT to get back time domain signal
    filtered_signal = np.real(irfft(fft_signal, n=N))
    return filtered_signal


# to plot the ideal notch
def plot_ideal_notch_response(notch_freq, sampling_freq, bandwidth=10):
    N = 44100  # 1 second of samples for visualization
    freqs = rfftfreq(N, 1.0/sampling_freq)
    
    response = np.ones(len(freqs))
    mask = (freqs >= notch_freq - bandwidth/2) & (freqs <= notch_freq + bandwidth/2)
    response[mask] = 0
    
    plt.figure(figsize=(10, 4))
    plt.plot(freqs, 20 * np.log10(np.clip(response, 1e-10, None)))
    plt.axvline(x=notch_freq, color='r', linestyle='--', label=f'Notch at {notch_freq} Hz')
    plt.axvline(x=notch_freq - bandwidth/2, color='g', linestyle='--', label=f'Lower edge: {notch_freq - bandwidth/2} Hz')
    plt.axvline(x=notch_freq + bandwidth/2, color='b', linestyle='--', label=f'Upper edge: {notch_freq + bandwidth/2} Hz')
    plt.title(f'Ideal Notch Filter Frequency Response for Bandwidth = {BANDWIDTH}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.xlim(notch_freq - 100, notch_freq + 100)  # zoom around notch
    plt.legend()
    plt.grid(True)
    save_and_show()


plot_ideal_notch_response(notch_freq=peak_freq, sampling_freq=44100, bandwidth=BANDWIDTH)

notch_signal = ideal_notch_filter(signal_mp3, notch_freq=peak_freq, sampling_freq=Fs, bandwidth=BANDWIDTH, num_harmonics=7)

plt.plot(notch_signal, 'b')
plt.title(f'Ideal Notch Filtered Signal Time Domain Bandwidth={BANDWIDTH}')
plt.xlabel('Time[sec]')
plt.ylabel('Amplitude')
save_and_show()

notch_x,notch_y,_=real_fourier(notch_signal,Fs)
plt.plot(notch_x,notch_y)
plt.title(f'Ideal Notch Filtered Signal Frequency Domain Bandwidth={BANDWIDTH}')
plt.xlabel('Frequency[Hz]')
plt.ylabel('Amplitude')
save_and_show()


#turn signal to audio
def sign_to_audio(signal,sampling_rate):
    channels = 2 if (signal.ndim == 2 and signal.shape[1] == 2) else 1
    audio = AudioSegment(
        signal.tobytes(),
        frame_rate=sampling_rate,
        sample_width=4,
        channels=channels
    )
    return audio

audio_signal = np.clip(notch_signal, -1.0, 1.0)
audio_signal = (audio_signal * (2**31 - 1)).astype(np.int32)
audio = sign_to_audio(audio_signal, Fs)

#exporting signal
output_path=f"./mp3_files/filtered_names_notch_bandwidth_{BANDWIDTH}.mp3"
audio.export(out_f=output_path,format="mp3")

