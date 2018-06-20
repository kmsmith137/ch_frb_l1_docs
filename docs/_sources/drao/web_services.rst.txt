Web Services (out-of-date?)
---------------------------

The following documentation is probably out-of-date, and I plan to verify/update it soon!

- Dustin's "webapp", for live L1 monitoring and control.

  There is a persistent instance of the webapp maintained by Dustin, which runs at port 5002 on cf0g9.
  Since this is behind the DRAO firewall, you'll need to create an ad hoc ssh tunnel.
  In a terminal window on your laptop, do::

    ssh -L 5002:cf0g9:5002 tubular

  Leave this window open!  (If you close the ssh session in the window, then the tunnel will terminate.)
  Then point your browser to ``localhost:5002`` and the webapp should appear.  If this doesn't work, let Dustin know!
  
  If for some reason you want to run your own instance of the webapp, you can launch it as follows::

    ssh cf0g9
    cd git/ch_frb_l1
    ./run-webapp.sh l1_configs/l1_production_16beam_webapp.yaml PORT

  where PORT is a TCP port number which doesn't conflict with any our existing services (see "Port number assignments" below).
  Then follow the instructions in the previous paragraph with 5002 replaced by PORT.

- Maya's "web viewer", for viewing results of our offline analysis pipeline.

  There is a persistent instance of the web viewer maintained by Kendrick, which runs at port 5003 on cf0g9.
  The instructions are the same as the "Dustin webapp" case above, with 5002 replaced by 5003.
  (I.e. ``ssh -L 5003:cf0g9:5003 tubular``, then point browser at ``localhost:5003``.)

  If for some reason you want to run your own instance of the web viewer, you can launch it as follows::

    ssh cf0g9
    cd git/rf_pipelines/web_viewer
    ./run-web-viewer.sh /frb-archiver-1/web_viewer PORT

  where PORT is a TCP port number which doesn't conflict with any our existing services (see "Port number assignments" below).
  Then view it through the ssh tunnel as usual (``ssh -L PORT:cf0g9:PORT tubular``, then point browser at ``localhost:PORT``).

- Port number assignments (placeholder section for now, to be fleshed out later)::

    5001 = Michelle's L4 server
    5002 = Dustin's "webapp"
    5003 = Maya's "web viewer"
    5004 = Alex's coarse-grained trigger viewer

    5100-5109 = Davor
    5110-5119 = Michelle
    5120-5129 = Dustin
    5130-5139 = Kendrick
    5140-5149 = Alex
    5150-5159 = Utkarsh

    5555 = L1 RPC  
    UDP 1313 = used by correlator to send real data packets
    UDP 6677 = used for simulated data packets in examples in MANUAL.md

    9090 = Prometheus
    9100 = node_exporter
    9116 = snmp_exporter
    9093 = alertmanager
