import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import neo

# use InputExtractor and OutputExtractor
from InputExtractor import InputExtractor
from OutputExtractor import OutputExtractor

class Analyzer(object):
    '''A class that handles InputExtractor and OutputExtractor objects and performs
    standardized analysis and evaluation on spike sorting output.

    Attributes:
        input_extractor (InputExtractor)
        output_extractor (InputExtractor)
    '''
    def __init__(self, input_extractor, output_extractor):
        '''No need to initalize the parent class with any parameters (unless we
        agree on a standard attribute every spike sorter needs)
        '''
        # to perform comparisons between spike sorters
        if isinstance(input_extractor, InputExtractor):
            self.input_extractor = input_extractor
        else:
            raise AttributeError('Input extractor argument should be an InputExtractor object')
        if isinstance(output_extractor, OutputExtractor):
            self.output_extractor = output_extractor
        else:
            raise AttributeError('Output extractor argument should be an OutputExtractor object')

    def inputExtractor(self):
        '''This function returns the input extractor and allows tu call its methods

        Returns
        ----------
        input_extractor (InputExctractor)
        '''
        return self.input_extractor

    def outputExtractor(self):
        '''This function returns the output extractor and allows tu call its methods

        Returns
        ----------
        output_extractor (OutputExctractor)
        '''
        return self.output_extractor

    def getUnitSpikeWaveforms(self, unit_id, t_start=None, t_stop=None, cutout=[3., 3.]):
        '''This function returns the spike waveforms from the specified unit_id from t_start and t_stop
        in the form of a numpy array of spike waveforms.

        Parameters
        ----------
        unit_id: (int)
            The unit to extract waveforms from
        t_start: (int) or (Quantity)
            Starting time to extract waveforms (default=None, if int it is assumed in seconds)
        t_stop: (int) or (Quantity)
            Stop time to extract waveforms (default=None, if int it is assumed in seconds)
        cutout: list of 2 float or 2 Quantities
            Time to cut out waveform before (cutout[0]) and after (cutout[1]) the peak. If float it is assumed ms

        Returns
        -------

        '''
        recordings, times = self.input_extractor.extractRawSlices(t_start, t_stop)
        fs = self.input_extractor.getSamplingFrequency()
        spike_times = self.output_extractor.getUnitSpikeTimes(unit_id, t_start, t_stop)

        if type(cutout[0]) == float:
            n_pad = [int(cutout[0] * pq.ms * fs.rescale('kHz')), int(cutout[1] * pq.ms * fs.rescale('kHz'))]
        elif type(cutout[0]) == pq.Quantity:
            n_pad = [int(cutout[0].rescale('ms') * fs.rescale('kHz')), int(cutout[1].rescale('ms') * fs.rescale('kHz'))]
        nchs, npts = recordings.shape
        nsamples = np.sum(n_pad)

        waveforms = np.zeros((len(spike_times), nchs, nsamples))

        print('Number of waveforms: ', len(spike_times))

        for t_i, t in enumerate(spike_times):
            idx = np.where(times > t)[0]
            if len(idx) != 0:
                idx = idx[0]
                # find single waveforms crossing thresholds
                if idx - n_pad[0] > 0 and idx + n_pad[1] < npts:
                    t_spike = times[idx - n_pad[0]:idx + n_pad[1]]
                    wf = recordings[:, idx - n_pad[0]:idx + n_pad[1]]
                elif idx - n_pad[0] < 0:
                    t_spike = times[:idx + n_pad[1]]
                    t_spike = np.pad(t_spike, (np.abs(idx - n_pad[0]), 0), 'constant') * unit
                    wf = recordings[:, :idx + n_pad[1]]
                    wf = np.pad(spike_rec, ((0, 0), (np.abs(idx - n_pad[0]), 0)), 'constant')
                elif idx + n_pad[1] > npts:
                    t_spike = times[idx - n_pad[0]:]
                    t_spike = np.pad(t_spike, (0, idx + n_pad[1] - npts), 'constant') * unit
                    wf = recordings[:, idx - n_pad[0]:]
                    wf = np.pad(spike_rec, ((0, 0), (0, idx + n_pad[1] - npts)), 'constant')
                waveforms[t_i] = wf

        return waveforms


    def getSpikeTrain(self, unit_id=None, t_start=None, t_stop=None):
        '''This function returns a NEO spike train for the given unit.
        It will throw an error if the ExtracellularExtractor did not implement
        the needed functions.

        Parameters
        ----------
        unit_id: int or list
            The id that specifies a unit or a list of units in the recording. If None all units are returned.
        t_start: (int) or (Quantity)
            Starting time to clip spike trains (default=None, if int it is assumed in seconds)
        t_stop: (int) or (Quantity)
            Stop time to clip spike trains (default=None, if int it is assumed in seconds)
        Returns
        ----------
        spike_train: list of Neo.Spiketrain
            A list of neo.Spiketrain for the specified units spike times
        '''
        if unit_id is None:
            # extract all spiketrains
            spike_trains = []
            for i in range(self.output_extractor.getNumUnits()):
                spike_times = self.output_extractor.getUnitSpikeTimes(i, t_start, t_stop)
                st = neo.SpikeTrain(spike_times, t_start=t_start, t_stop=t_stop)
                spike_trains.append(st)
        elif isinstance(unit_id, int):
            spike_times = self.output_extractor.getUnitSpikeTimes(unit_id, t_start, t_stop)
            st = neo.SpikeTrain(spike_times, t_start=t_start, t_stop=t_stop)
            spike_trains = [st]
        elif isinstance(unit_id, list):
            spike_trains = []
            for i in unit_id:
                spike_times = self.output_extractor.getUnitSpikeTimes(i, t_start, t_stop)
                st = neo.SpikeTrain(spike_times, t_start=t_start, t_stop=t_stop)
                spike_trains.append(st)
        else:
            raise AttributeError('unit_id should be either None, int, or list')

        return spike_trains

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
