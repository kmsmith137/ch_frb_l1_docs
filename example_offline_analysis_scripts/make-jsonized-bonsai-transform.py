#!/usr/bin/env python
#
# This script makes a bonsai transform, and serializes it to a json file
# for later use in 'rfp-run'.
#
# Note that there are already some json-serialized bonsai transforms in
# the 'ch_frb_rfi' repository (in json_files/bonsai_16k), so you may not
# need to make a new one.
#
# A possible reason to make a new one: maybe you want to write bonsai's
# output to an HDF5 file?


import rf_pipelines


# The bonsai transform has its own configuration file.  This can be in a few
# different file formats, but for "production-scale" instances I recommend using
# the HDF5 format, which contains precomputed transfer matrices.  (If an alternative
# file format is used, then bonsai will take a few minutes to start up!)
#
# On the CHIME nodes, there are some pregenerated bonsai config files in 
# /data/bonsai_configs.  In this example, we use the "pulsar" config, which
# searches to max DM 205.  (The "production" configs search to max DM 13000.)

config_filename = '/data/bonsai_configs/bonsai_pulsar_v2.hdf5'


t = rf_pipelines.bonsai_dedisperser(
    config_filename = config_filename,
    fill_rfi_mask = True,    # always necessary for real dae

    # Write the output of the dedispersion transform to an HDF5 file.
    # FIXME: this should get written to the web viewer directory (or pipeline rundir).
    # Currently it gets written to the current working directory when the pipeline is run.
    hdf5_output_filename = 'triggers.hdf5',
    
    # These settings control plots for the web viewer.
    # To disable the web viewer plots, set img_prefix=None.
    img_prefix = 'triggers',
    img_ndm = 512,
    img_nt = 256,
    downsample_nt = 16,
    n_zoom = 4,
    plot_threshold1 = 7,
    plot_threshold2 = 10,
    plot_all_trees = True)


rf_pipelines.utils.json_write('example_bonsai_transform.json', t, clobber=True)
