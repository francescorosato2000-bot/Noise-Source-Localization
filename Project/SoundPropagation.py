import numpy as np

class Obstacle:
    def __init__(self, x=None, y=None, z=None, reflCoeff=0.6, normVec=1):
        if sum(v is not None for v in (x, y, z)) != 1:
            raise ValueError("The obstacle must be specified as a plane through one dimension prescribed (e.g. x=0).")
        if x is not None:
            self.normVec = np.array([1., 0., 0.])
            self.point = np.array([x, 0., 0.])
        elif y is not None:
            self.normVec = np.array([0., 1., 0.])
            self.point = np.array([0., y, 0.])
        else:
            self.normVec = np.array([0., 0., 1.])
            self.point = np.array([0., 0., z])
        self.reflCoeff = reflCoeff
        
    def reflect(self, Point):
        Point = np.asarray(Point)
        n = self.normVec
        Point0 = self.point
    
        return Point - 2 * np.dot(Point - Point0, n) / np.dot(n, n) * n

def computeDelays(xSource, xMics, c=343):
    xSource = np.asarray(xSource)
    xMics = np.asarray(xMics)
    
    dist = np.linalg.norm(xMics - xSource, axis=1)
        
    return dist / c

def applyPropagation(signal, xSource, xMics, fS, sourceAxis=np.array([0, 0, 1]), directivityPower=2, c=343):
    tau = computeDelays(xSource, xMics)
    N = len(tau)
    propSignals = np.zeros((N, len(signal)))
    t = np.arange(len(signal)) / fS
    
    sourceAxis = sourceAxis / np.linalg.norm(sourceAxis)
    vecs = xMics - xSource
    vecs = vecs / np.linalg.norm(vecs, axis=1)[:, None]

    cosTheta = np.clip(np.dot(vecs, sourceAxis), -1, 1)
    theta = np.arccos(cosTheta)
    directivity = np.sin(theta)**directivityPower
    
    for i in range(N):
        tShifted = t - tau[i]

        propSignals[i,:] = directivity[i] * np.interp(t, tShifted, signal, left=0, right=0) / max(tau[i] * c, 1e-6)
    return propSignals

def addMultipath(signal, xSource, xMics, obstacles, fS, c=343, maxReflOrder=1, currentReflOrder=0, currentCoeff=1):
    reflSignal = np.zeros((len(xMics), len(signal)))
    
    if currentReflOrder >= maxReflOrder:
        return reflSignal

    xSource = np.asarray(xSource)
    xMics = np.asarray(xMics)
    
    for obs in obstacles:
        if np.dot(obs.point - xSource, obs.normVec) < 0:
            xSourceRefl = obs.reflect(xSource)
            newCoeff = currentCoeff * obs.reflCoeff

            reflSignal += applyPropagation(signal, xSourceRefl, xMics, fS, directivityPower=0) * newCoeff

            reflSignal += addMultipath(signal, xSourceRefl, xMics, obstacles, fS, 
                                        maxReflOrder=maxReflOrder,
                                        currentReflOrder=currentReflOrder+1,
                                        currentCoeff=newCoeff)
    return reflSignal
    
def addNoise(signal, snrdB=10):
    noisySignals = np.zeros_like(signal)
    
    for i in range(signal.shape[0]):
        sig = signal[i]
        sigRms = np.sqrt(np.mean(sig**2))
        noiseRms = sigRms / (10**(snrdB / 20))
        noise = np.random.randn(len(sig)) * noiseRms
        noisySignals[i] = sig + noise
        
    return noisySignals