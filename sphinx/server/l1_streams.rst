L1 streams
==========

Now is a good place to explain L1 streams.  The input data to the L1 node
is divided into multiple streams, with the following properties:

 - Each stream corresponds to a unique (ip_address, udp_port) pair.
   For example, a node with four network interfaces, using a single UDP
   port on each, would use four streams.

 - The beams received by the node must be divided evenly between streams.
   For example, if a node is configured with 16 beams and 2 streams, then
   the correlator is responsible for sending 8 beams to each of the node's
   two (ip_address, udp_port) pairs.

 - Each stream is handled by an independent set of threads, and has an
   independent RPC server.  For example, to tell the node to write all
   of its beams to disk, a separate RPC would need to be sent to every
   stream.
   
   If the node has multiple CPU's, then each stream's threads will be
   "pinned" to one of the CPU's.

The stream configuration of an L1 node is determined by the ``ipaddr`` and ``port``
fields in the L1 configuration file.  There is one stream for each distinct
(ipaddr, port) pair.  See the section :ref:`Config reference: L1 server` for more info.

Now let's consider some examples.

  - The "production-scale" 16-beam L1 server, running on an L1 node with
    two CPU's, four 1 Gbps NIC's, and no link bonding.

    In this case, we need to use a different IP address on each NIC.
    Therefore, the L1 node would be configured to use four streams (one
    for each NIC), and the correlator nodes would need
    to be configured to send four beams to each IP address.

  - The "production-scale" 16-beam L1 server with link bonding.  (Link bonding
    is something we were experimenting with at one point, but are
    currently leaning toward not using.)

    In this case, the four NIC's behave as one virtual NIC with
    4 Gbps bandwidth and one IP address.  However, we still
    need to use two streams (rather than one), to divide processing
    between the two CPU's in the node.  The two streams would have
    the same IP address, but would use different UDP ports.  The
    correlator nodes would need to be configured to send 8 beams
    to each UDP port.

  - A "production" L1 server with 8 beams instead of 16 (assuming no
    link bonding).  In this case, there are two possibilities.  We could
    either use two streams (=NIC's) with four beams/NIC, or four streams
    (=NIC's) with two beams/NIC.  Currently, only the first of these
    is implemented in the L1 server.

  - A subscale test case running on a laptop.  In this case there
    is no reason to use more than one stream, but we sometimes use
    multiple streams for testing.

The L1 server can run in one of two modes:

  - A "production-scale" mode which assumes two 10-core CPU's, and
    either 16 beams (on four NIC's), or 8 beams (on two NIC's).
    In this mode, we usually use 16384 frequency channels.
    The L1 server will use 230 GB of memory!

  - A "subscale" mode which assumes <=4 beams, and either 1, 2, or 4 streams.
  
    This is intended for development/debugging (e.g. on a laptop).  In this
    case, you'll almost certainly want to decrease the number of frequency
    channels, so that the memory and CPU usage are reasonable.  With 1024
    frequency channels and 1-4 beams, the L0 simulator and L1 server should
    easily run on a laptop over the "loopback" network interface.
