Config reference: L0 simulator
=============================

In this section, we document the YAML configuration file which is used by the L0 simulator.

  - ``nbeams`` (integer).

    Number of beams being simulated.
    Must match the value of 'nbeams' in the L1 server's config file.

  - ``nfreq`` (integer).

    Number of frequency channels (usually 1024 in subscale testing, or 16384 in production-scale).
    Must match the value of 'nfreq' in the L1 server's config file.

  - ``nt_per_packet`` (integer).

    Number of time samples sent in each UDP packet.  Must match the value of 'nt_per_packet'
    in the L1 server's config file.

  - ``fpga_counts_per_sample`` (integer, default 384).

    Number of FPGA counts per time sample.  Must match the value of 'fpga_counts_per_sample'
    in the L1 server's config file.

    This is an indirect way of specifiying the sampling rate.  One FPGA count corresponds to	
    2.5 microseconds (hardcoded).  Therefore, the default value fpga_counts_per_sample=384
    corresponds to a sampling rate of 0.983 milliseconds.

    One use for this parameter is to artificially speed up or slow down test instances.
    For example, to run a "stress test" in which the L1 server is required to run 10%
    faster than normal, you can take fpga_counts_per_sample=349.  (Note that you'll also
    need to decrease the value of 'dt_sample' in the bonsai config file by 10%, and the
    max DM of the search will automatically decrease by 10%.)
  
  - ``ipaddr`` (either a string, or a list of strings).

    This has the same meaning as the `ipaddr` parameter in the L1 config file (see above).

    It can either be a list of strings (one for each stream) or a single string
    (if all strings use the same IP address).  IP addresses are specified as strings, e.g. ``"127.0.0.1"``.

  - ``port`` (either an integer, or a list of integers).

    This has the same meaning as the `port` parameter in the L1 config file (see above).
    
    One or more UDP ports, for the L1 server's stream(s).  This can be either a list
    of UDP ports (one for each stream), or a single UDP port (if all streams use the same
    port).

  - ``nthreads`` (integer).

    Number of threads used by the L0 simulator.  This must be a multiple of the number of
    streams, i.e. the number of distinct (ipaddr, udp_port) pairs.  Usually I just set nthreads = nstreams.
    
  - ``max_packet_size`` (integer, default 8900).

    If running on a network with ethernet jumbo frames enabled, the default of 8900
    bytes is a good choice.  Otherwise, I suggest 1400.

  - ``nfreq_coarse_per_packet`` (integer, optional).

    If specified, this determines the number of "coarse" frequency channels sent per packet.
    A "coarse" frequency channel is always 1/1024 of the full CHIME band.  For example, if
    nfreq=16384, then one coarse frequency channel contains 16 "fine" frequency channels.

    If unspecified, then nfreq_coarse_per_packet will be automatically determined by
    the max_packet_size.  (We send as many frequency channels as possible, given the
    max packet size constraint, the number of beams and time samples, and some
    internal constraints of the code.)
