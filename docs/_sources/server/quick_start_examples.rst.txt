Quick-start examples
====================

The following quick-start examples are small enough to run on a laptop.

Example 1
---------

Simplest example: one beam, 1024 frequency channels, one dedispersion tree.
The L0 simulator and L1 server run on the same machine (e.g. a laptop), and exchange packets 
over the loopback interface (127.0.0.1).

  - **This step only needs to be done once.** Initialize the bonsai HDF5 file, 
    using the utility ``bonsai-mkweight``, which should have been installed in 
    your $PATH when bonsai was built::

      cd bonsai_configs/
      bonsai-mkweight bonsai_example1.txt bonsai_example1.hdf5
      cd ..

  - Start the L1 server::

      ./ch-frb-l1  \
         l1_configs/l1_example1.yaml  \
         rfi_configs/rfi_placeholder.json  \
         bonsai_configs/bonsai_example1.hdf5  \
         l1b_config_placeholder

    There are four configuration files, which will be described in the
    next section (:ref:`L1 server parameter files`).

    After you start the L1 server, you should see the line "ch_frb_io: listening for packets..."
    and the server will pause.

  - In another window, start the L0 simulator::

      ./ch-frb-simulate-l0 l0_configs/l0_example1.yaml 30

    This will simulate 30 seconds of data.  If you switch back to the L1 server's window,
    you'll see some incremental output, as chunks of data are processed.  

    After it finishes, you'll see a line "toy-l1b.py: wrote toy_l1b_beam0.png".  This is a 
    plot of the coarse-grained triggers, with time on the x-axis and DM on the y-axis.  The
    plot will not contain any FRB's, because the simulation is pure noise.  Note that the blue 
    "stairstep" region in the left part of the plot is symptomatic of the "slow start" problem
    mentioned previously in :ref:`Caveats`.

  - Optional: if you would like to try sending RPC's, you can either run './rpc-client'
    (C++), or 'python rpc_client.py' (python).  While the L1 server is running::

       # Send get_statistics RPC using a C++ client, and print the result.
       # Port number 5555 from l1_configs/l1_example1.yaml
       ./rpc-client tcp://127.0.0.1:5555

       # Send a few different RPC's using a python client, and print the results.
       # Port number 5555 from l1_configs/l1_example1.yaml
       # See 'python rpc_client.py --help' for a lot of interesting optional arguments.
       python rpc_client.py tcp://127.0.0.1:5555


Example 2
---------

Example 2: similar to example 1, but slightly more complicated as follows.

We process 4 beams, which are divided between UDP ports 6677 and 6688 (two beams per UDP port).
This is more representative of the real L1 server configuration, where we process 4 beams/NIC
with either two or four NIC's (i.e. 8 or 16 beams total).
See the section :ref:`L1 streams` below for more discussion.

In example 2, we also use three dedispersion trees which search different
parts of the (DM, pulse width) parameter space.  See comments in the bonsai
config files for more details (and MANUAL.md in the bonsai repo).
This is more representative of the real search, where we plan to use
6 or 7 trees (I think!)

The steps below are similar to example 1, so discussion is minimal.

  - **This step only needs to be done once.** Initialize the bonsai HDF5 file::

      cd bonsai_configs/
      bonsai-mkweight bonsai_example2.txt bonsai_example2.hdf5
      cd ..

  - Start the L1 server::

      ./ch-frb-l1  \
         l1_configs/l1_example2.yaml  \
         rfi_configs/rfi_placeholder.json  \
         bonsai_configs/bonsai_example2.hdf5  \
         l1b_config_placeholder

    There are four configuration files, which will be described in the
    next section (:ref:`Configuration file overview`).

  - In another window, start the L0 simulator::

       ./ch-frb-simulate-l0 l0_configs/l0_example2.yaml 30

    After the example finishes, you should see four plots `toy_l1b_beam$N.png`,
    where N=0,1,2,3.  Each plot corresponds to one beam, and contains three
    rows of output, corresponding to the three dedispersion trees in this example.

  - Optional: if you would like to try sending RPC's, you can either run './rpc-client'
    (C++), or 'python rpc_client.py' (python).

    In this example, the L1 server defines two streams (see :ref:`L1 streams` below), with 
    associated RPC servers on TCP ports 5555 and 5566 (see l1_configs/l1_example2.yaml).
    Each stream processes two beams.

    While the L1 server is running::

       # Send get_statistics RPC using a C++ client, and print the result.
       ./rpc-client tcp://127.0.0.1:5555
       ./rpc-client tcp://127.0.0.1:5556

       # Send a few different RPC's using a python client, and print the results.
       # See 'python rpc_client.py --help' for a lot of interesting optional arguments.
       python rpc_client.py tcp://127.0.0.1:5555 tcp://127.0.0.1:5556
