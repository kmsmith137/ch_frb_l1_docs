Configuration file overview
===========================

Before giving more examples, we pause to give an overview
of the various config files used in the L0 simulator
(``ch-frb-simulate-l0``) and the L1 server (``ch-frb-l1``).

L0 simulator parameter file
---------------------------

The L0 simulator command-line syntax is::

   Usage: ch-frb-simulate-l0 <l0_params.yaml> <num_seconds>

The l0_params.yaml file contains high-level info such as
the number of beams being simulated, number of frequency
channels, etc.

I recommend looking at the toy examples first (l0_configs/l0_toy_1beam.yaml and
l0_configs/l0_toy_4beams.yaml) to get a general sense of what they contain.  For
detailed information on the L1 config file, see :ref:`Config reference: L1 server` below.

L1 server parameter files
-------------------------

The L1 server command-line syntax is::

  Usage: ch-frb-l1 [-fvpm] <l1_config.yaml> <rfi_config.json> <bonsai_config.hdf5> <l1b_config_file>
    -f forces the L1 server to run, even if the config files look fishy
    -v increases verbosity of the toplevel ch-frb-l1 logic
    -p enables a very verbose debug trace of the pipe I/O between L1a and L1b
    -m enables a very verbose debug trace of the memory_slab_pool allocation
    -w enables a very verbose debug trace of the logic for writing chunks
    -c deliberately crash dedispersion thread (for debugging, obviously)
    -t starts a "toy server" which assembles packets, but does not run RFI removal,
       dedispersion, or L1B (if -t is specified, then the last 3 arguments are optional)

The L1 server takes four parameter files as follows:

  - **The L1 config file (l1_config.yaml)**

    This is a YAML file which defines "high-level" parameters, such as the number of beams
    being dedispersed, and parameters of the network front-end code, such as ring buffer sizes.

    I recommend looking at the toy examples first (l1_configs/l1_toy_1beam.yaml and
    l1_configs/l1_toy_4beams.yaml) to get a general sense of what they contain.  For
    detailed information on the L1 config file, see :ref:`Config reference: L1 server`.

  - **The RFI config file (rfi_config.json)**

    This is a JSON file which defines the RFI removal algorithm.  It is
    read and interpreted by the rf_pipelines library.  Full documentation
    of the file format, and instructions for creating new versions of this
    file, will be forthcoming in a future releaes.

    Currently, there are two possibilities available in the `rfi_configs` directory:

      - `rfi_configs/rfi_placeholder.json`: a placeholder which detrends
        the data, but does not actually mask RFI.

      - `rfi_configs/rfi_production_v1.json`: a complex 16K-channel RFI removal
        chain developed by Masoud, which is working well on captured data from
        the 26m telescope and the CHIME pathfinder.  It is currently running
        slower than originally hoped (0.55 cores/beam), but we have some
        ideas for improving it and speeding it up.

        Note that this is the same as the file `json_files/rfi_16k/17-10-24-first-try.json`
        in the [ch_frb_rfi repository](https://github.com/mrafieir/ch_frb_rfi).  The idea
        is that RFI transform chains can be developed in the ch_frb_rfi "laboratory" and 
        copied to ch_frb_l1 when we want to use them in the real-time search.

  - **The bonsai config file (bonsai_config.hdf5)**

    This file defines parameters related to dedispersion, such as number of
    trees, their level of downsampling/upsampling, number of trial spectral
    indices, etc.

    Currently, bonsai config files must be constructed by a two-step process as follows.
    First, a human-editable text file `bonsai_xxx.txt` is written (for an example, see
    bonsai_configs/bonsai_example1.txt).  Second, this must be processed into a "config HDF5"
    file using the utility `bonsai-mkweight`::

      bonsai-mkweight bonsai_xxx.txt bonsai_xxx.hdf5

    where that the ``bonsai-mkweight`` utility is part of bonsai, not ch_frb_l1.

    The config HDF5 file contains all of the information in an ordinary config file, plus some large binary arrays.
    The config HDF5 file is not human-readable, but can be inspected with ``bonsai-show-config``.
    The binary array data in the config HDF5 file is needed by the L1 server, to do its real-time RFI-mask-filling
    and trigger variance estimation.

    Note that we don't put config HDF5 files in git, since they are large files, so you may need
    to create them by hand using the above procedure.  Exception: on the CHIME nodes, 
    the "production" config HDF5 files should already be in `/data/bonsai_configs`.

    If the L1 server fails with an error such as::

       bonsai_xxx.txt: transfer matrices not found.  Maybe you accidentally specified a .txt file instead of .hdf5?

    then it's failing to find the binary array data it expects in the config HDF5 file.
    Most likely, this is because an ordinary bonsai config file was specified on the command line,
    instead of a config HDF5 file.

    The utility ``bonsai-show-config`` is useful for viewing the contents of
    a bonsai parameter file, including derived parameters such as the max DM
    of each tree.  The utility ``bonsai-time-dedisperser`` is useful for estimating
    the CPU cost of dedispersion, given a bonsai config file.  (These utilities
    are part of bonsai, not part of ch-frb-l1.)

    The bonsai library is the best-documented part of the L1 pipeline.
    For more information on bonsai, including documentation of the configuration
    file and pointers to example programs, see
    [CHIMEFRB/bonsai/MANUAL.md](https://github.com/CHIMEFRB/bonsai/blob/master/MANUAL.md).

  - **The L1b config file.**

    This file is not read by the L1 server itself (the L1 server does not even check
    whether a file with the given filename exists).  However, the filename is passed from the
    L1 server command line to the L1b command line in the following way.  When the
    L1 server is invoked with the command line::

      ch-frb-l1 <l1_config.yaml> <rfi_config.json> <bonsai_config.txt> <l1b_config_file>

    it will spawn one L1b subprocess for each beam.  These subprocesses are invoked
    with the command line::

      <l1b_executable_filename> <l1b_config_file> <beam_id>

    where the second argument is passed through from the L1 command line.

    In the quick-start examples from the previous section, the L1b subprocesses
    are instances of the 'toy-l1b.py' executable in the ch_frb_l1 repository.
    This is a toy program which "processes" the coarse-grained triggers by
    generating a big waterfall plot for each beam.  This is mainly intended
    as a way of documenting the L1a-L1b interface, but toy-l1b.py may also
    be useful for debugging, since it gives a simple way to plot the output
    of the L1 server.  It is worth emphasizing that "L1b" can be any
    python script which postprocesses the coarse-grained triggers!
