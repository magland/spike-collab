import numpy as np

class OutputExtractor(object):
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

    def getNumUnits(self):
        '''This function returns the number of units detected in the recording

        Returns
        ----------
        num_units: int
            The number of units in the recording
        '''
        raise NotImplementedError("The getNumUnits function is not \
                                  implemented for this extractor")

    def getUnitSpikeTimes(self, unit_id):
        '''This function extracts all the spike times from the specified unit
        and returns it in the form of a numpy array of spike times.

        Parameters
        ----------
        unit_id: int
            The id that specifies a unit in the recording.
        Returns
        ----------
        spike_times: numpy.ndarray
            An 1D array containing all the spike times in the specified
            unit.
        '''
        raise NotImplementedError("The extractUnitSpikeTimes function is not \
                                  implemented for this extractor")
