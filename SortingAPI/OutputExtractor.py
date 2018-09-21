import numpy as np
from abc import ABC, abstractmethod

class OutputExtractor(ABC):
    '''A class that contains functions for extracting important information
    from the output data of spike sorting software.

    Attributes:
        We can include any agreed upon global attributes every extractor must
        have here. If we agree on nothing, then it needs no shared attributes!

    '''
    def __init__(self):
        '''No need to initalize the parent class with any parameters (unless we
        agree on a standard attribute every spike sorter needs)
        '''

        self.implemented_get_num_units = False
        self.implemented_get_unit_spike_times = False

    @abstractmethod
    def getNumUnits(self):
        '''This function returns the number of units detected in the recording

        Returns
        ----------
        num_units: int
            The number of units in the recording
        '''
        pass

    @abstractmethod
    def getUnitSpikeTimes(self, unit_id, t_start=None, t_end=None):
        '''This function extracts spike times from the specified unit.
        The inputs t_start and t_end give the range from which the extracted
        spike times can occur. If t_start and t_end are given then the spike
        times are returned which fall in the range:
                    [t_start, t_start+1, ..., t_end-1]
        Spike times are returned in the form of a numpy array of spike times.

        Parameters
        ----------
        unit_id: int
            The id that specifies a unit in the recording.
        t_start: int
            The frame above which a spike time is returned.
        t_end: int
            The frame below which a spike time is returned.
        Returns
        ----------
        spike_times: numpy.ndarray
            An 1D array containing all the spike times in the specified
            unit.
        '''
        pass
