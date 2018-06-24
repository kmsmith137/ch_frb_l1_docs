Offline Analysis TODO
=====================

 - Inventory captured data, make pulsar acquisitions.

     - :ref:`Making an acquisition` example script, showing how to construct an rf_pipelines stream object from a set of data files,
       and serialize the stream to a json file for later use in ``rfp-run``.

   We will need to convert FPGA timestamps to real timestamps.
     
     - There is a json file which contains all the necessary information, automatically committed to git whenever the FPGA counts are reset
       (https://github.com/CHIMEFRB/frb-configs/tree/master/RunParameters).  Unfortunately it overwrites the previous file, so we need to
       write a little code to loop over the git history and retrieve them all!

     - Example code: https://github.com/CHIMEFRB/Intensity-Analysis-Utils/blob/master/iautils/scripts/msgpack2fil.py
       (search for fpga_time)

 - Understand Miles' framework for forecasting SNR.

     - Miles framework: https://github.com/CHIMEFRB/Sensitivity
     - ATNF catalog: http://www.atnf.csiro.au/people/pulsar/psrcat
     - ATNF parameter list: http://www.atnf.csiro.au/research/pulsar/psrcat/psrcat_help.html#par_list

 - Set up offline scripting framework for reproducing SNR values in database, comparing with forecasts.

   Roughly, the chain of steps might look like this:

     - Make an rf_pipelines stream object and serialize it to a json file (see "Inventory captured data" bullet point above).

     - Choose a RFI transform chain.  There are some json-serialized RFI chains in the mrafieir/ch_frb_l1_ repo.
       In this example, I'll use ``ch_frb_rfi/json_files/rfi_16k/17-12-02-two-pass-v3.json``, which also contains
       some plotter transforms for the web viewer.

     - Make a bonsai transform and serialize it to json.  There are some json-serialized bonsai transforms in mrafieir/ch_frb_l1_,
       but let's make a new transform, so that we can write the output of the dedispersion transform to an hdf5 file for later
       processing.  

     - Run it::

          # Type 'rfp-run' with no arguments for a list of all its command-line options.

         rfp-run -w example \    # name of run for web viewer
	 example_acq.json \      # first in pipeline: stream
	 ch_frb_rfi/json_files/rfi_16k/17-12-02-two-pass-v3.json   # second: RFI chain
	 example_bonsai_transform.json     # last in pipeline: dedisperser

     - FIXME: triggers.hdf5 goes to the wrong place!!!

 - Incorporate detrending correction.  Can we use less detrending?  (in real-time pipeline?  in offline analysis of bright pulsars?)

 - Overclipping studies.  What happens in simulation?  If we dedisperse the mask, do we see peaks?

 - Simulating a pulsar.  Are bonsai's SNR estimates still unbiased if pulses are repeating (rather than isolated)?

 - Variance estimation.  How should we be weighting the channels?  Is the radiometer equation satisfied?

     - TODO

 - Related: estimating the spectrum of the pulsar.

 - Pulsar masker/unmasking transform.

 - Determining arrival times of pulses (either through external ephemeris or internal analysis).

.. _mrafieir/ch_frb_rfi: https://github.com/mrafieir/ch_frb_rfi