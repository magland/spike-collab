from SortingAPI import InputExtractor
from SortingAPI import OutputExtractor

from mountainlab_pytools import mlproc as mlp
from mountainlab_pytools import mdaio
import os, json
import numpy as np

class MdaInputExtractor(InputExtractor):
    def __init__(self, dataset_directory, download=True):
        InputExtractor.__init__(self)
        self._dataset_directory=dataset_directory
        timeseries0=dataset_directory+'/raw.mda'
        if download:
            print('Downloading file if needed: '+timeseries0)
            self._timeseries_path=mlp.realizeFile(timeseries0)
            print('Done.')
        else:
            self._timeseries_path=mlp.locateFile(timeseries0)
        X=mdaio.DiskReadMda(self._timeseries_path)
        self._num_channels=X.N1()
        self._num_timepoints=X.N2()
        self._dataset_params=read_dataset_params(dataset_directory)
        self._samplerate=self._dataset_params['samplerate']
        
    def extractRawTraces(self, t_start=None, t_end=None, electrode_ids=None):
        X=mdaio.DiskReadMda(self._timeseries_path)
        recordings=X.readChunk(i1=0,i2=t_start,N1=X.N1(),N2=t_end-t_start)
        times=np.arange(t_start,t_end)/self._samplerate
        return recordings, times
    
    def getSamplingFrequency(self):
        return self._samplerate
    
    def getProbeInformation(self):
        raise NotImplementedError("The getProbeInformation function is not \
                                  implemented for this extractor")

class MdaOutputExtractor(OutputExtractor):
    def __init__(self, firings_fname):
        OutputExtractor.__init__(self)
        print('Downloading file if needed: '+firings_fname)
        self._firings_path=mlp.realizeFile(firings_fname)
        print('Done.')
        self._firings=mdaio.readmda(self._firings_path)
        self._times=self._firings[1,:]
        self._labels=self._firings[2,:]
        self._num_units=np.max(self._labels)
        
    def getNumUnits(self):
        return self._num_units

    def getUnitSpikeTimes(self, unit_id, t_start=None, t_stop=None):
        if t_start is None:
            t_start=0
        if t_stop is None:
            t_stop=np.Inf
        inds=np.where((self._labels==unit_id)&(t_start<=self._times)&(self._times<t_stop))
        return self._times[inds]
    
def read_dataset_params(dsdir):
    params_fname=mlp.realizeFile(dsdir+'/params.json')
    if not os.path.exists(params_fname):
        raise Exception('Dataset parameter file does not exist: '+params_fname)
    with open(params_fname) as f:
        return json.load(f)
