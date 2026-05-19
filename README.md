# Signal-Analyzer
A signal processing project that reads an MP3 audio file, analyzes it in both time and frequency domains, detects the dominant noise frequency, and removes it using a notch filter.

## Features
- Time-domain plot and visualization
- Frequency-domain (FFT) analysis
- Automatic peak frequency detection
- Notch filter applied at the detected noise frequency
- Filtered signal exported as MP3

## Figures

### 1. Audio Signal — Time Domain
![Audio Signal Time Domain](https://github.com/youssefokeil/Signal-Analyzer/blob/main/figures/audio_signal_time_domain.png?raw=true)

The raw audio signal plotted in the time domain after loading from the MP3 file. 

---

### 2. Audio Signal — Frequency Domain
![Audio Signal Frequency Domain](https://github.com/youssefokeil/Signal-Analyzer/blob/main/figures/audio_signal_frequency_domain.png?raw=true)

The FFT of the original signal showing the frequency content. A dominant noise should be at 400hz.

---

### 3. Zoomed Around 400 Hz
![Zoomed Around 400 Hz](https://github.com/youssefokeil/Signal-Analyzer/blob/main/figures/zoomed_around_400_hz.png?raw=true)

A zoomed-in view of the FFT between 350–450 Hz to precisely identify the noise frequency. This confirmed the peak at around **410 Hz** rather than 400 Hz.

---

### 4. Notch Filter Frequency Response
![Notch Filter Frequency Response](https://github.com/youssefokeil/Signal-Analyzer/blob/main/figures/ideal_notch_filter_frequency_response.png?raw=true)

We made an ideal notch filter that zeroes out at the desired frequency with a passed bandwidth. This will be passed for 8 harmonics like this:
```
Zeroed harmonic 1: 409.98 Hz
Zeroed harmonic 2: 819.95 Hz
Zeroed harmonic 3: 1229.93 Hz
Zeroed harmonic 4: 1639.90 Hz
Zeroed harmonic 5: 2049.88 Hz
Zeroed harmonic 6: 2459.86 Hz
Zeroed harmonic 7: 2869.83 Hz
Zeroed harmonic 8: 3279.81 Hz
```
---

### 5. Notch Filtered Signal — Time Domain
![Notch Filtered Signal Time Domain](https://github.com/youssefokeil/Signal-Analyzer/blob/main/figures/ideal_notch_filtered_signal_time_domain.png?raw=true)

The filtered signal in the time domain after applying the ideal notch filter. The overall shape of the signal is preserved while the 410 Hz noise component is removed. After removing it for multiple harmonics.

---

### 6. Notch Filtered Signal — Frequency Domain
![Notch Filtered Signal Frequency Domain](https://github.com/youssefokeil/Signal-Analyzer/blob/main/figures/ideal_notch_filtered_signal_frequency_domain.png?raw=true)

The FFT of the filtered signal confirming the 410 Hz peak has been successfully removed a big part of it. The rest of the frequency content remains intact. After removing it for multiple harmonics.

---


## Requirements

```
numpy
scipy
plotly
matplotlib
librosa
pydub
```

Install with:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
