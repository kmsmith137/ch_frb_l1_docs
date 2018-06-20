#!/usr/bin/env python
#
# This script can be run on a DRAO node (suggestion: ``cfdn7``, which is dedicated to 
# offline analysis), to create an rf_pipelines stream object from previously captured data.
#
# In this example, we use 10 seconds of data in beam 111 from a run in April 2018 
# (arbitrarily chosen).


import os
import rf_pipelines


# Top-level acquisition directory (on central CHIME FRB file server)
dirname = '/frb-archiver-1/acq_data'

# Subdirectory corresponding to a run from April 2018
dirname = os.path.join(dirname, 'frb_run_11_20180407_beams_111to118_130to137_146to150')

# Sub-subdirectory corresponding to beam 111
dirname = os.path.join(dirname, 'beam_0111')

dirname = '/Users/kmsmith/chime_data'


############################################################################################
#
# Now we choose 10 files arbitrarily, and construct an rf_pipelines stream object.
#
# Currently we can't do this by calling rf_pipelines.streams.chime_stream_from_times().
# This is because chime_stream_from_times() assumes the old HDF5 file format, whereas we've
# now switched to a msgpack-based file format.
#
# TODO: write a version of rf_pipelines.streams.chime_stream_from_times() which uses
# the new msgpack format.  One nontrivial difference: the HDF5 format contained timestamps,
# whereas the new format doesn't!  (More accurately, the new format uses "fpga counts" as
# its timestamps, which can't yet be converted to an externally meaningful time, although
# this may be possible in the future.)  For now, the best we can do is to use the creation
# time of the msgpack file (os.stat().st_ctime) as an approximate timestamp.
#
# Note that there are currently two different low-level stream classes for CHIME
# HDF5 and msgpack files (the naming convention could be improved here!!)
#
#    chime_stream_from_filename_list() - old HDF5 format
#    chime_frb_stream_from_filename_list() - new msgpack format


# Arbitrarily chosen range of file indices.
index_list = range(308990, 309000)

filename_list = [ os.path.join(dirname, ('chunk_%08d.msg' % i)) for i in index_list ]

# Sanity check
assert all(os.path.exists(f) for f in filename_list)  

# See chime_frb_stream_from_filename_list() docstring for info on these arguments
stream = rf_pipelines.chime_frb_stream_from_filename_list(
    filename_list, 
    nt_chunk = 0, 
    noise_source_align = 0
)

print 'Stream object created successfully!'


############################################################################################
#
# Serialize the stream object to a json object, and save to an external .json file.
#
# This is a useful way to save the stream object, for later use in rf_pipelines command-line
# utilities (e.g. rfp-run).
#
# Note: rf_pipelines.utils.json_write() is roughly equivalent to
#    json.dump(stream.jsonize(), file, indent=4)


rf_pipelines.utils.json_write('example_acq.json', stream, clobber=True)


############################################################################################
#
# As an ultra-low-budget way to see the data, if you uncomment the following, a few
# waterfall plots will be generated in the current directory.  This may be useful
# as a quick sanity check!  A better way to browse the data is to use the rf_pipelines
# web viewer, which will be documented soon in its own example script!


# t = rf_pipelines.plotter_transform(
#     img_prefix = 'chime_acq', 
#     img_nfreq = 256, 
#     img_nt = 256, 
#     downsample_nt = 16, 
#     n_zoom = 1
# )
#
# p = rf_pipelines.pipeline([stream, t])
# p.run(outdir='.')
