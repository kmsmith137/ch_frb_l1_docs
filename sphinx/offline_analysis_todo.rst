Offline Analysis TODO
=====================

Items marked ``KMS`` are things Kendrick is actively working on!

 - Inventory captured data, make pulsar acquisitions.

     - :ref:`Making an acquisition` example script, showing how to construct an rf_pipelines stream object from a set of data files,
       and serialize the stream to a json file for later use in ``rfp-run``.

   To determine whether there is a bright pulsar in a run, we will want to convert FPGA timestamps to real timestamps.
     
     - There is a json file which contains all the necessary information, automatically committed to git whenever the FPGA counts are reset
       (https://github.com/CHIMEFRB/frb-configs/tree/master/RunParameters).  Unfortunately it overwrites the previous file, so we need to
       write a little code to loop over the git history and retrieve them all!

     - Example code: https://github.com/CHIMEFRB/Intensity-Analysis-Utils/blob/master/iautils/scripts/msgpack2fil.py
       (search for fpga_time)

 - Understand Miles' framework for forecasting SNR.

     - Miles framework: https://github.com/CHIMEFRB/Sensitivity
     - ATNF catalog: http://www.atnf.csiro.au/people/pulsar/psrcat
     - ATNF parameter list: http://www.atnf.csiro.au/research/pulsar/psrcat/psrcat_help.html#par_list

 - Set up offline scripting framework for reproducing SNR values, comparing with forecasts.

   Roughly, the chain of steps might look like this:

     - Make an rf_pipelines stream object and serialize it to a json file.
       See the :ref:`Making an acquisition` example script, although you'll want to use more data!  (The example
       script only uses 10 data files, i.e. 10 seconds of data.)

     - Choose a RFI transform chain.  There are some json-serialized RFI chains in the `mrafieir/ch_frb_rfi`_ repo.
       In this example, I'll use ``ch_frb_rfi/json_files/rfi_16k/17-12-02-two-pass-v3.json``, which also contains
       some plotter transforms for the web viewer.

     - Make a bonsai transform and serialize it to json.  There are some json-serialized bonsai transforms in `mrafieir/ch_frb_rfi`_,
       but let's make a new transform, so that we can write the output of the dedispersion transform to an hdf5 file for later
       processing.  See the :ref:`Making a bonsai transform` example script.

     - Run the stream-rfi-bonsai transform chain with the ``rfp-run`` utility (which is part of rf_pipelines)::

          # Type 'rfp-run' with no arguments for a list of all its command-line options.

         rfp-run -w example \    # name of run for web viewer
	   example_acq.json \      # first in pipeline: stream
	   ch_frb_rfi/json_files/rfi_16k/17-12-02-two-pass-v3.json   # second: RFI chain
	   example_bonsai_transform.json     # last in pipeline: dedisperser

       Depending on how long your stream is, this may take a while to run.  You may want to use ``screen`` or ``tmux`` to run the command above.

       After the pipeline run ends, there should be an entry in the web viewer, containing waterfall and trigger plots.
       (For information on the web viewer, see :ref:`Web Services`.)
       
       There should also be a large HDF5 file containing bonsai's output arrays during the run.  We can postprocess
       this file to determine the SNR of each pulse.

     - Another option for determining the pulsar SNR would be to figure out how to use Alex Josephy's "L1B" code,
       a real-time tool which runs in the pipeline, postprocesses the bonsai output arrays, and generates an event list.

     - At some point we should figure out how to query the SQL database to figure out what SNR values
       were reported by the real-time pipeline.

     - ``KMS``: the bonsai HDF5 file format currently isn't documented anywhere!  I'll do this soon.

     - ``KMS``: the bonsai HDF5 file should get written to the web viewer directory (or pipeline rundir).
       Currently it gets written to the current working directory when the pipeline is run.
       This is a recipe for different runs overwriting each other and creating confusion!

     - ``KMS``: it would be convenient for pulsars to have a bonsai configuration file which doesn't search to such high DM.

 - More work on detrending.  Here is one possible reason why our reported SNR for pulsars might be low.
   Our RFI removal chain includes a "detrender" (i.e. fitting and subtracting a slowly varying baseline) along the 
   frequency axis of the (frequency, time) array.  This removes a fraction of the SNR, which will depend on the parameters
   of the pulse.

   In the memo :download:`18-03-19-pulsar-snr.pdf <../memos/18-03-19-pulsar-snr.pdf>`, we made an initial study of this
   effect and found that the fractional SNR loss was a simple function of (pulse DM) / (pulse width).  For typical FRB
   parameters, the SNR loss is small, but for pulsars it can be very significant.

   Does this effect completely or partially explain our low reported SNR's?

   This effect can be reduced substantially by changing a parameter in the RFI removal pipeline (the degree of the polynomial 
   fit that we use in the detrender).  We should definitely be doing this for pulsars, and maybe for the real-time FRB search.
   What is the lowest polynomial degree we can "get away with" without getting a lot of false positives from RFI?

 - Overclipping studies.  Here is another possible reason our reported SNR for pulsars might be low.
   We usually study bright pulsars, where the pulses may be mistaken for RFI and masked by the "clipper" transforms
   in our RFI removal chain.

   Is this happening?  If so, how should we modify our RFI transform chain so that we avoid overclipping bright pulsars,
   while still removing most of the RFI?  (Reminder: we don't need to use the same RFI transform chain for postprocessing
   pulsars as we do in the real-time search.)

 - I like the following idea for a quick hack to test whether we're overclipping bright pulsars.

   We write a new transform which *overwrites* the data array with 0 or 1, depending on whether the data element
   is unmasked or masked (i.e. the complement of the mask array), and sets the mask array to all ones.  We put this 
   transform after RFI removal and before dedispersion.
   Then if we see the pulsar in the output of the dedispersion transform, we'll know that we're overclipping.

   ``KMS``: will add an example script showing how to write a new rf_pipelines transform in python.

 - Simulating a pulsar.  Are bonsai's SNR estimates still unbiased if pulses are repeating (rather than isolated)?

   Here is something we should have done a long time ago!  The variance estimation logic in bonsai assumes that
   pulses are isolated (as expected for FRB's).  It has never been tested on a simulated pulsar, with regularly
   repeating pulses at the same DM.  We should do a quick simulation study to check whether bonsai's SNR estimates
   are still unbiased in this case.

   Here is an example script showing how to inject a simulated pulse into a pipeline run: :ref:`Injecting a simulated pulse`.

   This script should be hackable to inject a simulated pulsar (using a long chain of frb_injector_transforms, this approach will
   waste some CPU time but should be fine for a one-time study!)

 - Channel weighting.  Here is an important topic that we will be working on for a while!

   Currently, bonsai assigns equal weight to each frequency channel.  The optimal weighting would be to
   weight frequency channel "i" by (s_i / v_i), where s_i is the frequency spectrum of the pulsar (i.e.
   the strength of the pulsar in channel i), and v_i is the variance of channel i.  

   We don't know how much the quantity (s_i / v_i) varies from channel to channel, so we don't know
   how suboptimal our current weighting is!

   There is already a ``VarianceEstimator`` class in rf_pipelines, so we should be able to use that
   to get estimates for v_i.  

   Getting estimates for s_i is harder and will require significant new code!  It helps a lot that
   we know the period and dispersion measure of the pulsar in advance.

   ``KMS``: will add an example script showing how to use the VarianceEstimator.

 - Some low-level data quality studies that don't require running the pipeline!

   Is the radiometer equation satisfied?  The radiometer equation states that the variance V
   of the sampled intensity data is related to its mean value by V = (2/N) I^2, where N is the number
   of channelized electric field values which contribute to a sample.  (I believe N=96 for CHIME but
   I need to double-check!)

   The radiometer equation always applies if the intensity samples are formed by summing the squares
   of N uncorrelated Gaussian electric field samples, even if the weighting used to obtain those
   samples is suboptimal.  So if we see large deviations from the radiometer equation, then something
   is seriously wrong "upstream" from the FRB search backend!

   Is quantization noise an issue?  This should be an easy question to answer, we can just compute the
   variance of each channel (with median filtering to remove RFI) and check that it is significantly
   larger than the quantization scale.

   The following example script may be useful: :ref:`Reading a msgpack file`.

 - If we end up finding it difficult to write an RFI transform chain which avoids overclipping bright pulsars,
   here is an idea which may be helpful.

   We can write a pair of transforms, the ``pulsar_masker`` and ``pulsar_unmasker``, which respectively mask
   pulses from a known pulsar, and undo this masking.  Then we can use a weaker level of RFI removal for data
   in pulses than for data outside pulses.  This would be implemented by applying the pulsar_masker, then applying
   "strong" RFI removal, then the pulsar_unmasker, then "weak" RFI removal.

   For this to work, we would need to know the arrival times of the pulses, which is a mini-project in itself!
   Are our timestamps good enough to get this information (the pulsar "ephemeris") from external sources?
   Or do we need to infer the arrival time directly from the data, by running a simplified pulsar search code?

.. _mrafieir/ch_frb_rfi: https://github.com/mrafieir/ch_frb_rfi
