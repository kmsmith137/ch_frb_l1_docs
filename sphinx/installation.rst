Installation
============

Here are installation instructions for the CHIMEFRB L1 code, consisting of the following git repositories.

Depending on what you're doing, you may only need a subset of these!
In particular, the modules marked "frb1 only" include hardcoded pathnames on
`frb1.physics.mcgill.ca`, and probably won't be useful on other machines.

  - `kiyo-masui/bitshuffle`_:
    "bitwise" compression algorithm used throughout CHIME.
  - `kmsmith137/simd_helpers`_:
    header-only library for writing x86 assembly language kernels.
  - `kmsmith137/pyclops`_:
    some hacks for writing hybrid C++/python code.
  - `kmsmith137/rf_kernels`_:
    fast C++/assembly kernels for RFI removal and related tasks.
  - `kmsmith137/sp_hdf5`_:
    header-only library for reading/writing hdf5 from C++.
  - `kmsmith137/simpulse`_:
    library for simulating FRB's and pulsars.
  - `CHIMEFRB/ch_frb_io`_:
    networking code, CHIME-specific file formats.
  - `CHIMEFRB/bonsai`_:
    fast tree dedispersion on x86.
  - `kmsmith137/rf_pipelines`_:
    plugin-based radio astronomy pipelines.  
    (Note: this repo now includes the web viewer code which was previously
    in `mburhanpurkar/web_viewer`_.)
  - `mrafieir/ch_frb_rfi`_:
    scritping framework for RFI removal and offline L1 analysis.  `(frb1 only)`
  - `kmsmith137/ch_frb_l1`_:
    toplevel repo, whose documentation you're reading right now.

Prerequisites
-------------

