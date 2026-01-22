import numpy as np
import matplotlib.pyplot as plt
from AeroacousticSource import tonalNoise, broadbandNoise, combineSignals
from SoundPropagation import Obstacle, applyPropagation, addMultipath, addNoise
from Localization import beamforming

fS = 1000
duration = 1.0
nMics = 4

# Posizioni dei microfoni sul piano xz (y=0)
xMics = np.array([
    [0, 0, 0], 
    [5, 0, 0], 
    [0, 0, 3], 
    [5, 0, 3]
])

# Sorgente
xSource = np.array([0.5, 0, 0.5])  # (x,z)

# Genera segnale sorgente
tonal = tonalNoise(2, 50, fS=fS, duration=duration)
broadband = broadbandNoise(fS=fS, duration=duration)
sourceSignal = combineSignals(tonal, broadband, amplitude=1)

# Ostacoli (muri verticali)
obstacles = [Obstacle(x=0), Obstacle(x=5)]

# Propagazione diretta
propSignals = applyPropagation(sourceSignal, xSource, xMics, fS)

# Aggiunta multipath
propSignals += addMultipath(sourceSignal, xSource, xMics, obstacles, fS, maxReflOrder=1)

# Aggiunta rumore
propSignals = addNoise(propSignals, snrdB=10)

# Griglia beamforming sul piano xz
xGrid = np.linspace(0, 5, 500)
yGrid = np.asarray([0])
zGrid = np.linspace(0, 3, 300)
X, Y, Z = np.meshgrid(xGrid, yGrid, zGrid)
gridPoints = np.vstack([X.ravel(), Y.ravel(), Z.ravel()]).T

# Beamforming
xEst, J = beamforming(propSignals, xMics, gridPoints, fS)

# Trova massimo (stima sorgente)
idxMax = np.argmax(J)
xEst = gridPoints[idxMax]
print("True source:", xSource)
print("Estimated source:", xEst)

# Visualizza mappa beamforming
#plt.figure()
#plt.pcolormesh(X, Z, J.reshape(X.shape), shading='auto')
#plt.scatter(xMics[:,0], xMics[:,1], c='r', label='Mics')
#plt.scatter(xSource[0], xSource[1], c='g', label='True Source')
#plt.scatter(xEst[0], xEst[1], c='b', label='Estimated Source')
#plt.xlabel('x [m]')
#plt.ylabel('z [m]')
#plt.title('Beamforming map')
#plt.legend()
#plt.colorbar(label='Beamforming cost')
#plt.show()
