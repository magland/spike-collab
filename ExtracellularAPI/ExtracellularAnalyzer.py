import numpy as np
import matplotlib.pyplot as plt

class ExtracellularAnalyzer(object):
    '''A class that takes in an ExtracellularExtractor and implements
    standardized evaluation and visualization using the functions from the
    ExtracellularExtractor and built in code.

    Attributes:
        num_units (int)                       Number of units detected in the recording
        spike_times (numpy.ndarray (2D))      Contains all spike times for each unit
        spike_waveforms (numpy.ndarray (2D))  Contains all spike waveforms for each unit

    '''
    def __init__(self, extracellular_extractor, waveform_len=30):
        '''No need to initalize the parent class with any parameters (unless we
        agree on a standard attribute every spike sorter needs)
        '''

        #Make sure the most basic function is implemented or this will break!
        if(extracellular_extractor.implemented_get_num_units):
            self.num_units = extracellular_extractor.getNumUnits()
        else:
            raise NotImplementedError("You have to implement getNumUnits!")

        self.waveform_len = waveform_len

        #More code below depending on what functions we want

    '''
    This implementation allows for the analyzer to return important information
    using the passed in ExtracellularExtractor if the ExtracellularExtractor
    implemented the corresponding functions. Otherwise it will throw an error.
    '''
    def getNumUnits(self):
        '''This function returns the number of units detected in the recording

        Returns
        ----------
        num_units: int
            The number of units in the recording
        '''
        return self.num_units

    def getUnitSpikeTimes(self, unit_id):
        '''This function returns the spike times from the specified unit
        in the form of a numpy array of spike times.

        Returns
        ----------
        spike_times: numpy.ndarray
            An 1D array containing all the spike times in the specified
            unit.
        '''
        if(extracellular_extractor.implemented_extract_unit_spike_times):
            unit_spike_times = extracellular_extractor.extractUnitSpikeTimes(unit_id)
            return unit_spike_times
        else:
            raise NotImplementedError("The extractor did not implement extractUnitSpikeTimes")

    def getUnitSpikeWaveforms(self, unit_id):
        '''This function returns the spike waveforms from the specified unit
        in the form of a numpy array of spike waveforms.

        Returns
        ----------
        spike_times: numpy.ndarray
            An 2D array containing all the spike waveforms in the specified
            unit.
        '''
        if(extracellular_extractor.implemented_extract_unit_spike_waveforms):
            unit_spike_waveforms = extracellular_extractor.extractUnitSpikeWaveforms(unit_id, self.waveform_len)
            return unit_spike_waveforms
        else:
            raise NotImplementedError("The extractor did not implement extractUnitSpikeWaveforms")


    '''
    This implementation also allows for the analyzer to use the Extracellular
    Extractor to do more exciting universal functions such as plotting waveforms,
    returning NEO spike trains, or running unsupervised metrics for getting
    spike sorting results.
    '''

    def plotUnitWaveforms(self, unit_id, num_waveforms):
        '''This function plots all the waveforms in the specified unit in a
        clean and appropriate manner. It will throw an error if the ExtracellularExtractor
        did not implement the needed functions.

        Parameters
        ----------
        unit_id: int
            The id that specifies a unit in the recording.
        num_waveforms: int
            The number of waveforms to be plotted.
        '''
        unit_waveforms = self.getUnitSpikeWaveforms(unit_id)
        do some plotting of unit_waveforms

    def getSpikeTrain(self, unit_id):
        '''This function returns a NEO spike train for the given unit.
        It will throw an error if the ExtracellularExtractor did not implement
        the needed functions.

        Parameters
        ----------
        unit_id: int
            The id that specifies a unit in the recording.
        Returns
        ----------
        spike_train: NEOSPIKETRAIN.type
            A neospike train for the specified unit spike times
        '''
        unit_times = self.getUnitSpikeTimes(unit_id)
        return NEOSPIKETRAINWRAPPER(unit_times)

    def getClusterStability(self, unit_id):
        '''This function returns the cluster stability of a given unit.
        It will throw an error if the ExtracellularExtractor did not implement
        the needed functions.

        Parameters
        ----------
        unit_id: int
            The id that specifies a unit in the recording.
        Returns
        ----------
        cluster_stability: float
            The cluster stability of the specified unit
        '''
        unit_waveforms = self.getUnitSpikeWaveforms(unit_id)
        cluster_stability = do some code
        return cluster_stability
