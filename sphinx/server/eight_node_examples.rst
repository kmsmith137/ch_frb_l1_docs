Eight-node examples (OUT OF DATE)
=================================

**This part of the manual is out of date, and should be ignored until updated!**

The DRAO backend consists of the following machines:

  - Gateway machines: ``tubular.drao.nrc.ca`` and ``liberty.drao.nrc.ca``.
    All ssh connections to the outside world go through one of these machines!

  - L1 compute nodes: ``cf0g0``, ``cf0g1``, ..., ``cf0g7``.  These machines are diskless and
    share a root filesystem.  The root filesystem is mounted read-write on `cf0g0` and
    mounted read-only on the other nodes.  Therefore, to make changes (such as recompiling,
    editing a config file, etc.) you should use `cf0g0`, and the changes will automatically
    appear on the other nodes.

    There is also an SSD (actually two SSD's in RAID-0) in each compute node, mounted
    at ``/local``.

  - L1 head node: ``cf0hn``.  This exports (via NFS) the root filesystem to the compute nodes,
    and is used for a few other things, like rebooting the nodes (see "Cookbook of miscelleanous
    tasks" below).

  - L4 node: ``cf0g9``.  Our web services run here, and can be accessed from outside DRAO
    using ad hoc ssh tunnels.  See [Web services](#user-content-web-services) below.

  - NFS server: ``cf0fs``.  A central machine where L1 nodes can write data (although currently
    we usually use the local SSD's in the L1 nodes instead of the NFS server).

    Right now our NFS server is a pulsar node which has been retrofitted with a few HDD's.
    It may be a little underpowered, but we have a much larger NFS server coming soon.

Example 5
---------

This is a production-scale example with
nodes ``cf0g[0-3]`` acting as receivers and ``cf0g[4-7]`` acting as senders.
The L1 server will dedisperse 8 beams, with 16384 frequency channels,
and use real RFI removal (as in example 4).

We currently need a separate config file for each node (i.e. node `cf0g0`
uses ``l1_example5_0.yaml``, node `cf0g1` uses ``l1_example5_1.yaml``, etc.)

Note that node `cf0g0` gets all of its packets from `cf0g4`, node `cf0g1` gets
all of its packets from `cf0g5`, etc.  This does not reflect what happens
on the real backend, where every L0 node sends packets to every L1 node.
However it's all we can script with our existing tools!  

  - **Before running example L1 servers on the DRAO backend, use htop to
    check that they are not processing real data!**

  - Log into `cf0g0`, `cf0g1`, `cf0g2`, `cf0g3` separately and start L1 servers::

      # on cf0g0
      ./ch-frb-l1 l1_configs/l1_example5_0.yaml rfi_configs/rfi_production_v1.json /data/bonsai_configs/bonsai_production_noups_nbeta1_v2.hdf5 l1b_placeholder

      # on cf0g1
      ./ch-frb-l1 l1_configs/l1_example5_1.yaml rfi_configs/rfi_production_v1.json /data/bonsai_configs/bonsai_production_noups_nbeta1_v2.hdf5 l1b_placeholder

      # on cf0g2
      ./ch-frb-l1 l1_configs/l1_example5_2.yaml rfi_configs/rfi_production_v1.json /data/bonsai_configs/bonsai_production_noups_nbeta1_v2.hdf5 l1b_placeholder

      # on cf0g3
      ./ch-frb-l1 l1_configs/l1_example5_3.yaml rfi_configs/rfi_production_v1.json /data/bonsai_configs/bonsai_production_noups_nbeta1_v2.hdf5 l1b_placeholder


  - When the servers finish initializing and are listening for packets, log
    into `cf0g4`, `cf0g5`, `cf0g6`, `cf0g7` separately and start L0 simulators::

      # on cf0g4
      ./ch-frb-simulate-l0 l0_configs/l0_example5_4.yaml 1200
    
      # on cf0g5
      ./ch-frb-simulate-l0 l0_configs/l0_example5_5.yaml 1200
    
      # on cf0g6
      ./ch-frb-simulate-l0 l0_configs/l0_example5_6.yaml 1200
    
      # on cf0g7
      ./ch-frb-simulate-l0 l0_configs/l0_example5_7.yaml 1200

