from mountainlab_pytools import mlproc as mlp
from mountainlab_pytools import mdaio
from matplotlib import pyplot as plt
import numpy as np

class OutputVisualizer:
    '''A class that contains functions for visualizing the output of spike sorting.
    '''
    def __init__(self,output_analyzer):
        '''Pass in the output analyzer which will allow us to retrieve the data we need for visualization
        '''
        self._output_analyzer=output_analyzer

    def viewUnitWaveforms(self, units=None, channels=None):
        '''Plot average spike waveforms and representative spikes for a collection of units
        Parameters
        ----------
        units: list of ints
            A list of unit ids
        channels: list of ints
            A list of channel ids
        '''
        if units is None:
            units=range(1,self._output_analyzer.getUnitCount()+1)
        if not units:
            return
        channel_locations=self._output_analyzer.getElectrodeLocations()
        if channels is None:
            channels=range(1,self._output_analyzer.getChannelCount()+1)
        
        list=[]
        for unit in units:
            spikes=self._get_random_spike_waveforms(unit=unit,max_num=20,channels=channels)
            item=dict(
                representative_waveforms=spikes,
                title='Unit {}'.format(unit)
            )
            list.append(item)
        with plt.rc_context({'axes.edgecolor':'gray'}):
            self.plot_spike_shapes_multi(list,channel_locations=channel_locations[:,np.array(channels)-1])
    
    def _get_random_spike_waveforms(self,*,unit,max_num,channels):
        num_events=self._output_analyzer.getUnitEventCount(unit=unit)
        if num_events>max_num:
            event_indices=np.random.choice(range(num_events),size=max_num,replace=False)
        else:
            event_indices=range(num_events)
        spikes=self._output_analyzer.getUnitEventWaveforms(unit=unit,event_indices=event_indices,channels=channels)
        return spikes
    
    def plot_spike_shapes(self, *, representative_waveforms=None, average_waveform=None, channel_locations=None, ylim=None, max_representatives=None, color='blue',title=''):
        if average_waveform is None:
            if representative_waveforms is None:
                raise Exception('You must provide either average_waveform, representative waveforms, or both')
            average_waveform=np.mean(representative_waveforms,axis=2)
        M=average_waveform.shape[0] # number of channels
        T=average_waveform.shape[1] # number of timepoints
        if ylim is None:
            ylim=[average_waveform.min(),average_waveform.max()]
        yrange=ylim[1]-ylim[0]
        if channel_locations is None:
            channel_locations=np.zeros((2,M))
            for m in range(M):
                channel_locations[:,m]=[0,-m]

        spacing=1/0.8 # TODO: auto-determine this from the channel_locations

        xvals=np.linspace(-yrange/2,yrange/2,T)
        if representative_waveforms is not None:
            if max_representatives is not None:
                W0=representative_waveforms
                if W0.shape[2]>max_representatives:
                    indices=np.random.choice(range(W0.shape[2]),size=max_representatives,replace=False)
                    representative_waveforms=W0[:,:,indices]
            L=representative_waveforms.shape[2]
            XX=np.zeros((T,M,L))
            YY=np.zeros((T,M,L))
            for m in range(M):
                loc=channel_locations[:,m]*yrange*spacing
                for j in range(L):
                    XX[:,m,j]=loc[0]+xvals
                    YY[:,m,j]=loc[1]+representative_waveforms[m,:,j]-representative_waveforms[m,0,j]
            XX=XX.reshape(T,M*L)
            YY=YY.reshape(T,M*L)
            plt.plot(XX, YY, 'gray', alpha=0.2)

            XX=np.zeros((T,M))
            YY=np.zeros((T,M))
            for m in range(M):
                loc=channel_locations[:,m]*yrange*spacing
                XX[:,m]=loc[0]+xvals
                YY[:,m]=loc[1]+average_waveform[m,:]-average_waveform[m,0]
            plt.plot(XX, YY, color)

        plt.gca().get_xaxis().set_ticks([])
        plt.gca().get_yaxis().set_ticks([])
        if title:
            plt.title(title,color='gray')

    def _get_ylim_for_item(self,average_waveform=None,representative_waveforms=None):
        if average_waveform is None:
            if representative_waveforms is None:
                raise Exception('You must provide either average_waveform, representative waveforms, or both')
            average_waveform=np.mean(representative_waveforms,axis=2)
        return [average_waveform.min(),average_waveform.max()]

    def _determine_global_ylim(self,list):
        ret=[0,0]
        for item in list:
            ylim0 = self._get_ylim_for_item(
                average_waveform=item.get('average_waveform',None),
                representative_waveforms=item.get('representative_waveforms',None)
            )
            ret[0]=np.minimum(ylim0[0],ret[0])
            ret[1]=np.maximum(ylim0[1],ret[1])
        return ret

    def plot_spike_shapes_multi(self, list, *, ncols=5, **kwargs):
        if 'ylim' in kwargs:
            ylim=kwargs['ylim']
        else:
            ylim=self._determine_global_ylim(list)
        nrows = np.ceil(len(list) / ncols)
        plt.figure(figsize=(3 * ncols, 3 * nrows))
        for i, item in enumerate(list):
            plt.subplot(nrows, ncols, i + 1)
            self.plot_spike_shapes(**item, **kwargs, ylim=ylim)

