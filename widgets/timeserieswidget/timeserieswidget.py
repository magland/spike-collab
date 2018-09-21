from matplotlib import pyplot as plt
import numpy as np
import ipywidgets as widgets
from matplotlib.ticker import MaxNLocator

class TimeseriesWidget:
    def __init__(self,*,input_extractor,output_extractor=None,channels=None,trange=None):
        self._input_extractor=input_extractor
        self._output_extractor=output_extractor
        self._samplerate=input_extractor.getSamplingFrequency()
        if channels is not None:
            self._visible_channels=channels
        else:
            raise Exception('TODO: default channels')
            #self._visible_channels=range(1,reader.numChannels()+1)
        if trange is not None:
            self._visible_trange=trange
        else:
            raise Exception('TODO: default trange')
            #self._visible_trange=[0,np.minimum(reader.numTimepoints(),3500)]
        self._initialize_stats()
        self._vspacing=self._mean_channel_std*15
        self._widget=widgets.Output()
        self._control_panel=self._create_control_panel()
        display(widgets.VBox([self._control_panel,self._widget]))
        self._update_plot()
    def widget(self):
        return self._widget
    def figure(self):
        return self._figure
    def _update_plot(self):
        chunk0=self._input_extractor.extractRawSlices(
            electrode_ids=self._visible_channels,
            t_start=self._visible_trange[0],
            t_end=self._visible_trange[1]
        )[0]
        self._widget.clear_output(wait=True)
        with self._widget:
            plt.xlim(self._visible_trange[0]/self._samplerate,self._visible_trange[1]/self._samplerate)
            plt.ylim(-self._vspacing,self._vspacing*len(self._visible_channels))
            plt.gcf().set_size_inches(14,7)
            plt.gca().get_xaxis().set_major_locator(MaxNLocator(prune='both'))
            plt.gca().get_yaxis().set_ticks([])
            plt.xlabel('Time (sec)')
            
            self._plots={}
            self._plot_offsets={}
            offset0=self._vspacing*(len(self._visible_channels)-1)
            tt=np.arange(self._visible_trange[0],self._visible_trange[1])/self._samplerate
            for im,m in enumerate(self._visible_channels):
                self._plot_offsets[m]=offset0
                self._plots[m]=plt.plot(tt,self._plot_offsets[m]+chunk0[im,:])
                offset0=offset0-self._vspacing
            self._figure=plt.gcf()
            plt.show()
    def _pan_left(self):
        self._pan(-0.1)
    def _pan_right(self):
        self._pan(0.1)
    def _pan(self,factor):
        span=self._visible_trange[1]-self._visible_trange[0]
        delta=int(span*factor)
        new_trange=[self._visible_trange[0]+delta,self._visible_trange[1]+delta]
        if new_trange[0]<0:
            new_trange[1]+=-new_trange[0]
            new_trange[0]=0
        self._visible_trange=new_trange
        self._update_plot()
    def _scale_up(self):
        self._scale(1.2)
    def _scale_down(self):
        self._scale(1/1.2)
    def _scale(self,factor):
        self._vspacing/=factor
        self._update_plot()
    def _zoom_in(self):
        self._zoom(1.2)
    def _zoom_out(self):
        self._zoom(1/1.2)
    def _zoom(self,factor):
        span=self._visible_trange[1]-self._visible_trange[0]
        new_span=int(np.maximum(30,span/factor))
        tcenter=int((self._visible_trange[0]+self._visible_trange[1])/2)
        new_trange=[int(tcenter-new_span/2),int(tcenter-new_span/2+new_span-1)]
        if new_trange[0]<0:
            new_trange[1]+=-new_trange[0]
            new_trange[0]=0
        self._visible_trange=new_trange
        self._update_plot()
    def _initialize_stats(self):
        self._channel_stats={}
        #M=self._reader.numChannels()
        #N=self._reader.numTimepoints()
        chunk0=self._input_extractor.extractRawSlices(
            electrode_ids=self._visible_channels,
            t_start=self._visible_trange[0],
            t_end=self._visible_trange[1]
        )[0]
        #chunk0=self._reader.getChunk(channels=self._visible_channels,trange=self._visible_trange)
        M0=chunk0.shape[0]
        N0=chunk0.shape[1]
        for ii in range(M0):
            self._channel_stats[self._visible_channels[ii]]=self._compute_channel_stats_from_data(chunk0[ii,:])
        self._mean_channel_std=np.mean([self._channel_stats[m]['std'] for m in self._visible_channels])
    def _compute_channel_stats_from_data(self,X):
        return dict(
            mean=np.mean(X),
            std=np.std(X)
        )
    def _create_control_panel(self):
        def on_zoom_in(b):
            self._zoom_in()
        def on_zoom_out(b):
            self._zoom_out()
        def on_pan_left(b):
            self._pan_left()
        def on_pan_right(b):
            self._pan_right()
        def on_scale_up(b):
            self._scale_up()
        def on_scale_down(b):
            self._scale_down()
        zoom_in=widgets.Button(icon='plus-square',tooltip="Zoom In",layout=dict(width='40px'))
        zoom_in.on_click(on_zoom_in)
        zoom_out=widgets.Button(icon='minus-square',tooltip="Zoom Out",layout=dict(width='40px'))
        zoom_out.on_click(on_zoom_out)
        pan_left=widgets.Button(icon='arrow-left',tooltip="Pan left",layout=dict(width='40px'))
        pan_left.on_click(on_pan_left)
        pan_right=widgets.Button(icon='arrow-right',tooltip="Pan right",layout=dict(width='40px'))
        pan_right.on_click(on_pan_right)
        scale_up=widgets.Button(icon='arrow-up',tooltip="Scale up",layout=dict(width='40px'))
        scale_up.on_click(on_scale_up)
        scale_down=widgets.Button(icon='arrow-down',tooltip="Scale down",layout=dict(width='40px'))
        scale_down.on_click(on_scale_down)
        self._debug=widgets.Output()
        return widgets.HBox([zoom_in,zoom_out,pan_left,pan_right,scale_up,scale_down,self._debug])