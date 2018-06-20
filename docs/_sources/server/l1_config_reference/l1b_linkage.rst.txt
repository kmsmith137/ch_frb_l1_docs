L1B linkage
===========

  - ``l1b_executable_filename`` (string).

     Filename of the L1b executable.  The L1 server spawns
     L1b subprocesses using the following command line::

        <l1b_executable_filename> <l1b_config_filename> <beam_id>

     Here, l1b_config_filename is one of the command-line arguments when the L1 server is started
     (see [configuration file overview](#user-content-configuration-file-overview) above for the 
     L1 server command-line syntax).  The beam_id is an integer.

     When each L1b subprocess is spawned, its standard input (file descriptor 0) will be connected to a unix pipe
     which will be used to send coarse-grained triggers from L1a to L1b.  The bonsai configuration
     information (e.g. dimensions of coarse-grained trigger arrays) will also be sent over the
     pipe, so there is no need for the bonsai_config_filename to appear on the L1b command line.

     Currently, the L1b process should be written in python, and the `bonsai.PipedDedisperser`
     python class should be used to receive coarse-grained triggers through the pipe.  The
     program `toy-l1b.py` is a toy example, which "processes" coarse-grained triggers by
     combining them into a waterfall plot.

     If l1b_executable_filename is an empty string, then L1b subprocesses will not be spawned.

  - ``l1b_search_path`` (boolean, default=false).

     If true, then duplicate the actions of the
     shell in searching for the l1b executable, by trying all colon-separated directories
     in the $PATH environnment variable.

  - ``l1b_buffer_nsamples`` (integer, default=0).

    Number of time samples which can be buffered between L1a and L1b.

    Under the hood, this gets converted to a buffer size in bytes, which is used to set
    the capacity of the unix pipe between L1 and L1b.  The default (0) means that a
    system default pipe capacity is used (usually 64 kbytes, which is uncomfortably small).

    It is important to note that setting the capacity of a pipe is a linux-only feature!
    Therefore, on other operating systems, setting l1b_buffer_nsamples=0 is the only option.
    In linux, there is also a maximum allowed capacity (/proc/sys/fs/pipe-max-size).  If you
    get an error such as::

       Couldn't set pipe_capacity=XX: You may need to increase /proc/sys/fs/pipe-max-size.

    then you'll need to increase the maximum (as root).  This can be done as follows::

       sudo echo 16777216 | sudo tee /proc/sys/fs/pipe-max-size   # set capacity to 16MB

    but the change will only persist until reboot.  To change it permanently, you can
    create a file `/etc/sysctl.d/pipe-max-size.conf` containing the single line::

       fs.pipe-max-size = 16777216

    A minor detail: when the L1 server computes the pipe capacity from `l1b_buffer_nsamples`, the buffer size
    will be rounded up to a multiple of the bonsai chunk size ('nt_chunk' in the bonsai config 
    file), and a little bit of padding will be added for metadata.

  - ``l1b_pipe_timeout`` (floating-point, default=0).

    Timeout in seconds for the unix pipe connecting L1a and L1b.

    This parameter determines what happens when L1a tries to write to the pipe and the pipe
    is full (presumably because L1b is running slow).  The dedispersion thread will sleep
    until the timeout expires, or the pipe becomes writeable, whichever comes first.  If a
    second write also fails because the pipe is full, then the L1 server will throw an
    exception.  (This will be replaced later by some recovery logic which resets the server.)

    **Important:** the default parameters (l1b_buffer_nsamples = l1b_pipe_timeout = 0) are asking for trouble!  
    In this case, the L1 server will crash if the pipe fills for an instant, and the pipe capacity will be a system 
    default (usually 64 kbytes) which is probably too small to hold the coarse-grained triggers from a single bonsai 
    chunk.  In this situation, the L1 server can crash even in its normal mode of operation, in the middle of sending
    a chunk of data from L1a to L1b.

    In the production L1 server, we plan to set l1b_pipe_timeout=0,
    but set l1b_buffer_nsamples to some reasonable value (say 4096, corresponding to a 4-second buffer).
    This solution is suitable for a real-time search, since it puts a hard limit on how far L1b can
    fall behind in its processing (4 seconds) before it is considered an error.  This configuration only works on Linux,
    which is OK for the real L1 nodes.  This configuration is used in example 3 above.

    In subscale testing, I like to set l1b_pipe_timeout to a reasonable value (a few seconds).
    In this configuration, there is no hard limit on how far L1b can fall behind cumulatively,
    as long as it calls PipedDedisperser.get_triggers() frequently enough.  This configuration
    is used in examples 1 and 2 above.

  - ``l1b_pipe_blocking`` (boolean, default=false).

    If true, then L1a's writes to the pipe will be blocking.
    This has the same effect as setting l1b_pipe_timeout to a huge value.
