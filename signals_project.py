# importing packages
import numpy as np
from scipy.fft import  rfft
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

# constants
F_s=200
DURATION=2
CUTOFF_LOW=10  #frequency to cutoff on
ORDER= 2       #order of filter, by increasing order we get steeper attentuation

#making signal using signal class
signal_20Hz= Signal(amplitude=1,frequency=20, sampling_rate=F_s, duration=DURATION)
sine_20hz=signal_20Hz.sine()
signal_1Hz= Signal(amplitude=3,frequency=1, sampling_rate=F_s, duration=DURATION)
sine_1hz=signal_1Hz.sine()
signal_10Hz= Signal(amplitude=5,frequency=10, sampling_rate=F_s, duration=DURATION)
sine_10hz=signal_10Hz.sine()


# summing signals together
signal_final= sine_20hz+sine_10hz+sine_1hz

#import MP3 file
mp3_path=f"./mp3_files/names_400hz_noise.mp3"
signal_mp3, Fs=librosa.load(mp3_path,sr=None, mono=True)
signal_shifted = signal_mp3 * (2 ** 31 - 1)  
signal_mp3=signal_shifted.astype(np.int32)
plt.plot(signal_mp3)
plt.xlabel('Time[sec]')
plt.ylabel('Amplitude')
plt.title('Audio Signal Time Domain')
plt.show()

print(Fs)


# applying real fast fourier transform
def real_fourier(signal,sampling_freq):
    N= len(signal)
    normalize= N/2
    rfourier=rfft(signal)
    rfourier_xf = rfftfreq(N, 1.0/sampling_freq)
    rfourier_yf = np.abs(rfourier)/normalize
    return rfourier_xf, rfourier_yf

# plotting fourier transformed signal
xf,yf=real_fourier(signal_mp3,Fs)
plt.plot(xf,yf)
plt.xlabel('Frequency[Hz]')
plt.ylabel('Amplitude')
plt.title('Audio Signal Frequency Domain')
plt.show()

# low pass filter function
def low_pass(signal,cutoff_freq,sampling_freq,order_filter):
    nyq_freq=0.5*sampling_freq
    normalized_cutoff=cutoff_freq/nyq_freq
    b, a= butter(order_filter, normalized_cutoff, btype='low', analog=False, output='ba')
    filtered_sign=filtfilt(b,a,signal)
    return filtered_sign

# high pass filter function
def high_pass(signal,cutoff_freq,sampling_freq,order_filter):
    nyq_freq=0.5*sampling_freq
    normalized_cutoff=cutoff_freq/nyq_freq
    b, a= butter(order_filter, normalized_cutoff, btype='high', analog=False, output='ba')
    filtered_sign=filtfilt(b,a,signal)
    return filtered_sign

# notch filter
def notch_filter(signal, notch_freq, sampling_freq, quality_factor=30):
    nyq_freq = 0.5 * sampling_freq
    normalized_freq = notch_freq / nyq_freq
    b, a = iirnotch(normalized_freq, quality_factor)
    filtered_sign = filtfilt(b, a, signal)
    return filtered_sign


def plot_notch_response(notch_freq, sampling_freq, quality_factor=30):
    nyq_freq = 0.5 * sampling_freq
    normalized_freq = notch_freq / nyq_freq
    b, a = iirnotch(normalized_freq, quality_factor)
    
    freq, h = freqz(b, a, fs=sampling_freq)
    
    plt.figure(figsize=(10, 4))
    plt.plot(freq, 20 * np.log10(abs(h)))
    plt.axvline(x=notch_freq, color='r', linestyle='--', label=f'Notch at {notch_freq} Hz')
    plt.title('Notch Filter Frequency Response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.legend()
    plt.grid(True)
    plt.show()


plot_notch_response(notch_freq=400, sampling_freq=44100, quality_factor=10)


notch_signal=notch_filter(signal_mp3,notch_freq=400,sampling_freq=Fs, quality_factor=50)
notch_signal=notch_signal.astype(np.int32)
plt.plot(notch_signal, 'b')
plt.title('Notch Filtered Signal Time Domain')
plt.xlabel('Time[sec]')
plt.ylabel('Amplitude')
plt.show()

notch_x,notch_y=real_fourier(notch_signal,Fs)
plt.plot(notch_x,notch_y)
plt.title('Notch Filtered Signal Frequency Domain')
plt.xlabel('Frequency[Hz]')
plt.ylabel('Amplitude')
plt.show()


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
audio=sign_to_audio(notch_signal,Fs)

#exporting signal
output_path=f"./mp3_files/filtered_names_notch.mp3"
audio.export(out_f=output_path,format="mp3")

