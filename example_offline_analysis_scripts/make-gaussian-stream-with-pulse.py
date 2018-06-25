#!/usr/bin/env python

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

p = rf_pipelines.pipeline([s,t])

rf_pipelines.utils.json_write('example_gaussian_stream_with_pulse.json', p, clobber=True)
