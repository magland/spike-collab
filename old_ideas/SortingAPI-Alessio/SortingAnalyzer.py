import numpy as np

class SortingAnalyzer(object):
    '''A class that takes in a Parser and implements
    standardized evaluation functions knowing the input and output format

    At this point, given the standard and unprocessed format of the parser we can decide, e.g., to use neo as a
    spiketrain object (pro: waveforms stored alongside with spiketimes and annotations can be used,
    e.g. 'pc1'=[0.2,...], 'pc2'=[0.001, ...], 'clusterMetric'=0.9, and so on)

    '''
    def __init__(self, parser):
        '''Just register the ocrresponding parser object
        '''
        self.parser = parser
        # if neo is decided parse parses.spiketimes and parser.cluster_nums in neo.Spiketrain objects

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
        pass

    def getUnitSpikeTimes(self, unit_id):
        '''This function returns the spike times from the specified unit
        in the form of a numpy array of spike times.

        Returns
        ----------
        spike_times: numpy.ndarray
            An 1D array containing all the spike times in the specified
            unit.
        '''
        pass

    def getUnitSpikeWaveforms(self, unit_id):
        '''This function returns the spike waveforms from the specified unit
        in the form of a numpy array of spike waveforms.

        Returns
        ----------
        spike_times: numpy.ndarray
            An 2D array containing all the spike waveforms in the specified
            unit.
        '''
        pass

    def computePCAwaveforms(self, unit_id):
        '''

        Parameters
        ----------
        unit_id

        Returns
        -------

        '''
        pass

    def getNeoSpikeTrain(self, unit_id):
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
        pass

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
        pass