class PlaceholderOutputAnalyzer:
    def __init__(self,*,timeseries,firings,geom=None):
        self._timeseries=timeseries
        self._firings=firings
        self._geom=geom
    def initialize(self):
        print('Downloading timeseries (if needed): {}'.format(self._timeseries))
        timeseries_path=mlp.realizeFile(self._timeseries)
        print('Downloading firings (if needed): {}'.format(self._firings))
        firings_path=mlp.realizeFile(self._firings)
        if self._geom is not None:
            print('Downloading geom (if needed): {}'.format(self._geom))
            geom_path=mlp.realizeFile(self._geom)
            self._G=np.genfromtxt(geom_path, delimiter=',').T
            self._G=np.flip(self._G,axis=0)
        else:
            self._G=None
        print('Reading arrays into memory...')
        self._X=mdaio.readmda(timeseries_path)
        self._F=mdaio.readmda(firings_path)
        self._times=self._F[1,:]
        self._labels=self._F[2,:]
        self._K=int(self._labels.max())
        
    def getUnitCount(self):
        return self._K
    def getChannelCount(self):
        return self._X.shape[0]
    def getUnitEventCount(self,*,unit):
        inds0=np.where(self._labels==unit)[0]
        return len(inds0)
    def getUnitEventWaveforms(self,*,unit,event_indices=None,channels=None,clip_size=50):
        inds0=np.where(self._labels==unit)[0]
        times0=self._times[inds0]
        if event_indices is not None:
            times0=times0[event_indices]
        spikes=self._extract_clips(self._X,times=times0,clip_size=clip_size)
        if channels is not None:
            spikes=spikes[np.array(channels)-1,:,:]
        return spikes
    def getElectrodeLocations(self):
        if self._G is not None:
            return self._G
        M=self.getChannelCount()
        channel_locations=np.zeros((2,M))
        for m in range(1,M+1):
            channel_locations[:,m-1]=[0,-m]
        return channel_locations
        
    def _extract_clips(self,timeseries,*,times,clip_size):
        M=timeseries.shape[0]
        T=clip_size
        L=len(times)
        Tmid = int(np.floor((T + 1) / 2) - 1);
        clips=np.zeros((M,T,L),dtype='float32')
        for j in range(L):
            t1=int(times[j]-Tmid)
            t2=int(t1+clip_size)
            clips[:,:,j]=timeseries[:,t1:t2]
        return clips

    #def _sample_spikes(timeseries,firings,max_spikes_per_unit=20,clip_size=100):
    #    M=timeseries.shape[0]
    #    times=firings[1,:]
    #    labels=firings[2,:]
    #    K=int(labels.max())
    #    units=[]
    #    for k in range(1,K+1):
    #        unit={}
    #        inds_k=np.where(labels==k)[0]
    #        if len(inds_k>max_spikes_per_unit):
    #            inds_k=np.random.choice(inds_k,max_spikes_per_unit,replace=False)
    #        unit['spikes']=extract_clips(timeseries,times=times[inds_k],clip_size=clip_size)    
    #        units.append(unit)
    #    return dict(
    #        units=units
    #    )
    

    