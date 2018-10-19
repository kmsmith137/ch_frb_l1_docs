Buffer sizes
============

The following parameters in the L1 server config file define buffer sizes.

  - ``unassembled_ringbuf_nsamples`` (integer, default 4096).

    The "unassembled" ring buffer sits between the network thread and assembler thread.
    If the assembler thread is running slow, then this ring buffer will start to fill up.
    The unassembled_ringbuf_nsamples parameter sets the size of the ring buffer, in time samples.

    Currently, if the unassembled ring buffer fills up, then the L1 server throws an exception.
    This behavior will eventually be replaced with some recovery logic which resets the server.

  - ``assembled_ringbuf_nsamples`` (integer, default 8192).

    The "assembled" ring buffer sits between the assembler thread and the dedispersion threads.
    If the dedispersion threads are running slow, then this ring buffer will start to fill up.
    The assembled_ringbuf_nsamples parameter sets the size of the ring buffer, in time samples.

    Currently, if the assembled ring buffer fills up, then the L1 server throws an exception.
    This behavior will eventually be replaced with some recovery logic which resets the server.

  - ``telescoping_ringbuf_nsamples`` (list of integers, optional).

    After data is processed by the assembler thread, it goes to the "telescoping" ring buffer,
    which saves it for later retrieval by RPC's.

    As the name suggests, the buffer is telescoping, in the sense that data is saved at
    multiple levels of time downsampling.  For example, the most recent 60 seconds of 
    data might be saved at full time resolution (1 ms), the next 60 seconds of data
    might be saved at 2 ms resolution, and the next 180 seconds might be saved at 4 ms
    resolution.

    The telescoping_ringbuf_nsamples field is a list of integers, which defines how many
    samples (i.e. milliseconds) are saved at each level of downsampling.  The scheme described
    in the previous paragraph could be configured as follows::

      # Telescoping ring buffer configuration
      #      60 seconds at 1 ms time resolution
      #   +  60 seconds at 2 ms time resolution
      #   + 180 seconds at 4 ms time resolution

      telescoping_ringbuf_nsamples = [ 60000, 60000, 180000 ]

    Note that the elements of the telescoping_ringbuf_nsamples list are *non-downsampled*
    sample counts, i.e. the number "180000" above corresponds to (180000 * 1 ms), not
    (180000 * 4 ms).

    If the telescoping_ringbuf_nsamples field is absent (or an empty list) then the
    telescoping ring buffer is disabled, and the node will not save data for RPC-based
    retrieval.

  - ``write_staging_area_gb`` (floating-point, default 0.0)

    Allocates additional memory (in addition to memory reserved for the assembled_ringbuf
    and telescoping_ringbuf) for "staging" intensity data after an RPC write request is
    received, but before the data is actually written to disk or NFS.

    The value of 'write_staging_area_gb' is the total memory reserved on the whole node
    in GB (i.e. not memory per stream, or per beam).  It is highly recommended to set this
    parameter to a nonzero value if you plan to save data with RPC's!

    Currently, there is some guesswork involved in setting this parameter, since it's
    hard to figure out how much memory is being used by other things (e.g. bonsai).
    I plan to address this soon!  In the meantime, I recommend 2 GB/beam for production-scale
    runs, and 0.1 GB/beam for subscale testing runs.

  - ``rfi_mask_meas_history`` (integer, default 300)

    This is the buffer size (in assembled_chunks, which correspond to one second of data)
    for the mask_counter ring buffers.  These are used to implement the RFI real-time web monitor.
