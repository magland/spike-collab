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

################################################################################

class ColesExampleExtractor(ExtracellularExtractor):
    '''This child class inherits all the functions of the parent class. Now I
    just need to override all of the parent class functions such that it works
    for my specific file format and spike sorting implementation.

    In my extractor example, the user had no way of getting waveforms. Whoops!
    I guess they will have to leave that unimplemented then.

    '''
    def __init__(self, spike_unit_ids, spike_times_file):
        ExtracellularExtractor.__init__(self)

        '''
        All passed in arguments and saved attributes are specific for my
        situation. When a user makers a subclass they can put whatever they want
        here.
        '''
        self.spike_times_file = spike_times_file
        self.spike_unit_ids = spike_unit_ids

        '''
        Any other initialization code can go here. Here is an example of a
        private function call that only my child extractor has.
        '''
        self.something_useful = self.__Foo(parameter1, parameter2)

    def getNumUnits(self):
        '''Now I can override the parent class function, getNumUnits, with my
        own code to match my specific file types and formats!

        Still must keep the same input and return the same output as is
        specified by the parent

        Returns
        ----------
        num_units: int
            The number of units in the recording
        '''

        num_units = do_some_code
        self.implemented_get_num_units = True
        return num_units



    def extractUnitSpikeTimes(self, unit_id):
        '''Now I can override the parent class function, extractUnitSpikeTimes,
        with my own code to match my specific file types and formats!

        Still must keep the same input and return the same output as is
        specified by the parent

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

        spike_times = do_some_code
        self.implemented_extract_unit_spike_times = True
        return spike_times


    def __Foo(parameter1, parameter2):
         '''Private functions allow for the user to easily make helper functions
         inside their extractor subclass to make their life simpler. :)

         Parameters
         ----------
         parameter1: type
             The first parameter of my method
         parameter2: type
             The second parameter of my method

         Returns
         ----------
         something_useful: unit
             Returns something I will find useful!
         '''

         #Code goes here for my private function
