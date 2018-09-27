from mountainlab_pytools import mlproc as mlp
from mountainlab_pytools import mdaio
import spikeinterface as si
import os, sys
import numpy as np
import json


def gen_synth_datasets(datasets,*,tmpdir,outdir):
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for ds in datasets:
        ds_name=ds['name']
        print(ds_name)
        templates=ds['templates']
        spiketrains_fname=tmpdir+'/spiketrains_{}.npy'.format(ds_name)
        recording_fname=tmpdir+'/recording_{}.h5'.format(ds_name)
        gen_spiketrains(spiketrains_fname,dict(duration=ds['duration'],n_exc=ds['n_exc'],n_inh=ds['n_inh']))
        gen_recording(templates,spiketrains_fname,recording_fname,dict(noise_level=ds['noise_level'],min_dist=15))
        mlp.runPipeline()
        IX=si.MEArecInputExtractor(recording_file=recording_fname)
        OX=si.MEArecOutputExtractor(recording_file=recording_fname)
        IX2=si.SubInputExtractor(IX,channel_ids=ds['channel_ids'])
        print('Writing in mda format...')
        si.MdaInputExtractor.writeDataset(IX2,outdir+'/{}'.format(ds_name))
        si.MdaOutputExtractor.writeFirings(OX,outdir+'/{}/firings_true.mda'.format(ds_name))
    print('Done.')
        
# Wrappers to MEArec processors
def gen_spiketrains(spiketrains_out,params):
    mlp.addProcess(
        'mearec.gen_spiketrains',
        inputs=dict(
        ),
        outputs=dict(
            spiketrains_out=spiketrains_out
        ),
        parameters=params,
        opts={}
    )
    
def gen_recording(templates,spiketrains,recording_out,params):
    #ml_mearec.gen_recording()(templates=templates,spiketrains=spiketrains,recording_out=recording_out,**params)
    mlp.addProcess(
        'mearec.gen_recording',
        inputs=dict(
            templates=templates,
            spiketrains=spiketrains
        ),
        outputs=dict(
            recording_out=recording_out
        ),
        parameters=params,
        opts={}
    )