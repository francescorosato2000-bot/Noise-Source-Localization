import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

def tonalNoise(nBlades, fRot, nHarmonics=5, amplitude=1, t=None, duration=None, fS=None):
    BPF = nBlades * fRot
    if t is None:
        if duration is None:
            duration = 2
        if fS is None:
            fS = 10 * BPF
            
    t = np.linspace(0, duration, int(duration * fS))
            
    y = np.zeros_like(t)
    for n in range(1, nHarmonics + 1):
        y += 1/n * amplitude * np.sin(2 * np.pi * n * BPF * t)
    return y
    
def broadbandNoise(fCutoff=200, amplitude=1, duration=None, fS=None, filterOrder=4, seed=None):
    if seed is not None:
        np.random.seed(seed)
        
    if duration is None:
        duration = 2
        
    if fS is None:
        fS = 10 * fCutoff
    
    whiteNoise = np.random.randn(int(duration * fS))
    nyquist = fS / 2
    normalizedCutoff = fCutoff / nyquist
    b, a = butter(filterOrder, normalizedCutoff, btype='low')
    coloredNoise = filtfilt(b, a, whiteNoise)
    coloredNoise *= amplitude / np.std(coloredNoise)
    
    return coloredNoise
    
def combineSignals(tonal, broadband, amplitude, alpha=0.7):
    if len(tonal) != len(broadband):
        raise ValueError("Tonal and broadband signals must have the same length.")
        
    sourceSignal = alpha * tonal + (1 - alpha) * broadband
    sourceSignal /= np.max(np.abs(sourceSignal))
    sourceSignal *= amplitude
    
    return sourceSignal
    
tonal = tonalNoise(2, 50, nHarmonics=5, duration=2, fS=5000)
broadband = broadbandNoise(fCutoff=500, duration=2, fS=5000)
sourceSignal = combineSignals(tonal, broadband, amplitude=3, alpha=0.7)
plt.plot(sourceSignal[:1000])
plt.title("Combined source signal")
plt.show()
    
