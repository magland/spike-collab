import h5py
import numpy as np
from mountainlab_pytools import mdaio

class TimeseriesMdaReader:
    def __init__(self,path,*,samplerate):
        self._samplerate=samplerate
        self._mda_path=path
        X=mdaio.DiskReadMda(path)
        self._num_channels=X.N1()
        self._num_timepoints=X.N2()
    def numChannels(self):
        return self._num_channels
    def numTimepoints(self):
        return self._num_timepoints
    def sampleRate(self):
        return self._samplerate
    def getChunk(self,*,trange=None,channels=None):
        if not channels:
            channels=range(1,self._num_channels+1)
        if not trange:
            trange=[0,self._num_timepoints]
        X=mdaio.DiskReadMda(self._mda_path)
        chunk=X.readChunk(i1=0,i2=trange[0],N1=self._num_channels,N2=trange[1]-trange[0])
        return chunk[np.array(channels)-1,:]

class TimeseriesHdf5Reader:
    def __init__(self,path):
        self._hdf5_path=path
        with h5py.File(self._hdf5_path,"r") as f:
            self._num_chunks=f.attrs['num_chunks']
            self._chunk_size=f.attrs['chunk_size']
            self._padding=f.attrs['padding']
            self._num_channels=f.attrs['num_channels']
            self._num_timepoints=f.attrs['num_timepoints']
            self._samplerate=f.attrs['samplerate']
    def numChannels(self):
        return self._num_channels
    def numTimepoints(self):
        return self._num_timepoints
    def sampleRate(self):
        return self._samplerate
    def getChunk(self,*,trange=None,channels=None):
        if not channels:
            channels=range(1,self._num_channels+1)
        if not trange:
            trange=[0,self._num_timepoints]
        t1=trange[0]
        t2=trange[1]
        if (t1<0) or (t2>self.numTimepoints()):
            ret=np.zeros((len(channels),t2-t1))
            t1a=np.maximum(t1,0)
            t2a=np.minimum(t2,self.numTimepoints())
            ret[:,t1a-(t1):t2a-(t1)]=self.getChunk(trange=[t1a,t2a],channels=channels)
            return ret
        else:
            c1=int(t1/self._chunk_size)
            c2=int((t2-1)/self._chunk_size)
            ret=np.zeros((len(channels),t2-t1))
            with h5py.File(self._hdf5_path,"r") as f:
                for cc in range(c1,c2+1):
                    if cc==c1:
                        t1a=t1
                    else:
                        t1a=self._chunk_size*cc
                    if cc==c2:
                        t2a=t2
                    else:
                        t2a=self._chunk_size*(cc+1)
                    for ii in range(len(channels)):
                        m=channels[ii]
                        assert(cc>=0)
                        assert(cc<self._num_chunks)
                        str='parts/channel-{}/chunk-{}'.format(m,cc)
                        offset=self._chunk_size*cc-self._padding
                        ret[ii,t1a-t1:t2a-t1]=f[str][t1a-offset:t2a-offset]
            return ret
