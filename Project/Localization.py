import numpy as np

def beamforming(signals, xMics, gridPoints, fS, c=343):
    nMics, nSamples = signals.shape
    nPoints = gridPoints.shape[0]
    energyMap = np.zeros(nPoints)
    
    for i, xGuess in enumerate(gridPoints):
        tau = np.linalg.norm(xMics - xGuess, axis=1) / c
        alignedSignals = np.zeros(nSamples)
        t = np.arange(nSamples) / fS
        for j in range(nMics):
            idxDelay = int(np.round(tau[j]*fS))
            alignedSignals[idxDelay:] += signals[j][:nSamples-idxDelay]
        energyMap[i] = np.sum(alignedSignals**2)
    
    bestIndex = np.argmax(energyMap)
    xEst = gridPoints[bestIndex]
    return xEst, energyMap
