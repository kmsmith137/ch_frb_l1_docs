#!/usr/bin/env python
#
# This script creates a stream consisting of Gaussian noise plus a single pulse,
# and serializes the stream to a json file.
#
# The json file can be used in 'rfp-run'.  For example, to dedisperse the data and
# plot the result in the web viewer, do:
#
#   rfp-run -w pulse \                            # run name for web viewer
#     example_gaussian_stream_with_pulse.json \   # stream
#     example_bonsai_transform.json               # see make-jsonized-bonsai-transform.py

import rf_pipelines

s = rf_pipelines.gaussian_noise_stream(
    nfreq = 16384,
    nt_tot = 512*1024,
    freq_lo_MHz = 400.0,
    freq_hi_MHz = 800.0,
    dt_sample = 0.984e-3,
    sample_rms = 1.0,
    nt_chunk = 1024
)

t = rf_pipelines.frb_injector_transform(
    snr = 100.0,
    undispersed_arrival_time = 200.0,
    dm = 30.0,
    variance = 1.0**2,   # should be square of 'sample_rms' above
    intrinsic_width = 0.005,
)

# The output of this script is logically a "stream" consisting of Gaussian noise plus a
# single pulse, but is implemented as a two-stage mini-pipeline: a stream object which
# produces the Gaussian noise, plus a transform to add the pulse.

p = rf_pipelines.pipeline([s,t])

rf_pipelines.utils.json_write('example_gaussian_stream_with_pulse.json', p, clobber=True)
