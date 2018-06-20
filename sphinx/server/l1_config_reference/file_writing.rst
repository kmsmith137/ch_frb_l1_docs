File-writing parameters
=======================

  - ``output_devices`` (list of strings).

    This is a list of devices (or filesystems) on the L1 server which can be written to independently.
    Each output_device is identified by a pathname (usually the mount point of a filesystem) such as ``"/ssd"``
    or ``"/frb-archiver1"``.  Each output_device will get a separate I/O thread.

    When the L1 server needs to write a file, it looks for a "matching" output_device whose identifying pathname is a prefix
    of the filename being written.  For example, the output_device `/ssd` would match the filename `/ssd/dir/file`.
    The file will then be queued for writing by the appropriate I/O thread.

    In subscale testing on a laptop, I usually set ``output_devices: [""]``, which creates one output_device
    which matches all filenames, and a single I/O thread to process all write requests.

    On the real nodes, I usually set::

       output_devices: [ "/ssd", "/frb-archiver-1", "/frb-archiver-2", 
                         "/frb-archiver-3", "/frb-archiver-4" ]

    which defines 5 file I/O threads, corresponding to (4 NIC's) + (1 SSD) in the node.
    Recall that the L1 node is configured so that it "thinks" the NFS server is four different
    servers, mounted on directories /frb-archiver1, /frb-archiver2, /frb-archiver3, /frb-archiver4.  
    File writes to each of these four filesystems will be sent from the corresponding NIC.

    Note that ``output_devices: [ ]`` (an empty list) means that the server spawns no I/O threads and all write_requests
    fail, whereas ``output_devices: [""]`` means that the server spawns one I/O thread which matches every write request.

If the following parameters are defined, then the node will continuously stream all incoming data
to either its local SSD or NFS.

  - ``stream_acqname`` (string, optional).

    If this parameter is specified, then the node will continuously stream all incoming data
    to either its local SSD or NFS.  Warning: it's very easy to use a lot of disk space this way!

    The 'string_acqname' parameter is a unique identifying directory name for the acqisition.
    If the given acquisition already exists (probably from a previous run) then the L1 server will abort.

  - ``stream_devname`` (string, optional).

    Either ``"ssd"`` (the default) or ``"nfs"``.

    NFS bandwidth is limited, so if you're writing to NFS then you probably want to reduce the
    number of beam_ids, by assigning a value to 'stream_beam_ids' (see below).

  - ``stream_beam_ids`` (list of integers, optional).

    A list of beam_ids to stream to disk.

    Must be a subset of 'beam_ids', the set of all beam_ids processed by the server.
    If unspecified, every beam_id processed by the server will be streamed.
