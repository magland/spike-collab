import numpy as np

class InputExtractor(object):
    '''A class that contains functions for extracting important information
    from input data to spike sorting software.

    Attributes:
        We can include any agreed upon global attributes every extractor must
        have here. If we agree on nothing, then it needs no shared attributes!

    '''
    def __init__(self):
        '''No need to initalize the parent class with any parameters (unless we
        agree on a standard attribute every spike sorter needs)
        '''

        self.implemented_get_raw_traces = False
        self.implemented_get_probe_information = False

    def extractRawTraces(self, t_start=None, t_end=None, electrode_ids=None):
        '''This function extracts and returns a trace from the raw data from the
        given electrode ids.

        Parameters
        ----------
        t_start: int
            The starting frame of the trace to be returned
        t_end: int
            The ending frame of the trace to be returned
        electrode_ids: array_like
            A list of electrode ids (ints) from which each trace will be extracted.

        Returns
        ----------
        raw_traces: numpy.ndarray
            A 2D array that contains all of the raw slices from each electrode.
            Dimensions are: (num_electrodes x num_frames)
        timestamps: numpy.array
            A 1D array containing sliced timestamps with a Quantity per timestamp
        '''
        raise NotImplementedError("The extractRawTraces function is not \
                                  implemented for this extractor")

    def getSamplingFrequency(self):
        '''This function returns sampling frequency

        Returns
        -------
        fs: Quantity
            Sampling frequency of the recordings
        '''
        raise NotImplementedError("The getSamplingFrequency function is not \
                                          implemented for this extractor")

    def getProbeInformation(self):
        '''This function returns the name, sampling rate, and recording electrode
        ids and locations for the probe in this recording.

        Returns
        ----------
        name: string
            The name of the probe being used in the recording
        sampling_rate: float
            The sampling rate of the probe for this recording (in kilohertz)
        rec_electrode_id_pos: array_like (of tuples)
            A list of tuples of electrode ids (ints) and electrode locations (float, microns)
            which were used for the recording.
        '''
        raise NotImplementedError("The getProbeInformation function is not \
                                  implemented for this extractor")
