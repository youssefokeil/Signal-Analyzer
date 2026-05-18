# importing packages
import numpy as np
from scipy.fft import  rfft
from scipy.fft import  rfftfreq
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from scipy.signal import butter,filtfilt
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
mp3_path=f"record/audio.mp3"
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


hpf_signal=high_pass(signal_mp3,30,Fs,10)
hpf_signal=hpf_signal.astype(np.int32)
plt.plot(hpf_signal, 'b')
plt.title('HPFiltered Signal Time Domain')
plt.xlabel('Time[sec]')
plt.ylabel('Amplitude')
plt.show()

hpf_x,hpf_y=real_fourier(hpf_signal,Fs)
plt.plot(hpf_x,hpf_y)
plt.title('HPFiltered Signal Frequency Domain')
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
audio=sign_to_audio(hpf_signal,Fs)

#exporting signal
output_path=f"./MP3 files/filtered_names_hpf.mp3"
audio.export(out_f=output_path,format="mp3")

