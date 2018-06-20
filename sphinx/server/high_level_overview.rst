High-level overview
===================

Ingredients
-----------

The main high-level components of the L1 code are:

  - ``ch-frb-l1``: The "L1 server".

    This is the master executable, which receives UDP packets
    containing one or more beams, dedisperses each beam in a
    separate thread, and passes coarse-grained triggers to "L1b"
    (which runs as a separate process for each beam).

  - ``ch-frb-simulate-l0``: The "L0 simulator".

    This is for testing the L1 server.  It simulates a packet stream
    and sends it to L1.  Right now it can only simulate noise, but
    FRB's will be added soon!

  - RPC client python library.  (To be documented later.)

  - Monitoring webapp.  (To be documented later.)

Caveats
-------

The L1 server is not finished yet! Please note the following caveats:

  - The L0 simulator can only simulate noise; it cannot
    simulate pulses or replay RFI captures.

  - In the full CHIME parameter space (roughly DM <= 13000 and
    pulse width <= 100 ms), there is currently a technical issue in the
    bonsai code which requires an artificially large bonsai chunk size
    (8 seconds).  This will be fixed soon!  This issue only affects the
    "production-scale" examples, not the subscale examples which can
    run on a laptop.

  - Another technical issue in the bonsai code: the "slow start".  The bonsai
    triggers are all-zero arrays at first, and gradually "activate" as time
    progresses.  This activation process takes ~100 seconds for the lowest DM's,
    and ~600 seconds for the highest DM's!  We will try to reduce these
    timescales in future versions.

    Note: because of the "slow start" problem, the two-node backend examples
    [3](#user-content-example3) and [4](#user-content-example4) in this manual
    have been increased from 5-minute runs to 20-minute runs.

  - Currently, bonsai config files must be constructed by a two-step process as follows.
    First, a human-editable text file `bonsai_xxx.txt` is written (for an example, see
    bonsai_configs/bonsai_example1.txt).  Second, this must be processed into an HDF5
    file using the utility `bonsai-mkweight`::

       bonsai-mkweight bonsai_xxx.txt bonsai_xxx.hdf5

    where the `bonsai-mkweight` utility is part of bonsai, not ch_frb_l1.

    Note that we don't put the HDF5 files in git, since they are large files, so you may need
    to create the hdf5 files by hand using the above procedure.  Exception: on the CHIME nodes, 
    the "production" HDF5 files should already be in `/data/bonsai_configs`.

  - Currently, 16K RFI removal is running slower than originally hoped (0.55 cores/beam),
    so we need to run with 8 beams/node rather than 16 beams/node.

    The L1 server supports either 8 or 16 beams, but currently our best 16-beam configuration
    uses "placeholder" RFI removal (which detrends the data but doesn't actually remove RFI) and the least optimal 
    bonsai configuration (no low-DM upsampled tree or spectral index search).  Our best 8-beam configuration
    uses a real RFI removal scheme developed by Masoud, and the most optimal bonsai configuration
    (with a low-DM upsampled tree and two trial spectral indices).  See :ref:`Example 3` and :ref:`Example 4`
    in the :ref:`Two-node examples` section.
    
  - The L1 server is fragile; if anything goes wrong
    (such as a thread running slow and filling a ring buffer)
    then it will throw an exception and die.

    I find that this is actually convenient for debugging, but
    for production we'll want to carefully enumerate corner cases and
    make sure that the L1 server recovers sensibly.
    
  - The code is in a "pre-alpha" state, and serious testing
    will probably uncover bugs!
