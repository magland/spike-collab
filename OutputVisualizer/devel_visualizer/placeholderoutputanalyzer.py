from mountainlab_pytools import mlproc as mlp
from mountainlab_pytools import mdaio
import numpy as np


class PlaceholderOutputAnalyzer:
    def __init__(self,*,timeseries,firings,geom=None,samplerate=30000):
        self._timeseries=timeseries
        self._firings=firings
        self._geom=geom
        self._samplerate=samplerate
    def initialize(self):
        print('Downloading timeseries (if needed): {}'.format(self._timeseries))
        if self._timeseries is not None:
            timeseries_path=mlp.realizeFile(self._timeseries)
        print('Downloading firings (if needed): {}'.format(self._firings))
        firings_path=mlp.realizeFile(self._firings)
        if self._geom is not None:
            print('Downloading geom (if needed): {}'.format(self._geom))
            geom_path=mlp.realizeFile(self._geom)
            self._G=np.genfromtxt(geom_path, delimiter=',').T
            self._G=np.flip(self._G,axis=0)
        else:
            self._G=None
        print('Reading arrays into memory...')
        if self._timeseries is not None:
            self._X=mdaio.readmda(timeseries_path)
        else:
            self._X=None
        self._F=mdaio.readmda(firings_path)
        self._times=self._F[1,:]
        self._labels=self._F[2,:]
        self._K=int(self._labels.max())
        
    def getUnitCount(self):
        return self._K
    def getChannelCount(self):
        return self._X.shape[0]
    def getUnitEventCount(self,*,unit):
        inds0=np.where(self._labels==unit)[0]
        return len(inds0)
    def getUnitEventTimes(self,*,unit):
        inds0=np.where(self._labels==unit)[0]
        return self._times[inds0]
    def getUnitEventWaveforms(self,*,unit,event_indices=None,channels=None,clip_size=50):
        inds0=np.where(self._labels==unit)[0]
        times0=self._times[inds0]
        if event_indices is not None:
            times0=times0[event_indices]
        spikes=self._extract_clips(self._X,times=times0,clip_size=clip_size)
        if channels is not None:
            spikes=spikes[np.array(channels)-1,:,:]
        return spikes
    def getElectrodeLocations(self):
        if self._G is not None:
            return self._G
        M=self.getChannelCount()
        channel_locations=np.zeros((2,M))
        for m in range(1,M+1):
            channel_locations[:,m-1]=[0,-m]
        return channel_locations
    def sampleRate(self):
        return self._samplerate
        
    def _extract_clips(self,timeseries,*,times,clip_size):
        M=timeseries.shape[0]
        T=clip_size
        L=len(times)
        Tmid = int(np.floor((T + 1) / 2) - 1);
        clips=np.zeros((M,T,L),dtype='float32')
        for j in range(L):
            t1=int(times[j]-Tmid)
            t2=int(t1+clip_size)
            clips[:,:,j]=timeseries[:,t1:t2]
        return clips

    #def _sample_spikes(timeseries,firings,max_spikes_per_unit=20,clip_size=100):
    #    M=timeseries.shape[0]
    #    times=firings[1,:]
    #    labels=firings[2,:]
    #    K=int(labels.max())
    #    units=[]
    #    for k in range(1,K+1):
    #        unit={}
    #        inds_k=np.where(labels==k)[0]
    #        if len(inds_k>max_spikes_per_unit):
    #            inds_k=np.random.choice(inds_k,max_spikes_per_unit,replace=False)
    #        unit['spikes']=extract_clips(timeseries,times=times[inds_k],clip_size=clip_size)    
    #        units.append(unit)
    #    return dict(
    #        units=units
    #    )
    

    