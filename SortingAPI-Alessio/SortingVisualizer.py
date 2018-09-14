import numpy as np
import matplotlib.pyplot as plt

class SortingVisualizer(object):
    '''A class that takes in a Parser and Analyzer object and it is only devoted to plotting
    I would keep it separate from the analyzer

    The parser input could be useful for plotting original data, raster, etc.
    The analyzer for plotting of extracted info, such as waveforms, pc components, metrics, etc.

    '''
    def __init__(self, parser, analyzer):
        '''register parser and analyzer
        '''

        self.parser = parser
        self.analyzer = analyzer


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
        pass

    def plotRaster(self, unit_id):
        '''

        Parameters
        ----------
        unit_id

        Returns
        -------

        '''
        pass

    def plotPCAprojections(self, unit_id):
        '''

        Parameters
        ----------
        unit_id

        Returns
        -------

        '''
        pass