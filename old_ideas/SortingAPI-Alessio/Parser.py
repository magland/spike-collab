import numpy as np

class Parser(object):
    '''I like the idea of having an extractor, but I think its scope should be different:
    Parser: user-defined parser for input (ephys) and output (sorting) data. This is a parent class

    To be parsed from input:
    self.recordings - N x T np.array
    self.timestamps - pq.Quantity np.array (or alternatively frequency)
    self.positions - (optional) electrode positions
    self.channel_groups - chhannel for the electrode (e.g. 2 tetrodes are [0,0,0,0,1,1,1,1])

    To be parsed from output:
    self.spiketimes
    self.cluster_nums

    I think that from these sets of data we should be able to extract all the other info: waveforme, pca, anything else.
    Do we need other things?

    We could follow NWB definitions here too.

    '''
    def __init__(self):
        '''No need to initalize the parent class with any parameters (unless we
        agree on a standard attribute every spike sorter needs)
        '''

        # Input
        self.recordings = None
        self.timestamps = None
        self.positions = None
        self.channel_groups = None

        # Output
        self.spiketimes = None
        self.cluster_nums = None

    def parseInput(self, input_folder):
        '''
        Parses the input into our file format and populates input data
        :param input_folder:
        :return:
        '''
        raise NotImplementedError('subclasses must override parseInput()!')

    def parseOutput(self, ouput_folder):
        '''
        Parses the input into our file format and populates input data
        :param input_folder:
        :return:
        '''
        raise NotImplementedError('subclasses must override parseOutput()!')

################################################################################

class AlessioParser(Parser):
    '''This child class inherits all the functions of the parent class and only overrides the parseInput and
    parseOutput for specific formats

    '''
    def __init__(self, input, output):
        Parser.__init__(self)

        self.parseInput(input)
        self.parseOutput(output)

    def parseInput(self, input_folder):
        '''
        Parses the input into our file format and populates input data
        :param input_folder:
        :return:
        '''
        pass

    def parseOutput(self, ouput_folder):
        '''
        Parses the output into our file format and populates output data
        :param input_folder:
        :return:
        '''
        pass