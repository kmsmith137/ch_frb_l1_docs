Inventory of machines
---------------------

The DRAO gateway machines are ``tubular.drao.nrc.ca`` and ``liberty.drao.nrc.ca``.
All ssh connections to the outside world go through one of these machines!
You will need to get accounts on these machines before doing any computing at DRAO.

After logging into one of the gateway machines, here are some machines you can ssh to:

  - ``frb-archiver``: large (~150 TB) central file server where we store all of our data.
    You shouldn't run analysis code directly on the file server; instead use an analysis node
    which can access the file server over the network (as ``/frb-archiver-1`` or ``/frb-archiver-2``,
    which access the same server over different physical ethernet networks).

  - ``cfdn7``: seacan node dedicated to offline analysis.

A longer list is coming soon!
