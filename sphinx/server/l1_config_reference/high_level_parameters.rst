High-level parameters
=====================

  - ``nbeams`` (integer).

    Number of beams processed by the node.
    If the L0 simulator is also being used, then the value of 'nbeams' in its config file must match.

  - ``nfreq`` (integer).

    Number of frequency channels (usually 1024 in subscale testing, or 16384 in production-scale).
    If the L0 simulator is also being used, then the value of 'nfreq' in its config file must match.

  - ``nt_per_packet`` (integer).

    Number of time samples sent in each UDP packet.
    If the L0 simulator is also being used, then the value of 'nt_per_packet' in its config file must match.

    There is currently a restriction that in order to use fast kernels,
    nt_per_packet must be 16.  In particular, you should take nt_per_packet=16 in production-scale
    runs, where fast kernels are usually a necessity.  If you're using slow kernels,	
    then the value of nt_per_packet is probably not very important.  (For more discussion
    of slow-vs-fast kernels, see 'slow_kernels' below.)

  - ``fpga_counts_per_sample`` (integer, default 384).

    Number of FPGA counts per time sample.
    If the L0 simulator is also being used, then the value of 'fpga_counts_per_sample' in its config file must match.

    This is an indirect way of specifiying the sampling rate.  One FPGA count corresponds to	
    2.5 microseconds (hardcoded).  Therefore, the default value fpga_counts_per_sample=384
    corresponds to a sampling rate of 0.983 milliseconds.

    One use for this parameter is to artificially speed up or slow down test instances.
    For example, to run a "stress test" in which the L1 server is required to run 10%
    faster than normal, you can take fpga_counts_per_sample=349.  (Note that you'll also
    need to decrease the value of 'dt_sample' in the bonsai config file by 10%, and the
    max DM of the search will automatically decrease by 10%.)

  - ``ipaddr`` (either a string, or a list of strings).

    One or more IP addresses, for the L1 server's stream(s).  This can be either a list
    of strings (one for each stream), or a single string (if all streams use the same
    IP address).  IP addresses are specified as strings, e.g. ``"127.0.0.1"`` or ``eno1``.

  - ``port`` (either an integer, or a list of integers).

    One or more UDP ports, for the L1 server's stream(s).  This can be either a list
    of UDP ports (one for each stream), or a single UDP port (if all streams use the same
    port).

  - ``rpc_address`` (list of strings).

    The RPC server address for each stream, specified as a string in "zeromq" format
    (e.g. ``"tcp://127.0.0.1:5555"`` or ``tcp://eno1:5555``).  The 'rpc_address' field must be a list whose length
    is equal to the number of streams on the L1 node, that is, the number of distinct
    (ipaddr, udp_port) pairs.

    The RPC address of each stream must be different (by specifying either a different IP
    address or TCP port for each stream).

  - ``prometheus_address`` (list of strings)

    The L1 server also defines one prometheus server per beam.  The syntax is the same
    as the ``rpc_address`` keyword above.

  - ``logger_address`` (string, optional)

    The IP address of the L1 logging server, specified as a string in "zeromq" format
    (e.g. ``"tcp://10.6.213.19:5555"``).  If unspecified or the empty string, then
    distributed logging will be disabled.

  - ``nrfifreq`` (integer)

    If nonzero, then data files written to disk by the L1 server will contain the RFI mask,
    with the specified number of frequency channels.  Note that the RFI JSON file must contain
    a matching ``mask_counter`` transform with the appropriate frequency resolution.  If zero,
    then data files written by the server will not contain the RFI mask.

  - ``frame0_url`` (string)

    If a nonempty string, then the L1 server will determine the FPGA start time
    by "curl"-ing the specified URL.  This is necessary in order to convert FPGA
    counts to absolute times.  The FPGA start time will be written into the
    data files written to disk by the L1 server.

  - ``frame0_timeout_ms`` (integer, default 3000)

    Timeout for frame0_url curl requests, in milliseconds.
  
  - ``beam_ids`` (list of integers, optional).

    If specified, this is a list of beam_ids which will be processed on the node.  (The
    low-level UDP packet format defines a 32-bit integer beam_id).  The length of the
    list must be 'nbeams'.

    If unspecified, beam_ids defaults to ``[ 0, ..., nbeams-1 ]``.

    Note that in a setup with multiple L1 nodes, we would currently need a separate config
    file for each node, because the beam IDs would be different!  This will be fixed soon,
    by defining config file syntax which allows the beam IDs to be derived from the L1 node's
    IP address.

  - ``intensity_prescale`` (floating-point, optional)

    If 'intensity_prescale' is specified, then all intensity values will be multiplied by its value.
    This is a workaround for 16-bit overflow issues in bonsai.  When data is saved to disk, the
    prescaling will not be applied.

  - ``slow_kernels`` (boolean, default=false).

    By default (slow_kernels=false), the L1 server uses fast assembly-language kernels
    for packet-level operations such as decoding and buffer assembly.  However, there
    is currently a restriction: to use fast kernels, 'nt_per_packet' must be equal to 16,
    and 'nfreq' must be divisible by 2048.  If these conditions are not satisfied, you'll need
    to use slow_kernels=true.

    When running the L1 server at production-scale (~16 beams, ~16384 frequencies),
    you'll probably need to set slow_kernels=false, since the slow reference kernels
    may be too slow to keep up with the data.
