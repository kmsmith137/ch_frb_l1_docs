Help! My pipeline is broken
---------------------------

Since the pipeline is under continuous development, and updates to pipeline
modules depend on each other, at some point you may find yourself with an 
inconsistent set of modules.  In this case, you can use the cut-and-paste
recipe below to put all pipeline modules on their master branches,
update from git, and rebuild everything from scratch.

**Warning:** one problem with our current build system is that it doesn't track dependencies
between repositories.  So for example, if you update bonsai and do `make install`, you 
should rebuild everything which depends on bonsai (for example rf_pipelines) from scratch.
Otherwise you can get unpredictable results, such as segfaults.

**Important:** In the previous paragraph, "rebuild from scratch" means `make clean; make all install`.
Rebuilding with `make all install` wouldn't be enough, since dependencies aren't being tracked between repositories!

For this reason, it's easier to end up with a broken pipeline than you might think.
The following sequence of commands will put all pipeline modules on their master branches,
update from git, and rebuild everything.

If you don't have all of these modules installed (e.g. you may not need simpulse, ch_frb_rfi, or ch_frb_l1,
depending on what you're doing), then you can probably just skip the uninstalled ones::

  cd simd_helpers
  git checkout master
  git pull
  make -j4 install
  cd ..

  cd pyclops
  make clean uninstall
  git checkout master
  git pull
  make -j4 all install
  cd ..

  cd rf_kernels
  make clean uninstall
  git checkout master
  git pull
  make -j4 all install
  cd ..

  cd sp_hdf5
  git checkout master
  git pull
  make -j4 all install
  cd ..

  cd simpulse
  make clean uninstall
  git checkout master
  git pull
  make -j4 all install
  cd ..

  cd ch_frb_io
  make clean uninstall
  git checkout master
  git pull
  make -j4 all install
  cd ..

  cd bonsai
  make clean uninstall
  git checkout master
  git pull
  make -j4 all install
  cd ..

  cd rf_pipelines
  make clean uninstall
  git checkout master
  git pull
  make -j4 all install
  cd ..

  cd ch_frb_rfi
  make clean uninstall
  git checkout master
  git pull
  make -j4 install
  cd ..

  cd ch_frb_l1
  make clean
  git checkout master
  git pull
  make -j4 all
  cd ..

