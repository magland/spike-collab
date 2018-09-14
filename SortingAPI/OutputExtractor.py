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
        self.implemented_extract_unit_spike_times = False
        self.implemented_extract_unit_spike_waveforms = False
        self.implemented_extract_events_waveforms = False

    def getNumUnits(self):
        '''This function returns the number of units detected in the recording

        Returns
        ----------
        num_units: int
            The number of units in the recording
        '''
        raise NotImplementedError("The getNumUnits function is not \
                                  implemented for this extractor")

    def extractUnitSpikeTimes(self, unit_id):
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

    def extractUnitSpikeWaveforms(self, unit_id, waveform_len):
        '''This function extracts all the spike waveforms from the specified
        unit and returns it in the form of a numpy array of spike waveforms.

        Parameters
        ----------
        unit_id: int
            The id that specifies a unit in the recording.
        waveform_len: int
            The number of frames of the waveform to be extracted
        Returns
        ----------
        spike_waveforms: numpy.ndarray
            An array containing all the spike waveforms in the specified
            unit.
        '''
        raise NotImplementedError("The extractUnitSpikeWaveforms function is \
                                  not implemented for this extractor"

    def extractEventsWaveforms(self, event_ids, num_waveforms, waveform_len):
        '''This function extracts all the spike waveforms for the specified
        events in the recording (in chronological event order) and returns
        the specified number of waveforms for each event in the form of a numpy
        array of dimension num_events x num_waveforms x waveform_len.

        Parameters
        ----------
        event_ids: array_list
            A list of event ids (ints) that specifies the events from which the
            waveforms will be extracted and returned.
        num_waveforms: int
            The number of waveforms to be extracted for each event. The first
            waveform will be from the largest amplitude channel, then the second
            largest amplitude channel, etc.
        waveform_len: int
            The number of frames of the waveform to be extracted
        Returns
        ----------
        event_waveforms: numpy.ndarray
            An array containing all the spike waveforms for each specified
            event. Dimensions are num_events x num_waveforms x waveform_len.
        '''
        raise NotImplementedError("The extractEventsWaveforms function is \
                                  not implemented for this extractor"

