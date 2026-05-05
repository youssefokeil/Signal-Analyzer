# Signal-Analyzer
A signal processing project that reads a WAV audio file, analyzes it in 
both time and frequency domains, and applies an ideal notch filter around 
the peak frequency using FFT/IFFT.

Features:
- Time-domain plot and energy calculation
- Frequency-domain (FFT) plot and energy — verified against Parseval's theorem
- Peak frequency detection
- Ideal notch filter applied at 3 different bandwidths
- Filtered signal reconstructed via IFFT and saved as WAV
