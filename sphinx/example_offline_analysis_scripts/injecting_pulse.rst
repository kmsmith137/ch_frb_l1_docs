Injecting a simulated pulse
===========================

This script generates a stream consisting of Gaussian noise plus a single dispersed pulse.
The stream is represented as an rf_pipelines object, which is serialized to a json file.
The json file can be used in ``rfp-run``, for example::

   rfp-run -w pulse \                            # run name for web viewer
     example_gaussian_stream_with_pulse.json \   # stream
     example_bonsai_transform.json               # see make-jsonized-bonsai-transform.py

to dedisperse the data and plot the result in the web viewer.

(Source: ``ch_frb_l1_docs/example_offline_analysis_scripts/make-gaussian-stream-with-pulse.py``.)

.. literalinclude:: ../example_offline_analysis_scripts/make-gaussian-stream-with-pulse.py
    :language: python
