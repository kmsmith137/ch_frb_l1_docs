Misc parameters
===============

  - ``force_asynchronous_dedispersion`` (boolean, default=false).

     Forces RFI removal and dedispersion to run in separate threads (shouldn't
     need to specify this explicitly, except for debugging).

  - ``track_global_trigger_max`` (boolean, default=false).

    If track_global_trigger_max=true, then the L1 server will keep track of the FRB with the
    highest signal-to-noise in each beam.  When the L1 server exits, it prints the signal-to-noise,
    arrival time and DM to the terminal.

    This was implemented for early debugging, and is a little superfluous now that L1b is integrated!
