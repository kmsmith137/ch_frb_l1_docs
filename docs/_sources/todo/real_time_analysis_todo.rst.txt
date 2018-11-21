Real-Time Analysis TODO
=======================

 - More testing!  This is not straightforward, since testing the real-time server in a variety of
   use cases is nontrivial.  We probably want to do some groundwork first, in order to make tests 
   easier to write.  For example, it would be really helpful to define python wrappers for the L1 
   server/client, and helper functions for writing unit tests in python.

 - Shift central frequencies, as suggested by Ziggy and Kiyo's analysis of the frequency response
   of our upchannelization scheme.  (This is a trivial change, but we may want to wait until our
   October 27 sensitivity issues are resolved first, as part of a change-one-thing-at-a-time philosophy.)

 - Decrease latency of L1 server.  (Masoud and Kendrick are currently working on this.)

 - Real-time pulse injection.  (Dustin is currently working on this.)

 - Generate timestreams for pulsar search (Alex Roman is currently working on this.)

 - Add RFI mask fraction statistics to Prometheus/Grafana.  In hindsight I think this is really important.
   We're currently trying to figure out whether the RFI environment changed around October 27, and having
   historical RFI mask fractions would have been really useful.

   Dustin is currently working on this, prototype available at
   https://grafana.chimenet.ca/d/whlIPT-mk/l1-rfi-masking-summary?orgId=1&from=1541080903847&to=1541253703847
   but not yet integrated into our primary L1 dashboards (minor permissions problem needs to be resolved).

 - Implement an RFI ultra-coarse-grained viewer, now that we have the "plumbing" in place.

 - Collect statistics for pipeline latency at a few places in the pipeline.  One possible implementation
   would be to add the following fields to the "get statistics" RPC:

     - Largest FPGA count which has been stored in a finalized ``udp_packet_list`` object.  Not exactly
       the same thing as the largest FPGA count received by the network thread!  But this avoids the
       network thread needing to acquire a lock in every iteration of its inner packet loop.

     - Largest FPGA count which has been passed from the assembler thread to the rf_pipelines thread.

     - Largest FPGA count which has been RFI-masked.  This could be implemented by adding a new rf_pipelines
       transform, to be placed between the RFI transforms and the bonsai transform.

     - Last FPGA count which has been dedispersed.

       Warning: this can't be implemented by placing a new rf_pipelines transform after the bonsai_transform (as in
       the previous bullet point).  This is because the bonsai_transform marks a chunk of data "complete" as soon as 
       the data has been copied from the rf_pipelines ring buffer into a bonsai data structure.  (This is so that
       RFI removal and dedispersion can run in separate threads, in parallel without waiting for each other.)

       I (KMS) think the best approach is to add a new thread-safe member function to ``bonsai::dedisperser`` which	
       returns the number of chunks which have been processed so far.  I'll offer to write this, since I'm familiar
       with bonsai internals!

  - Collect statistics for "idle fraction" of different threads in the pipeline.  A nice impementation could be
    to define a std::condition_variable wrapper class which assumes a single waiter, automatically keeps track
    of the waiter's idle fraction, and allows the idle fraction to be queried by an arbitrary thread.  (But,
    if we use this approach, I think we need to switch some pthreads to std::thread.  See "cleanup" item below!)

  - Logging and capturing error messages.  We have a multithreaded logging system (chlog) but we're not
    currently using it consistently (sometimes we call chlog() and sometimes we just use cout).  What should
    we be doing?  (We now run the L1 server as a "service", does this change anything?)

    In practice, the most important case is where the L1 server crashes, and we want to know why.  Usually
    a crash is accompanied by an exception, so we just want to make sure that the exception text gets captured
    and is easily accessible through the high-level webapp.  (It's possible that we're already doing this, and
    I'm just out of the loop :))

    Update: according to Dustin, the logs are already viewable through the webapp (but with a minor permissions
    problem that needs to be resolved).  We do need to be more rigorous about using chlog(), this is a nontrivial
    amount of work.  

  - If the L1 server runs out of memory, then it currently crashes!  This is currently its main failure mode
    (in the typical failure scenario, there is a long-duration RFI storm which triggers continuous write_requests,
    which overload the NFS server and generate a backlog of write_requests on the L1 nodes).

    Instead, the L1 server should cancel write requests in order to reclaim memory, ordered from lowest priority
    to highest.

  - Cleanup/reorganization: factor python code in the ch-frb-l1 repo to its own git repository.  This was requested
    by the McGill team (and seems like a good idea in general, since python users shouldn't need to compiling the C++ server
    and all of its prerequisites).  We should coordinate with everyone on details such as, do we move the webapp to the
    new repo (or would it make more sense to make another new repo for the webapp?)  We should also check to make
    sure we're not introducing conflicts on feature branches (e.g. I think Alex Roman is editing the python RPC client
    on his slow pulsar feature branches).

    Related: currently many python source files are duplicated in the source tree (e.g. ``ch_frb_l1/cnc_ssh.py`` and
    ``ch_frb_l1/webapp/cnc_ssh.py`` are copies of each other).

  - Cleanup: add documentation for all RPC's.  (There is a placeholder section in the manual here: https://kmsmith137.github.io/ch_frb_l1_docs/server/rpc_reference.html)

  - Cleanup: command-line parsing in ch-frb-l1 needs improvement!  What happened here is that we started out with
    "homegrown" command-line parsing, but eventually outgrew it.  We then switched to cxxopts (https://github.com/jarro2783/cxxopts)
    and learned at the last minute that this didn't work on the production L1 nodes, since gcc 4.8 doesn't implement the C++11 regexp
    library.  Currently the code is a homegrown-cxxopts hybrid which isn't very maintainable.

    I think the path of least resistance is to switch again, to CLI11 (https://github.com/CLIUtils/CLI11) which
    explicitly mentions supporting gcc 4.8 as a design goal.  I think this shouldn't be too time-consuming but I
    understand why no one is excited about doing it!  :)

  - Cleanup: switch from pthreads to std::thread.

    The C++11 std::thread API is a lot better than the vintage-1980 pthread API.  (The only reason we still
    use pthreads is that I started out using C++03 instead of C++11, and this never got fully cleaned up!)

  - Cleanup: a lot of kludges in the code to convert between beam ID's and beam indices.  Do we want the
    L1 server to autodetect its beam ID's?

  - Cleanup: ch_frb_l1 is full of kludges to pass data from one thread to another.  In hindsight, we should
    get rid of the different thread context structs, and have every thread's context be a shared_ptr<l1_server>.
    The l1_server would need thread/safe accessors, for example a "setter" which sets a shared_ptr<bonsai::dedisperser>
    (called from the dedispersion thread after initializing and allocating it), and a "getter" which returns a
    shared_ptr<bonsai::dedisperser>, blocking if unavailable (called from the RPC thread, which needs it to
    implement latency monitoring).

  - Cleanup: I think it would be helpful to factor ch_frb_l1 into more functions.  (Random example: L1RpcServer::_handle_request() 
    is currently 500 lines, and factoring into one function for each RPC would be a nice cleanup.)

