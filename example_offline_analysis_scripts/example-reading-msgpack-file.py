#!/usr/bin/env python
#
# This example script shows how to read CHIME data files (in msgpack format)
# directly, without going through the pipeline.
#
# Note: rpc_client.py is part of the ch_frb_l1 repository, but it is not currently
# installed anywhere, when 'make install' is done in the ch_frb_l1 repo.  In the
# meantime, you can use ch_frb_l1/rpc_client.py by copying or symlinking it to the
# directory containing this script.

import rpc_client

# Arbitrarily selected file, visible from DRAO node such as cfdn0 or cfdn9.
filename = ('/frb-archiver-1/acq_data/frb_run_11_20180407_beams_111to118_130to137_146to150'
            + '/beam_0111/chunk_00308000.msg')

# Object of type rpc_client.AssembledChunk.
ac = rpc_client.read_msgpack_file(filename)

# The decode() method returns a pair of 2-d float32 arrays (data, mask).
(data, mask) = ac.decode()

# Each array is indexed by (frequency, time), where the frequency index is an "upsampled"
# frequency.  The number of upsampled frequencies is equal to (1024 * ac.nupfreq), where
# 1024 is the hardcoded number of "coarse" (i.e. non-upsampled) frequencies, and ac.nupfreq
# is an upsampling factor (currently always 16).

assert data.shape == mask.shape == (1024 * ac.nupfreq, ac.nt)

# The 'scales' and 'offsets' arrays are used to encode/decode the data as 8-bit integers.
# Usually these arrays are not needed, since they are transparently applied by decode(),
# but they are needed for studying quantization noise.  The encoding is:
#
#   data = scale * (8-bit value) + offset

(scales, offsets) = (ac.scales, ac.offsets)

# The scales and offsets arrays are indexed by (freqency, time) but the resolution
# is lower than the (data, weights) arrays.  The number of frequencies is always 1024
# (the hardcoded number of "coarse" frequencies), and the number of time samples
# is (ac.nt / ac.nt_per_packet), where ac.nt_per_packet is a time downsampling factor.

assert scales.shape == offsets.shape == (1024, ac.nt // ac.nt_per_packet)

print '%s: looks good!' % filename