If you're compiling on one of the CHIME machines, or Kendrick's desktop (orangutan),
then all of these should already be installed, and you can skip to the next step (`Compiling bitshuffle`_).


  - Python-centric things which can be installed painlessly with `pip`::

       pip install numpy
       pip install scipy
       pip install matplotlib
       pip install Pillow
       pip install h5py
       pip install Cython
       pip install zmq
       pip install msgpack-python
       pip install pyyaml

    To install without root privileges, do ``pip install --user``.
    To upgrade a previous pip install, do ``pip install --upgrade``.

    You might need to upgrade your cython, since bonsai currently requires a very
    recent cython (I know that cython 0.24 works, and cython 0.20 is too old).


  - libhdf5. 

    **Currently, the pipeline requires HDF5 version 1.8.12 or later,
    but does not work with version 1.10.x.  This will be fixed eventually!**

    In the meantime, for instructions for installing a version of HDF5
    which is neither too old nor too new, please see `kmsmith137/sp_hdf5/README.md`_.

  - lz4.  

      - osx one-liner: ``brew install lz4``
      - centos one-liner: ``sudo yum install lz4-devel``
      - ubuntu one-liner: ``sudo apt-get install liblz4-dev``

  - msgpack.

      - osx one-liner: ``brew install msgpack``
      - centos one-liner: ``sudo yum install msgpack-devel.x86_64``
      - ubuntu: don't install the apt-get version, it is too old!  (e.g. it is missing `/usr/include/msgpack/fbuffer.hpp`).
        Instead you should build from scratch, see next bullet point.

      - Building from scratch.  This is easy because we only use the msgpack headers, not the compiled library.
        You can either follow Kendrick's procedure for building from scratch::
          git clone https://github.com/msgpack/msgpack-c
          sudo cp -r msgpack-c/include/* /usr/local/include
        or Dustin's procedure: download the `msgpack source package`_,
        and then extract it and add its subdirectory ``msgpack-2.1.0/include`` into the
        include path.

  - zeromq and cppzmq.  

    - centos one-liner: ``sudo yum install cppzmq-devel.x86_64``
    - ubuntu: don't use the apt-get packages, they are too old!.  You'll need to build both zeromq and cppzmq from scratch, see bullet point below.
    - osx: zeromq can be installed with ``brew install zeromq``, but you'll need to build cppzmq from scratch, see bullet point below.
    - Building zmq from scratch.  Download from zeromq.org, and then do::

       ./configure --prefix=/usr/local
       make
       sudo make install

    - Building cppzmq from scratch.  Since it's a header-only library with two source files, I just ignored the build system and did::

       git clone https://github.com/zeromq/cppzmq.git
       cd cppzmq
       sudo cp zmq.hpp zmq_addon.hpp /usr/local/include

  - `jsoncpp`_

    - osx one-liner: ``brew install jsoncpp``
    - centos one-liner: ``sudo yum install jsoncpp-devel``
    - ubuntu one-liner: ``sudo apt-get install libjsoncpp-dev``
    - Building jsoncpp from scratch is a pain, but the following procedure worked for me::

        git clone https://github.com/open-source-parsers/jsoncpp
        mkdir -p build/debug
        cd build/debug
        cmake -DCMAKE_INSTALL_PREFIX=$HOME -DCMAKE_CXX_FLAGS=-fPIC -DCMAKE_C_FLAGS=-fPIC -DCMAKE_BUILD_TYPE=debug -G "Unix Makefiles" ../..
        make install

   - yaml-cpp_

    - osx one-liner: ``brew install yaml-cpp``.
    - centos one-liner: ``sudo yum install yaml-cpp-devel``.
    - ubuntu two-liner::

        sudo apt-get install libboost-all-dev    # overkill?
        sudo apt-get install libyaml-cpp-dev

      Note: if only libyaml-cpp-dev is installed, then some necessary boost libraries will be missing.
      Installing libboost-all-dev fixes this, but also installs around 200MB of software!  I didn't
      bother trying to figure out exactly which boost libraries were needed.


Compiling bitshuffle
--------------------

  You'll need this if you want to read or write bitshuffle-compressed files with ch_frb_io
  (note that CHIME pathfinder data is generally bitshuffle-compresed).

  The following recipe worked for me::

     git clone https://github.com/kiyo-masui/bitshuffle.git
     cd bitshuffle/

     # The HDF5 library can dynamically load the bitshuffle plugin, i.e. you don't need
     # to link the bitshuffle library when you compile ch_frb_io, but you need to set this
     # environment variable to tell libhdf5 where to look.  Suggest adding this to .bashrc!

     export HDF5_PLUGIN_PATH=$HOME/lib/hdf5_plugins

     # If you have root privileges and want to install "system-wide", omit the --user flag
     # The --h5plugin* flags will build/install the plugin needed to use bitshuffle from C++

     python setup.py install --user --h5plugin --h5plugin-dir=$HOME/lib/hdf5_plugins

  If you run into trouble, you'll want to refer to the installation instructions in the bitshuffle repo.


Compiling the core packages
---------------------------

If you're installing on `frb1.physics.mcgill.ca`, then you can disregard this section
and refer to `Quick install: frb1`_ below.

If you're installing on a CHIME compute node (e.g. `frb-compute-0.physics.mcgill.ca`, 
`cf0g0.drao.nrc.ca`), then you can disregard this section and refer to 
`Quick install: compute node`_ below.

If you're using another machine (e.g. a laptop) then the installation process
is more involved.  You'll probably need to write some "Makefile.local" files,
as described next.  We hope to streamline this process at some point!

These instructions apply to the following github repos (i.e. everything except bitshuffle):

  - `kmsmith137/simd_helpers`_:
    header-only library for writing x86 assembly language kernels.
  - `kmsmith137/pyclops`_:
    some hacks for writing hybrid C++/python code.
  - `kmsmith137/rf_kernels`_:
    fast C++/assembly kernels for RFI removal and related tasks.
  - `kmsmith137/sp_hdf5`_:
    header-only library for reading/writing hdf5 from C++.
  - `kmsmith137/simpulse`_:
    library for simulating FRB's and pulsars.
  - `CHIMEFRB/ch_frb_io`_:
    networking code, CHIME-specific file formats.
  - `CHIMEFRB/bonsai`_:
    fast tree dedispersion on x86.
  - `kmsmith137/rf_pipelines`_:
    plugin-based radio astronomy pipelines.  
    (Note: this repo now includes the web viewer code which was previously
    in `mburhanpurkar/web_viewer`_.)
  - `mrafieir/ch_frb_rfi`_:
    scritping framework for RFI removal and offline L1 analysis.  `(frb1 only)`
  - `kmsmith137/ch_frb_l1`_:
    toplevel repo, whose documentation you're reading right now.

They use a klunky build procedure which we should improve some day!
Roughly, it works like this.  For each package, in the order above,
you'll need to do the following:

   - Create a file ``Makefile.local`` in the toplevel directory which defines
     a bunch of machine-dependent variables, such as compiler flags, install directories,
     and boolean flags indicating which optional dependencies are available.  

     The variables which need to be defined are slightly different for each of the 
     packages above, and are listed in the Makefile.  However, it's easiest to
     start with one of the template Makefile.locals in the ``site/`` subdirectory of
     the toplevel directory, and either modify it, or just copy/symlink it to the
     toplevel directory if it doesn't need modification.
     
   - Type ``make all install``

   - Some of these packages have unit tests which you may want to run; see the 
     per-package README file for details.

Some more notes on writing Makefile.local files:

  - The bonsai package has an optional dependency on libpng which you'll want to enable for CHIMEFRB.
    Therefore, your Makefile.local should contain the line::

      HAVE_PNG=y


  - The rf_pipelines package has the following optional dependencies which you'll want to enable::

      HAVE_BONSAI=y
      HAVE_CH_FRB_IO=y
      HAVE_SIMPULSE=y
      HAVE_HDF5=y
      HAVE_PNG=y

    (There is also an optional dependency on psrfits which isn't important for CHIMEFRB.)

  - Some of the packages need to include header files from your python installation.
    This is the case if the example Makefile.locals contain lines like these::

      # This directory should contain e.g. Python.h
      PYTHON_INCDIR=/usr/include/python2.7

      # This directory should contain e.g. numpy/arrayobject.h
      NUMPY_INCDIR=/usr/lib64/python2.7/site-packages/numpy/core/include

      CPP=g++ -I$(PYTHON_INCDIR) -I$(NUMPY_INCDIR) ...

    It's important that these directories correspond to the versions of python/numpy
    that you're actually using!  (There may some confusion if more than one python interpreter
    is installed on your machine.)  The safest thing to do is to determine these directions
    from within the python interpreter itself, as follows::

      import distutils.sysconfig
      print distutils.sysconfig.get_python_inc()   # prints PYTHON_INCDIR

      import numpy
      print numpy.get_include()    # prints NUMPY_INCDIR

  - Each package also defines some installation directories, e.g. Makefile.local will contain something like this::

      # Directory where executables will be installed
      BINDIR=$(HOME)/bin

      # Directory where C++ libraries will be installed
      LIBDIR=$(HOME)/lib

      # Directory where C++ header files will be installed
      INCDIR=$(HOME)/include

      # Directory where python and cython modules will be installed
      PYDIR=$(HOME)/lib/python2.7/site-packages

    You'll want to make sure that your PATH, PYTHONPATH, and LD_LIBRARY_PATH environment variables
    contain the BINDIR, PYDIR, and LIBDIR directories from the Makefile.local.  For example, given the
    Makefile.local above, your ``$HOME/.bashrc`` should contain something like this::

      export PATH=$HOME/bin:$PATH
      export PYTHONPATH=$HOME/lib/python2.7/site-packages:$PYTHONPATH
      export LD_LIBRARY_PATH=$HOME/lib:$LD_LIBRARY_PATH

    (Note: on osx, you should use DYLD_LIBRARY_PATH environment variable instead of LD_LIBRARY_PATH.)


Quick install: frb1
-------------------

Here are instructions for building the L1 pipeline from scratch on frb1.physics.mcgill.ca.
All external dependencies should already be installed.

Directories and environment variables::

  # Binaries, header files, libraries, and python modules will be installed in these directories.
  mkdir -p ~/bin
  mkdir -p ~/include
  mkdir -p ~/lib
  mkdir -p ~/lib/python2.7/site-packages

  # Bitshuffle will be installed here.
  mkdir -p ~/lib/hdf5_plugins

  # I strongly recommend adding these lines to your ~/.bashrc!
  # Note that '.' is added to LD_LIBRARY_PATH (the unit testing logic in most of
  # the pipeline modules currently assumes this)

  export LD_LIBRARY_PATH=.:$HOME/lib:/usr/local/lib:$LD_LIBRARY_PATH
  export PYTHONPATH=$HOME/lib/python2.7/site-packages:$PYTHONPATH
  export HDF5_PLUGIN_PATH=$HOME/lib/hdf5_plugins

Checking out the pipeline modules::

  git clone https://github.com/kiyo-masui/bitshuffle
  git clone https://github.com/kmsmith137/simd_helpers
  git clone https://github.com/kmsmith137/pyclops
  git clone https://github.com/kmsmith137/rf_kernels
  git clone https://github.com/kmsmith137/sp_hdf5
  git clone https://github.com/kmsmith137/simpulse
  git clone https://github.com/CHIMEFRB/ch_frb_io
  git clone https://github.com/CHIMEFRB/bonsai
  git clone https://github.com/kmsmith137/rf_pipelines
  git clone https://github.com/mrafieir/ch_frb_rfi
  git clone https://github.com/kmsmith137/ch_frb_l1

Compilation::

  cd bitshuffle
  python setup.py install --user --h5plugin --h5plugin-dir=$HOME/lib/hdf5_plugins
  cd ..

  cd simd_helpers
  ln -s site/Makefile.local.norootprivs Makefile.local
  make -j4 install
  cd ..

  cd pyclops
  ln -s site/Makefile.local.frb1 Makefile.local
  make -j4 all install
  cd ..

  cd rf_kernels
  ln -s site/Makefile.local.frb1 Makefile.local
  make -j4 all install
  cd ..

  cd sp_hdf5
  ln -s site/Makefile.local.linux Makefile.local
  make -j4 all install
  cd ..

  cd simpulse
  ln -s site/Makefile.local.frb1 Makefile.local
  make -j4 all install
  cd ..

  cd ch_frb_io
  ln -s site/Makefile.local.frb1 Makefile.local
  make -j4 all install
  cd ..

  cd bonsai
  ln -s site/Makefile.local.frb1 Makefile.local
  make -j4 all install
  cd ..

  cd rf_pipelines
  ln -s site/Makefile.local.frb1 Makefile.local
  make -j4 all install
  cd ..

  cd ch_frb_rfi
  ln -s site/Makefile.local.frb1 Makefile.local
  make -j4 install
  cd ..

  cd ch_frb_l1
  ln -s site/Makefile.local.frb1 Makefile.local
  make -j4 all
  cd ..


Quick install: compute node
---------------------------

Here are instructions for building the L1 pipeline from scratch on the frb-compute-X nodex.
All external dependencies should already be installed.

Note that we don't build the `ch_frb_rfi` module here, since this module includes hardcoded
pathnames on `frb1.physics.mcgill.ca`.

Directories and environment variables::

  # Binaries, header files, libraries, and python modules will be installed in these directories.
  mkdir -p ~/bin
  mkdir -p ~/include
  mkdir -p ~/lib
  mkdir -p ~/lib/python2.7/site-packages

  # Bitshuffle will be installed here.
  mkdir -p ~/lib/hdf5_plugins

  # I strongly recommend adding these lines to your ~/.bashrc!
  # Note that '.' is added to LD_LIBRARY_PATH (the unit testing logic in most of
  # the pipeline modules currently assumes this)

  export LD_LIBRARY_PATH=.:$HOME/lib:/usr/local/lib:$LD_LIBRARY_PATH
  export PYTHONPATH=$HOME/lib/python2.7/site-packages:$PYTHONPATH
  export HDF5_PLUGIN_PATH=$HOME/lib/hdf5_plugins

Checking out the pipeline modules::

  git clone https://github.com/kiyo-masui/bitshuffle
  git clone https://github.com/kmsmith137/simd_helpers
  git clone https://github.com/kmsmith137/pyclops
  git clone https://github.com/kmsmith137/rf_kernels
  git clone https://github.com/kmsmith137/sp_hdf5
  git clone https://github.com/kmsmith137/simpulse
  git clone https://github.com/CHIMEFRB/ch_frb_io
  git clone https://github.com/CHIMEFRB/bonsai
  git clone https://github.com/kmsmith137/rf_pipelines
  git clone https://github.com/kmsmith137/ch_frb_l1

Compilation::

  cd bitshuffle
  python setup.py install --user --h5plugin --h5plugin-dir=$HOME/lib/hdf5_plugins
  cd ..

  cd simd_helpers
  ln -s site/Makefile.local.norootprivs Makefile.local
  make -j20 install
  cd ..

  cd pyclops
  ln -s site/Makefile.local.frb-compute-0 Makefile.local
  make -j20 all install
  cd ..

  cd rf_kernels
  ln -s site/Makefile.local.frb-compute-0 Makefile.local
  make -j20 all install
  cd ..

  cd sp_hdf5
  ln -s site/Makefile.local.linux Makefile.local
  make -j20 all install
  cd ..

  cd simpulse
  ln -s site/Makefile.local.frb-compute-0 Makefile.local
  make -j20 all install
  cd ..

  cd ch_frb_io
  ln -s site/Makefile.local.frb-compute-0 Makefile.local
  make -j20 all install
  cd ..

  cd bonsai
  ln -s site/Makefile.local.frb-compute-0 Makefile.local
  make -j20 all install
  cd ..

  cd rf_pipelines
  ln -s site/Makefile.local.frb-compute-0 Makefile.local
  make -j20 all install
  cd ..

  cd ch_frb_l1
  ln -s site/Makefile.local.frb-compute-0 Makefile.local
  make -j20 all
  cd ..


.. _kiyo-masui/bitshuffle: https://github.com/kiyo-masui/bitshuffle
.. _kmsmith137/simd_helpers: https://github.com/kmsmith137/simd_helpers
.. _kmsmith137/pyclops: https://github.com/kmsmith137/pyclops
.. _kmsmith137/rf_kernels: https://github.com/kmsmith137/rf_kernels
.. _kmsmith137/sp_hdf5: https://github.com/kmsmith137/sp_hdf5
.. _kmsmith137/simpulse: https://github.com/kmsmith137/simpulse
.. _CHIMEFRB/ch_frb_io: https://github.com/CHIMEFRB/ch_frb_io
.. _CHIMEFRB/bonsai: https://github.com/CHIMEFRB/bonsai
.. _kmsmith137/rf_pipelines: https://github.com/kmsmith137/rf_pipelines
.. _mburhanpurkar/web_viewer: https://github.com/mburhanpurkar/web_viewer
.. _mrafieir/ch_frb_rfi: https://github.com/mrafieir/ch_frb_rfi
.. _kmsmith137/ch_frb_l1: https://github.com/kmsmith137/ch_frb_l1
.. _kmsmith137/sp_hdf5/README.md: https://github.com/kmsmith137/sp_hdf5/blob/master/README.md
.. _msgpack source package: https://github.com/msgpack/msgpack-c/releases/download/cpp-2.1.0/msgpack-2.1.0.tar.gz
.. _jsoncpp: https://github.com/open-source-parsers/jsoncpp
.. _yaml-cpp_: https://github.com/jbeder/yaml-cpp
