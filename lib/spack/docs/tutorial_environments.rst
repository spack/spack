.. Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _environments-tutorial:

=====================
Environments Tutorial
=====================

We've shown you how to install and remove packages with Spack.  You can
use :ref:`cmd-spack-install` to install packages,
:ref:`cmd-spack-uninstall` to remove them, and :ref:`cmd-spack-find` to
look at and query what is installed.  We've also shown you how to
customize Spack's installation with configuration files like
:ref:`packages.yaml <build-settings>`.

If you build a lot of software, or if you work on multiple projects,
managing everything in one place can be overwhelming. The default ``spack
find`` output may contain many packages, but you may want to *just* focus
on packages for a particular project.  Moreover, you may want to include
special configuration with your package groups, e.g., to build all the
packages in the same group the same way.

Spack **environments** provide a way to handle these problems.

-------------------
Environment basics
-------------------

Let's look at the output of ``spack find`` at this point in the tutorial.

.. code-block:: console

   $ spack find
   ==> 70 installed packages
   -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
   tcl@8.6.8  zlib@1.2.8  zlib@1.2.11

   -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
   zlib@1.2.11

   -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
   adept-utils@1.0.1  hdf5@1.10.4          mpc@1.1.0               perl@5.26.2
   autoconf@2.69      hdf5@1.10.4          mpfr@3.1.6              pkgconf@1.4.2
   automake@1.16.1    hdf5@1.10.4          mpich@3.2.1             readline@7.0
   boost@1.68.0       hwloc@1.11.9         mpileaks@1.0            suite-sparse@5.3.0
   bzip2@1.0.6        hypre@2.15.1         mumps@5.1.1             tar@1.30
   callpath@1.0.4     hypre@2.15.1         mumps@5.1.1             tcl@8.6.8
   cmake@3.12.3       isl@0.18             ncurses@6.1             tcl@8.6.8
   diffutils@3.6      libdwarf@20180129    netcdf@4.6.1            texinfo@6.5
   dyninst@9.3.2      libiberty@2.31.1     netcdf@4.6.1            trilinos@12.12.1
   elfutils@0.173     libpciaccess@0.13.5  netlib-scalapack@2.0.2  trilinos@12.12.1
   findutils@4.6.0    libsigsegv@2.11      netlib-scalapack@2.0.2  util-macros@1.19.1
   gcc@7.2.0          libtool@2.4.6        numactl@2.0.11          xz@5.2.4
   gdbm@1.14.1        libxml2@2.9.8        openblas@0.3.3          zlib@1.2.8
   gettext@0.19.8.1   m4@1.4.18            openmpi@3.1.3           zlib@1.2.8
   glm@0.9.7.1        matio@1.5.9          openssl@1.0.2o          zlib@1.2.11
   gmp@6.1.2          matio@1.5.9          parmetis@4.0.3
   hdf5@1.10.4        metis@5.1.0          parmetis@4.0.3


This is a complete, but cluttered view.  There are packages built with
both ``openmpi`` and ``mpich``, as well as multiple variants of other
packages, like ``zlib``.  The query mechanism we learned about in ``spack
find`` can help, but it would be nice if we could start from a clean
slate without losing what we've already done.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Creating and activating environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``spack env`` command can help.  Let's create a new environment:

.. code-block:: console

   $ spack env create myproject
   ==> Created environment 'myproject' in ~/spack/var/spack/environments/myproject

An environment is a virtualized ``spack`` instance that you can use for a
specific purpose.  You can see the environments we've created so far like this:

.. code-block:: console

   $ spack env list
   ==> 1 environments
       myproject

And you can **activate** an environment with ``spack env activate``:

.. code-block:: console

   $ spack env activate myproject

Once you enter an environment, ``spack find`` shows only what is in the
current environment.  That's nothing, so far:

.. code-block:: console

   $ spack find
   ==> In environment myproject
   ==> No root specs

   ==> 0 installed packages

The ``spack find`` output is still *slightly* different.  It tells you
that you're in the ``myproject`` environment, so that you don't panic
when you see that there is nothing installed.  It also says that there
are *no root specs*.  We'll get back to what that means later.

If you *only* want to check what environment you are in, you can use
``spack env status``:

.. code-block:: console

   $ spack env status
   ==> In environment myproject

And, if you want to leave this environment and go back to normal Spack,
you can use ``spack env deactivate``.  We like to use the
``despacktivate`` alias (which Spack sets up automatically) for short:

.. code-block:: console

   $ despacktivate     # short alias for `spack env deactivate`
   $ spack env status
   ==> No active environment
   $ spack find
   netcdf@4.6.1            readline@7.0        zlib@1.2.11
   diffutils@3.6      hdf5@1.10.4       m4@1.4.18            netcdf@4.6.1            suite-sparse@5.3.0
   dyninst@10.0.0     hwloc@1.11.9      matio@1.5.9          netlib-scalapack@2.0.2  tar@1.30
   elfutils@0.173     hypre@2.15.1      matio@1.5.9          netlib-scalapack@2.0.2  tcl@8.6.8
   findutils@4.6.0    hypre@2.15.1      metis@5.1.0          numactl@2.0.11          tcl@8.6.8
   gcc@7.2.0          intel-tbb@2019    mpc@1.1.0            openblas@0.3.3          texinfo@6.5~


^^^^^^^^^^^^^^^^^^^
Installing packages
^^^^^^^^^^^^^^^^^^^

Ok, now that we understand how creation and activation work, let's go
back to ``myproject`` and *install* a few packages:

.. code-block:: console

   $ spack env activate myproject
   $ spack install tcl
   ==> tcl is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/tcl-8.6.8-qhwyccywhx2i6s7ob2gvjrjtj3rnfuqt
   $ spack install trilinos
   ==> trilinos is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1-rlsruavxqvwk2tgxzxboclbo6ykjf54r
   $ spack find
   ==> In environment myproject
   ==> Root specs
   tcl  trilinos

   ==> 22 installed packages
   -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
   boost@1.68.0  hwloc@1.11.9         matio@1.5.9   netlib-scalapack@2.0.2  parmetis@4.0.3      xz@5.2.4
   bzip2@1.0.6   hypre@2.15.1         metis@5.1.0   numactl@2.0.11          suite-sparse@5.3.0  zlib@1.2.11
   glm@0.9.7.1   libpciaccess@0.13.5  mumps@5.1.1   openblas@0.3.3          tcl@8.6.8
   hdf5@1.10.4   libxml2@2.9.8        netcdf@4.6.1  openmpi@3.1.3           trilinos@12.12.1

We've installed ``tcl`` and ``trilinos`` in our environment, along with
all of their dependencies.  We call ``tcl`` and ``trilinos`` the
**roots** because we asked for them explicitly.  The other 20 packages
listed under "installed packages" are present because they were needed as
dependencies.  So, these are the roots of the packages' dependency graph.

The "<package> is already installed" messages above are generated because
we already installed these packages in previous steps of the tutorial,
and we don't have to rebuild them to put them in an environment.

Now let's create *another* project.  We'll call this one ``myproject2``:

.. code-block:: console

   $ spack env create myproject2
   ==> Created environment 'myproject2' in ~/spack/var/spack/environments/myproject2
   $ spack env activate myproject2
   $ spack install hdf5
   ==> hdf5 is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4-ozyvmhzdew66byarohm4p36ep7wtcuiw
   $ spack install trilinos
   ==> trilinos is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1-rlsruavxqvwk2tgxzxboclbo6ykjf54r
   $ spack find
   ==> In environment myproject2
   ==> Root specs
   hdf5  trilinos

   ==> 22 installed packages
   -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
   boost@1.68.0  hdf5@1.10.4          libxml2@2.9.8  netcdf@4.6.1            openmpi@3.1.3       xz@5.2.4
   bzip2@1.0.6   hwloc@1.11.9         matio@1.5.9    netlib-scalapack@2.0.2  parmetis@4.0.3      zlib@1.2.11
   glm@0.9.7.1   hypre@2.15.1         metis@5.1.0    numactl@2.0.11          suite-sparse@5.3.0
   hdf5@1.10.4   libpciaccess@0.13.5  mumps@5.1.1    openblas@0.3.3          trilinos@12.12.1

Now we have two environments: one with ``tcl`` and ``trilinos``, and
another with ``hdf5`` and ``trilinos``.

We can uninstall trilinos from ``myproject2`` as you would expect:

.. code-block:: console

   $ spack uninstall trilinos
   ==> The following packages will be uninstalled:

       -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
       rlsruav trilinos@12.12.1%gcc~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2
   ==> Do you want to proceed? [y/N] y
   $ spack find
   ==> In environment myproject2
   ==> Root specs
   hdf5

   ==> 8 installed packages
   -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
   hdf5@1.10.4   libpciaccess@0.13.5  numactl@2.0.11  xz@5.2.4
   hwloc@1.11.9  libxml2@2.9.8        openmpi@3.1.3   zlib@1.2.11

Now there is only one root spec, ``hdf5``, which requires fewer
additional dependencies.

However, we still needed ``trilinos`` for the ``myproject`` environment!
What happened to it?  Let's switch back and see.

.. code-block:: console

   $ despacktivate
   $ spack env activate myproject
   $ spack find
   ==> In environment myproject
   ==> Root specs
   tcl  trilinos

   ==> 22 installed packages
   -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
   boost@1.68.0  hwloc@1.11.9         matio@1.5.9   netlib-scalapack@2.0.2  parmetis@4.0.3      xz@5.2.4
   bzip2@1.0.6   hypre@2.15.1         metis@5.1.0   numactl@2.0.11          suite-sparse@5.3.0  zlib@1.2.11
   glm@0.9.7.1   libpciaccess@0.13.5  mumps@5.1.1   openblas@0.3.3          tcl@8.6.8
   hdf5@1.10.4   libxml2@2.9.8        netcdf@4.6.1  openmpi@3.1.3           trilinos@12.12.1


Spack is smart enough to realize that ``trilinos`` is still present in
the other environment.  Trilinos won't *actually* be uninstalled unless
it is no longer needed by any environments or packages.  If it is still
needed, it is only removed from the environment.

-------------------------------
Dealing with many specs at once
-------------------------------

In the above examples, we just used ``install`` and ``uninstall``.  There
are other ways to deal with groups of packages, as well.

^^^^^^^^^^^^^
Adding specs
^^^^^^^^^^^^^

Let's go back to our first ``myproject`` environment and *add* a few specs instead of installing them:

.. code-block:: console

   $ spack add hdf5
   ==> Adding hdf5 to environment myproject
   $ spack add gmp
   ==> Adding mumps to environment myproject
   $ spack find
   ==> In environment myproject
   ==> Root specs
   gmp  hdf5  tcl  trilinos

   ==> 22 installed packages
   -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
   boost@1.68.0  hwloc@1.11.9         matio@1.5.9   netlib-scalapack@2.0.2  parmetis@4.0.3      xz@5.2.4
   bzip2@1.0.6   hypre@2.15.1         metis@5.1.0   numactl@2.0.11          suite-sparse@5.3.0  zlib@1.2.11
   glm@0.9.7.1   libpciaccess@0.13.5  mumps@5.1.1   openblas@0.3.3          tcl@8.6.8
   hdf5@1.10.4   libxml2@2.9.8        netcdf@4.6.1  openmpi@3.1.3           trilinos@12.12.1

Let's take a close look at what happened.  The two packages we added,
``hdf5`` and ``gmp``, are present, but they're not installed in the
environment yet.  ``spack add`` just adds *roots* to the environment, but
it does not automatically install them.

We can install *all* the as-yet uninstalled packages in an environment by
simply running ``spack install`` with no arguments:

.. code-block:: console

   $ spack install
   ==> Concretizing hdf5
   [+]  ozyvmhz  hdf5@1.10.4%gcc@5.4.0~cxx~debug~fortran~hl+mpi+pic+shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
   [+]  3njc4q5      ^openmpi@3.1.3%gcc@5.4.0~cuda+cxx_exceptions fabrics= ~java~legacylaunchers~memchecker~pmi schedulers= ~sqlite3~thread_multiple+vt arch=linux-ubuntu16.04-x86_64
   [+]  43tkw5m          ^hwloc@1.11.9%gcc@5.4.0~cairo~cuda+libxml2+pci+shared arch=linux-ubuntu16.04-x86_64
   [+]  5urc6tc              ^libpciaccess@0.13.5%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  o2pfwjf                  ^libtool@2.4.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  suf5jtc                      ^m4@1.4.18%gcc@5.4.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=linux-ubuntu16.04-x86_64
   [+]  fypapcp                          ^libsigsegv@2.11%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  fovrh7a                  ^pkgconf@1.4.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  milz7fm                  ^util-macros@1.19.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  wpexsph              ^libxml2@2.9.8%gcc@5.4.0~python arch=linux-ubuntu16.04-x86_64
   [+]  teneqii                  ^xz@5.2.4%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  5nus6kn                  ^zlib@1.2.11%gcc@5.4.0+optimize+pic+shared arch=linux-ubuntu16.04-x86_64
   [+]  ft463od              ^numactl@2.0.11%gcc@5.4.0 patches=592f30f7f5f757dfc239ad0ffd39a9a048487ad803c26b419e0f96b8cda08c1a arch=linux-ubuntu16.04-x86_64
   [+]  3sx2gxe                  ^autoconf@2.69%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  ic2kyoa                      ^perl@5.26.2%gcc@5.4.0+cpanm patches=0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac +shared+threads arch=linux-ubuntu16.04-x86_64
   [+]  q4fpyuo                          ^gdbm@1.14.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  nxhwrg7                              ^readline@7.0%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  3o765ou                                  ^ncurses@6.1%gcc@5.4.0~symlinks~termlib arch=linux-ubuntu16.04-x86_64
   [+]  rymw7im                  ^automake@1.16.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   ==> Concretizing gmp
   [+]  qc4qcfz  gmp@6.1.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  3sx2gxe      ^autoconf@2.69%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  suf5jtc          ^m4@1.4.18%gcc@5.4.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=linux-ubuntu16.04-x86_64
   [+]  fypapcp              ^libsigsegv@2.11%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  ic2kyoa          ^perl@5.26.2%gcc@5.4.0+cpanm patches=0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac +shared+threads arch=linux-ubuntu16.04-x86_64
   [+]  q4fpyuo              ^gdbm@1.14.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  nxhwrg7                  ^readline@7.0%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  3o765ou                      ^ncurses@6.1%gcc@5.4.0~symlinks~termlib arch=linux-ubuntu16.04-x86_64
   [+]  fovrh7a                          ^pkgconf@1.4.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  rymw7im      ^automake@1.16.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  o2pfwjf      ^libtool@2.4.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   ==> Installing environment myproject
   ==> tcl is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/tcl-8.6.8-qhwyccywhx2i6s7ob2gvjrjtj3rnfuqt
   ==> trilinos is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1-rlsruavxqvwk2tgxzxboclbo6ykjf54r
   ==> hdf5 is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.4-ozyvmhzdew66byarohm4p36ep7wtcuiw
   ==> gmp is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gmp-6.1.2-qc4qcfz4monpllc3nqupdo7vwinf73sw

Spack will concretize the new roots, and install everything you added to
the environment.  Now we can see the installed roots in the output of
``spack find``:

.. code-block:: console

   $ spack find
   ==> In environment myproject
   ==> Root specs
   gmp  hdf5  tcl  trilinos

   ==> 24 installed packages
   -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
   boost@1.68.0  hdf5@1.10.4   libpciaccess@0.13.5  mumps@5.1.1             openblas@0.3.3      tcl@8.6.8
   bzip2@1.0.6   hdf5@1.10.4   libxml2@2.9.8        netcdf@4.6.1            openmpi@3.1.3       trilinos@12.12.1
   glm@0.9.7.1   hwloc@1.11.9  matio@1.5.9          netlib-scalapack@2.0.2  parmetis@4.0.3      xz@5.2.4
   gmp@6.1.2     hypre@2.15.1  metis@5.1.0          numactl@2.0.11          suite-sparse@5.3.0  zlib@1.2.11

We can build whole environments this way, by adding specs and installing
all at once, or we can install them with the usual ``install`` and
``uninstall`` portions.  The advantage to doing them all at once is that
we don't have to write a script outside of Spack to automate this, and we
can kick off a large build of many packages easily.

^^^^^^^^^^^^^^^^^^^^^
Configuration
^^^^^^^^^^^^^^^^^^^^^

So far, ``myproject`` does not have any special configuration associated
with it.  The specs concretize using Spack's defaults:

.. code-block:: console

   $ spack spec hypre
   Input spec
   --------------------------------
   hypre

   Concretized
   --------------------------------
   hypre@2.15.1%gcc@5.4.0~debug~int64+internal-superlu+mpi+shared arch=linux-ubuntu16.04-x86_64
       ^openblas@0.3.3%gcc@5.4.0 cpu_target= ~ilp64 patches=47cfa7a952ac7b2e4632c73ae199d69fb54490627b66a62c681e21019c4ddc9d,714aea33692304a50bd0ccde42590c176c82ded4a8ac7f06e573dc8071929c33 +pic+shared threads=none ~virtual_machine arch=linux-ubuntu16.04-x86_64
       ^openmpi@3.1.3%gcc@5.4.0~cuda+cxx_exceptions fabrics= ~java~legacylaunchers~memchecker~pmi schedulers= ~sqlite3~thread_multiple+vt arch=linux-ubuntu16.04-x86_64
           ^hwloc@1.11.9%gcc@5.4.0~cairo~cuda+libxml2+pci+shared arch=linux-ubuntu16.04-x86_64
               ^libpciaccess@0.13.5%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                   ^libtool@2.4.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                       ^m4@1.4.18%gcc@5.4.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=linux-ubuntu16.04-x86_64
                           ^libsigsegv@2.11%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                   ^pkgconf@1.4.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                   ^util-macros@1.19.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
               ^libxml2@2.9.8%gcc@5.4.0~python arch=linux-ubuntu16.04-x86_64
                   ^xz@5.2.4%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                   ^zlib@1.2.11%gcc@5.4.0+optimize+pic+shared arch=linux-ubuntu16.04-x86_64
               ^numactl@2.0.11%gcc@5.4.0 patches=592f30f7f5f757dfc239ad0ffd39a9a048487ad803c26b419e0f96b8cda08c1a arch=linux-ubuntu16.04-x86_64
                   ^autoconf@2.69%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                       ^perl@5.26.2%gcc@5.4.0+cpanm patches=0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac +shared+threads arch=linux-ubuntu16.04-x86_64
                           ^gdbm@1.14.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                               ^readline@7.0%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                                   ^ncurses@6.1%gcc@5.4.0~symlinks~termlib arch=linux-ubuntu16.04-x86_64
                   ^automake@1.16.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64

You may want to add extra configuration to your environment.  You can see
how your environment is configured using ``spack config get``:

.. code-block:: console

   $ spack config get
   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs: [tcl, trilinos, hdf5, gmp]

It turns out that this is a special configuration format where Spack
stores the state for the environment. Currently, the file is just a
``spack:`` header and a list of ``specs``.  These are the roots.

You can edit this file to add your own custom configuration.  Spack
provides a shortcut to do that:

.. code-block:: console

   spack config edit

You should now see the same file, and edit it to look like this:

.. code-block:: yaml

   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     packages:
       all:
         providers:
           mpi: [mpich]

     # add package specs to the `specs` list
     specs: [tcl, trilinos, hdf5, gmp]

Now if we run ``spack spec`` again in the environment, specs will concretize with ``mpich`` as the MPI implementation:

.. code-block:: console

   $ spack spec hypre
   Input spec
   --------------------------------
   hypre

   Concretized
   --------------------------------
   hypre@2.15.1%gcc@5.4.0~debug~int64+internal-superlu+mpi+shared arch=linux-ubuntu16.04-x86_64
       ^mpich@3.2.1%gcc@5.4.0 device=ch3 +hydra netmod=tcp +pmi+romio~verbs arch=linux-ubuntu16.04-x86_64
           ^findutils@4.6.0%gcc@5.4.0 patches=84b916c0bf8c51b7e7b28417692f0ad3e7030d1f3c248ba77c42ede5c1c5d11e,bd9e4e5cc280f9753ae14956c4e4aa17fe7a210f55dd6c84aa60b12d106d47a2 arch=linux-ubuntu16.04-x86_64
               ^autoconf@2.69%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                   ^m4@1.4.18%gcc@5.4.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=linux-ubuntu16.04-x86_64
                       ^libsigsegv@2.11%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                   ^perl@5.26.2%gcc@5.4.0+cpanm patches=0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac +shared+threads arch=linux-ubuntu16.04-x86_64
                       ^gdbm@1.14.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                           ^readline@7.0%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
                               ^ncurses@6.1%gcc@5.4.0~symlinks~termlib arch=linux-ubuntu16.04-x86_64
                                   ^pkgconf@1.4.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
               ^automake@1.16.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
               ^libtool@2.4.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
               ^texinfo@6.5%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
       ^openblas@0.3.3%gcc@5.4.0 cpu_target= ~ilp64 patches=47cfa7a952ac7b2e4632c73ae199d69fb54490627b66a62c681e21019c4ddc9d,714aea33692304a50bd0ccde42590c176c82ded4a8ac7f06e573dc8071929c33 +pic+shared threads=none ~virtual_machine arch=linux-ubuntu16.04-x86_64

In addition to the ``specs`` section, an environment's configuration can
contain any of the configuration options from Spack's various config
sections. You can add custom repositories, a custom install location,
custom compilers, or custom external packages, in addition to the ``package``
preferences we show here.

But now we have a problem.  We already installed part of this environment
with openmpi, but now we want to install it with ``mpich``.

You can run ``spack concretize`` inside of an environment to concretize
all of its specs.  We can run it here:

.. code-block:: console

   $ spack concretize -f
   ==> Concretizing tcl
   [+]  qhwyccy  tcl@8.6.8%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  5nus6kn      ^zlib@1.2.11%gcc@5.4.0+optimize+pic+shared arch=linux-ubuntu16.04-x86_64
   ==> Concretizing trilinos
   [+]  kqc52mo  trilinos@12.12.1%gcc@5.4.0~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2 arch=linux-ubuntu16.04-x86_64
   [+]  zbgfxap      ^boost@1.68.0%gcc@5.4.0+atomic+chrono~clanglibcpp cxxstd=default +date_time~debug+exception+filesystem+graph~icu+iostreams+locale+log+math~mpi+multithreaded~numpy patches=2ab6c72d03dec6a4ae20220a9dfd5c8c572c5294252155b85c6874d97c323199 +program_options~python+random+regex+serialization+shared+signals~singlethreaded+system~taggedlayout+test+thread+timer~versionedlayout+wave arch=linux-ubuntu16.04-x86_64
   [+]  ufczdvs          ^bzip2@1.0.6%gcc@5.4.0+shared arch=linux-ubuntu16.04-x86_64
   [+]  2rhuivg              ^diffutils@3.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  5nus6kn          ^zlib@1.2.11%gcc@5.4.0+optimize+pic+shared arch=linux-ubuntu16.04-x86_64
   [+]  otafqzh      ^cmake@3.12.3%gcc@5.4.0~doc+ncurses+openssl+ownlibs patches=dd3a40d4d92f6b2158b87d6fb354c277947c776424aa03f6dc8096cf3135f5d0 ~qt arch=linux-ubuntu16.04-x86_64
   [+]  3o765ou          ^ncurses@6.1%gcc@5.4.0~symlinks~termlib arch=linux-ubuntu16.04-x86_64
   [+]  fovrh7a              ^pkgconf@1.4.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  b4y3w3b          ^openssl@1.0.2o%gcc@5.4.0+systemcerts arch=linux-ubuntu16.04-x86_64
   [+]  ic2kyoa              ^perl@5.26.2%gcc@5.4.0+cpanm patches=0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac +shared+threads arch=linux-ubuntu16.04-x86_64
   [+]  q4fpyuo                  ^gdbm@1.14.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  nxhwrg7                      ^readline@7.0%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  jnw622j      ^glm@0.9.7.1%gcc@5.4.0 build_type=RelWithDebInfo arch=linux-ubuntu16.04-x86_64
   [+]  xxd7syh      ^hdf5@1.10.4%gcc@5.4.0~cxx~debug~fortran+hl+mpi+pic+shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
   [+]  p3f7p2r          ^mpich@3.2.1%gcc@5.4.0 device=ch3 +hydra netmod=tcp +pmi+romio~verbs arch=linux-ubuntu16.04-x86_64
   [+]  d4iajxs              ^findutils@4.6.0%gcc@5.4.0 patches=84b916c0bf8c51b7e7b28417692f0ad3e7030d1f3c248ba77c42ede5c1c5d11e,bd9e4e5cc280f9753ae14956c4e4aa17fe7a210f55dd6c84aa60b12d106d47a2 arch=linux-ubuntu16.04-x86_64
   [+]  3sx2gxe                  ^autoconf@2.69%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  suf5jtc                      ^m4@1.4.18%gcc@5.4.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=linux-ubuntu16.04-x86_64
   [+]  fypapcp                          ^libsigsegv@2.11%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  rymw7im                  ^automake@1.16.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  o2pfwjf                  ^libtool@2.4.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  zs7a2pc                  ^texinfo@6.5%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  obewuoz      ^hypre@2.15.1%gcc@5.4.0~debug~int64~internal-superlu+mpi+shared arch=linux-ubuntu16.04-x86_64
   [+]  cyeg2yi          ^openblas@0.3.3%gcc@5.4.0 cpu_target= ~ilp64 patches=47cfa7a952ac7b2e4632c73ae199d69fb54490627b66a62c681e21019c4ddc9d,714aea33692304a50bd0ccde42590c176c82ded4a8ac7f06e573dc8071929c33 +pic+shared threads=none ~virtual_machine arch=linux-ubuntu16.04-x86_64
   [+]  gvyqldh      ^matio@1.5.9%gcc@5.4.0+hdf5+shared+zlib arch=linux-ubuntu16.04-x86_64
   [+]  3wnvp4j      ^metis@5.1.0%gcc@5.4.0 build_type=Release ~gdb~int64 patches=4991da938c1d3a1d3dea78e49bbebecba00273f98df2a656e38b83d55b281da1 ~real64+shared arch=linux-ubuntu16.04-x86_64
   [+]  cumcj5a      ^mumps@5.1.1%gcc@5.4.0+complex+double+float~int64~metis+mpi~parmetis~ptscotch~scotch+shared arch=linux-ubuntu16.04-x86_64
   [+]  p7iln2p          ^netlib-scalapack@2.0.2%gcc@5.4.0 build_type=RelWithDebInfo ~pic+shared arch=linux-ubuntu16.04-x86_64
   [+]  wmmx5sg      ^netcdf@4.6.1%gcc@5.4.0~dap~hdf4 maxdims=1024 maxvars=8192 +mpi~parallel-netcdf+shared arch=linux-ubuntu16.04-x86_64
   [+]  jehtata      ^parmetis@4.0.3%gcc@5.4.0 build_type=RelWithDebInfo ~gdb patches=4f892531eb0a807eb1b82e683a416d3e35154a455274cf9b162fb02054d11a5b,50ed2081bc939269689789942067c58b3e522c269269a430d5d34c00edbc5870,704b84f7c7444d4372cb59cca6e1209df4ef3b033bc4ee3cf50f369bce972a9d +shared arch=linux-ubuntu16.04-x86_64
   [+]  zaau4ki      ^suite-sparse@5.3.0%gcc@5.4.0~cuda~openmp+pic~tbb arch=linux-ubuntu16.04-x86_64
   ==> Concretizing hdf5
    -   zjgyn3w  hdf5@1.10.4%gcc@5.4.0~cxx~debug~fortran~hl+mpi+pic+shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
   [+]  p3f7p2r      ^mpich@3.2.1%gcc@5.4.0 device=ch3 +hydra netmod=tcp +pmi+romio~verbs arch=linux-ubuntu16.04-x86_64
   [+]  d4iajxs          ^findutils@4.6.0%gcc@5.4.0 patches=84b916c0bf8c51b7e7b28417692f0ad3e7030d1f3c248ba77c42ede5c1c5d11e,bd9e4e5cc280f9753ae14956c4e4aa17fe7a210f55dd6c84aa60b12d106d47a2 arch=linux-ubuntu16.04-x86_64
   [+]  3sx2gxe              ^autoconf@2.69%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  suf5jtc                  ^m4@1.4.18%gcc@5.4.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=linux-ubuntu16.04-x86_64
   [+]  fypapcp                      ^libsigsegv@2.11%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  ic2kyoa                  ^perl@5.26.2%gcc@5.4.0+cpanm patches=0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac +shared+threads arch=linux-ubuntu16.04-x86_64
   [+]  q4fpyuo                      ^gdbm@1.14.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  nxhwrg7                          ^readline@7.0%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  3o765ou                              ^ncurses@6.1%gcc@5.4.0~symlinks~termlib arch=linux-ubuntu16.04-x86_64
   [+]  fovrh7a                                  ^pkgconf@1.4.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  rymw7im              ^automake@1.16.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  o2pfwjf              ^libtool@2.4.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  zs7a2pc              ^texinfo@6.5%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  5nus6kn      ^zlib@1.2.11%gcc@5.4.0+optimize+pic+shared arch=linux-ubuntu16.04-x86_64
   ==> Concretizing gmp
   [+]  qc4qcfz  gmp@6.1.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  3sx2gxe      ^autoconf@2.69%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  suf5jtc          ^m4@1.4.18%gcc@5.4.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=linux-ubuntu16.04-x86_64
   [+]  fypapcp              ^libsigsegv@2.11%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  ic2kyoa          ^perl@5.26.2%gcc@5.4.0+cpanm patches=0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac +shared+threads arch=linux-ubuntu16.04-x86_64
   [+]  q4fpyuo              ^gdbm@1.14.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  nxhwrg7                  ^readline@7.0%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  3o765ou                      ^ncurses@6.1%gcc@5.4.0~symlinks~termlib arch=linux-ubuntu16.04-x86_64
   [+]  fovrh7a                          ^pkgconf@1.4.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  rymw7im      ^automake@1.16.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  o2pfwjf      ^libtool@2.4.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64

Now, all the specs in the environment are concrete and ready to be
installed with ``mpich`` as the MPI implementation.

Normally, we could just run ``spack config edit``, edit the environment
configuration, ``spack add`` some specs, and ``spack install``.

But, when we already have installed packages in the environment, we have
to force everything in the environment to be re-concretized using ``spack
concretize -f``.  *Then* we can re-run ``spack install``.


-----------------------------------
``spack.yaml`` and ``spack.lock``
-----------------------------------

So far we've shown you how to interact with environments from the command
line, but they also have a file-based interface that can be used by
developers and admins to manage workflows for projects.

In this section we'll dive a little deeper to see how environments are
implemented, and how you could use this in your day-to-day development.

^^^^^^^^^^^^^^
``spack.yaml``
^^^^^^^^^^^^^^

Earlier, we changed an environment's configuration using ``spack config
edit``.  We were actually editing a special file called ``spack.yaml``.
Let's take a look.

We can get directly to the current environment's location using ``spack cd``:

.. code-block:: console

   $ spack cd -e myproject
   $ pwd
   ~/spack/var/spack/environments/myproject
   $ ls
   spack.lock  spack.yaml

We notice two things here.  First, the environment is just a directory
inside of ``var/spack/environments`` within the Spack installation.
Second, it contains two important files: ``spack.yaml`` and
``spack.lock``.

``spack.yaml`` is the configuration file for environments that we've
already seen, but it does not *have* to live inside Spack.  If you create
an environment using ``spack env create``, it is *managed* by
Spack in the ``var/spack/environments`` directory, and you can refer to
it by name.

You can actually put a ``spack.yaml`` file *anywhere*, and you can use it
to bundle an environment, or a list of dependencies to install, with your
project.  Let's make a simple project:

.. code-block:: console

   $ cd
   $ mkdir code
   $ cd code
   $ spack env create -d .
   ==> Created environment in ~/code

Here, we made a new directory called *code*, and we used the ``-d``
option to create an environment in it.

What really happened?

.. code-block:: console

   $ ls
   spack.yaml
   $ cat spack.yaml
   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs: []

Spack just created a ``spack.yaml`` file in the code directory, with an
empty list of root specs.  Now we have a Spack environment, *in a
directory*, that we can use to manage dependencies.  Suppose your project
depends on ``boost``, ``trilinos``, and ``openmpi``.  You can add these
to your spec list:

.. code-block:: yaml

   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs:
     - boost
     - trilinos
     - openmpi

And now *anyone* who uses the *code* repository can use this format to
install the project's dependencies.  They need only clone the repository,
``cd`` into it, and type ``spack install``:

.. code-block:: console

   $ spack install
   ==> Concretizing boost
   [+]  zbgfxap  boost@1.68.0%gcc@5.4.0+atomic+chrono~clanglibcpp cxxstd=default +date_time~debug+exception+filesystem+graph~icu+iostreams+locale+log+math~mpi+multithreaded~numpy patches=2ab6c72d03dec6a4ae20220a9dfd5c8c572c5294252155b85c6874d97c323199 +program_options~python+random+regex+serialization+shared+signals~singlethreaded+system~taggedlayout+test+thread+timer~versionedlayout+wave arch=linux-ubuntu16.04-x86_64
   [+]  ufczdvs      ^bzip2@1.0.6%gcc@5.4.0+shared arch=linux-ubuntu16.04-x86_64
   [+]  2rhuivg          ^diffutils@3.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  5nus6kn      ^zlib@1.2.11%gcc@5.4.0+optimize+pic+shared arch=linux-ubuntu16.04-x86_64
   ==> Concretizing trilinos
   [+]  rlsruav  trilinos@12.12.1%gcc@5.4.0~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2 arch=linux-ubuntu16.04-x86_64
   [+]  zbgfxap      ^boost@1.68.0%gcc@5.4.0+atomic+chrono~clanglibcpp cxxstd=default +date_time~debug+exception+filesystem+graph~icu+iostreams+locale+log+math~mpi+multithreaded~numpy patches=2ab6c72d03dec6a4ae20220a9dfd5c8c572c5294252155b85c6874d97c323199 +program_options~python+random+regex+serialization+shared+signals~singlethreaded+system~taggedlayout+test+thread+timer~versionedlayout+wave arch=linux-ubuntu16.04-x86_64
   [+]  ufczdvs          ^bzip2@1.0.6%gcc@5.4.0+shared arch=linux-ubuntu16.04-x86_64
   [+]  2rhuivg              ^diffutils@3.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  5nus6kn          ^zlib@1.2.11%gcc@5.4.0+optimize+pic+shared arch=linux-ubuntu16.04-x86_64
   [+]  otafqzh      ^cmake@3.12.3%gcc@5.4.0~doc+ncurses+openssl+ownlibs patches=dd3a40d4d92f6b2158b87d6fb354c277947c776424aa03f6dc8096cf3135f5d0 ~qt arch=linux-ubuntu16.04-x86_64
   [+]  3o765ou          ^ncurses@6.1%gcc@5.4.0~symlinks~termlib arch=linux-ubuntu16.04-x86_64
   [+]  fovrh7a              ^pkgconf@1.4.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  b4y3w3b          ^openssl@1.0.2o%gcc@5.4.0+systemcerts arch=linux-ubuntu16.04-x86_64
   [+]  ic2kyoa              ^perl@5.26.2%gcc@5.4.0+cpanm patches=0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac +shared+threads arch=linux-ubuntu16.04-x86_64
   [+]  q4fpyuo                  ^gdbm@1.14.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  nxhwrg7                      ^readline@7.0%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  jnw622j      ^glm@0.9.7.1%gcc@5.4.0 build_type=RelWithDebInfo arch=linux-ubuntu16.04-x86_64
   [+]  oqwnui7      ^hdf5@1.10.4%gcc@5.4.0~cxx~debug~fortran+hl+mpi+pic+shared~szip~threadsafe arch=linux-ubuntu16.04-x86_64
   [+]  3njc4q5          ^openmpi@3.1.3%gcc@5.4.0~cuda+cxx_exceptions fabrics= ~java~legacylaunchers~memchecker~pmi schedulers= ~sqlite3~thread_multiple+vt arch=linux-ubuntu16.04-x86_64
   [+]  43tkw5m              ^hwloc@1.11.9%gcc@5.4.0~cairo~cuda+libxml2+pci+shared arch=linux-ubuntu16.04-x86_64
   [+]  5urc6tc                  ^libpciaccess@0.13.5%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  o2pfwjf                      ^libtool@2.4.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  suf5jtc                          ^m4@1.4.18%gcc@5.4.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=linux-ubuntu16.04-x86_64
   [+]  fypapcp                              ^libsigsegv@2.11%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  milz7fm                      ^util-macros@1.19.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  wpexsph                  ^libxml2@2.9.8%gcc@5.4.0~python arch=linux-ubuntu16.04-x86_64
   [+]  teneqii                      ^xz@5.2.4%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  ft463od                  ^numactl@2.0.11%gcc@5.4.0 patches=592f30f7f5f757dfc239ad0ffd39a9a048487ad803c26b419e0f96b8cda08c1a arch=linux-ubuntu16.04-x86_64
   [+]  3sx2gxe                      ^autoconf@2.69%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  rymw7im                      ^automake@1.16.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  fshksdp      ^hypre@2.15.1%gcc@5.4.0~debug~int64~internal-superlu+mpi+shared arch=linux-ubuntu16.04-x86_64
   [+]  cyeg2yi          ^openblas@0.3.3%gcc@5.4.0 cpu_target= ~ilp64 patches=47cfa7a952ac7b2e4632c73ae199d69fb54490627b66a62c681e21019c4ddc9d,714aea33692304a50bd0ccde42590c176c82ded4a8ac7f06e573dc8071929c33 +pic+shared threads=none ~virtual_machine arch=linux-ubuntu16.04-x86_64
   [+]  lmzdgss      ^matio@1.5.9%gcc@5.4.0+hdf5+shared+zlib arch=linux-ubuntu16.04-x86_64
   [+]  3wnvp4j      ^metis@5.1.0%gcc@5.4.0 build_type=Release ~gdb~int64 patches=4991da938c1d3a1d3dea78e49bbebecba00273f98df2a656e38b83d55b281da1 ~real64+shared arch=linux-ubuntu16.04-x86_64
   [+]  acsg2dz      ^mumps@5.1.1%gcc@5.4.0+complex+double+float~int64~metis+mpi~parmetis~ptscotch~scotch+shared arch=linux-ubuntu16.04-x86_64
   [+]  wotpfwf          ^netlib-scalapack@2.0.2%gcc@5.4.0 build_type=RelWithDebInfo ~pic+shared arch=linux-ubuntu16.04-x86_64
   [+]  mhm4izp      ^netcdf@4.6.1%gcc@5.4.0~dap~hdf4 maxdims=1024 maxvars=8192 +mpi~parallel-netcdf+shared arch=linux-ubuntu16.04-x86_64
   [+]  uv6h3sq      ^parmetis@4.0.3%gcc@5.4.0 build_type=RelWithDebInfo ~gdb patches=4f892531eb0a807eb1b82e683a416d3e35154a455274cf9b162fb02054d11a5b,50ed2081bc939269689789942067c58b3e522c269269a430d5d34c00edbc5870,704b84f7c7444d4372cb59cca6e1209df4ef3b033bc4ee3cf50f369bce972a9d +shared arch=linux-ubuntu16.04-x86_64
   [+]  zaau4ki      ^suite-sparse@5.3.0%gcc@5.4.0~cuda~openmp+pic~tbb arch=linux-ubuntu16.04-x86_64
   ==> Concretizing openmpi
   [+]  3njc4q5  openmpi@3.1.3%gcc@5.4.0~cuda+cxx_exceptions fabrics= ~java~legacylaunchers~memchecker~pmi schedulers= ~sqlite3~thread_multiple+vt arch=linux-ubuntu16.04-x86_64
   [+]  43tkw5m      ^hwloc@1.11.9%gcc@5.4.0~cairo~cuda+libxml2+pci+shared arch=linux-ubuntu16.04-x86_64
   [+]  5urc6tc          ^libpciaccess@0.13.5%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  o2pfwjf              ^libtool@2.4.6%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  suf5jtc                  ^m4@1.4.18%gcc@5.4.0 patches=3877ab548f88597ab2327a2230ee048d2d07ace1062efe81fc92e91b7f39cd00,c0a408fbffb7255fcc75e26bd8edab116fc81d216bfd18b473668b7739a4158e,fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8 +sigsegv arch=linux-ubuntu16.04-x86_64
   [+]  fypapcp                      ^libsigsegv@2.11%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  fovrh7a              ^pkgconf@1.4.2%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  milz7fm              ^util-macros@1.19.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  wpexsph          ^libxml2@2.9.8%gcc@5.4.0~python arch=linux-ubuntu16.04-x86_64
   [+]  teneqii              ^xz@5.2.4%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  5nus6kn              ^zlib@1.2.11%gcc@5.4.0+optimize+pic+shared arch=linux-ubuntu16.04-x86_64
   [+]  ft463od          ^numactl@2.0.11%gcc@5.4.0 patches=592f30f7f5f757dfc239ad0ffd39a9a048487ad803c26b419e0f96b8cda08c1a arch=linux-ubuntu16.04-x86_64
   [+]  3sx2gxe              ^autoconf@2.69%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  ic2kyoa                  ^perl@5.26.2%gcc@5.4.0+cpanm patches=0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac +shared+threads arch=linux-ubuntu16.04-x86_64
   [+]  q4fpyuo                      ^gdbm@1.14.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  nxhwrg7                          ^readline@7.0%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   [+]  3o765ou                              ^ncurses@6.1%gcc@5.4.0~symlinks~termlib arch=linux-ubuntu16.04-x86_64
   [+]  rymw7im              ^automake@1.16.1%gcc@5.4.0 arch=linux-ubuntu16.04-x86_64
   ==> Installing environment ~/code
   ==> boost is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/boost-1.68.0-zbgfxapchxa4awxdwpleubfuznblxzvt
   ==> trilinos is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1-rlsruavxqvwk2tgxzxboclbo6ykjf54r
   ==> openmpi is already installed in ~/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openmpi-3.1.3-3njc4q5pqdpptq6jvqjrezkffwokv2sx


Spack concretizes the specs in the ``spack.yaml`` file and installs them.

What happened here?  If you ``cd`` into a directory that has a
``spack.yaml`` file in it, Spack considers this directory's environment
to be activated.  The directory does not have to live within Spack; it
can be anywhere.

So, from ``~/code``, we can actually manipulate ``spack.yaml`` using
``spack add`` and ``spack remove`` (just like managed environments):

.. code-block:: console

   $ spack add hdf5@5.5.1
   ==> Adding hdf5 to environment ~/code
   $ cat spack.yaml
   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs:
     - boost
     - trilinos
     - openmpi
     - hdf5@5.5.1

   $ spack remove hdf5
   ==> Removing hdf5 from environment ~/code
   $ cat spack.yaml
   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs:
     - boost
     - trilinos
     - openmpi


^^^^^^^^^^^^^^
``spack.lock``
^^^^^^^^^^^^^^

Okay, we've covered managed environments, environments in directories, and
the last thing we'll cover is ``spack.lock``. You may remember that when
we ran ``spack install``, Spack concretized all the specs in the
``spack.yaml`` file and installed them.

Whenever we concretize Specs in an environment, all concrete specs in the
environment are written out to a ``spack.lock`` file *alongside*
``spack.yaml``.  The ``spack.lock`` file is not really human-readable
like the ``spack.yaml`` file.  It is a ``json`` format that contains all
the information that we need to *reproduce* the build of an
environment:

.. code-block:: console

   $ head spack.lock
   {
     "concrete_specs": {
      "teneqii2xv5u6zl5r6qi3pwurc6pmypz": {
       "xz": {
         "version": "5.2.4",
         "arch": {
           "platform": "linux",
           "platform_os": "ubuntu16.04",
         "target": "x86_64"
    },
    ...

``spack.yaml`` and ``spack.lock`` correspond to two fundamental concepts
in Spack, but for environments:

  * ``spack.yaml`` is the set of *abstract* specs and configuration that
    you want to install.
  * ``spack.lock`` is the set of all fully *concretized* specs generated
    from concretizing ``spack.yaml``

Using either of these, you can recreate an environment that someone else
built.  ``spack env create`` takes an extra optional argument, which can
be either a ``spack.yaml`` or a ``spack.lock`` file:

.. code-block:: console

   $ spack env create my-project spack.yaml

   $ spack env create my-project spack.lock

Both of these create a new environment called ``my-project``, but which
one you choose to use depends on your needs:

#. copying the yaml file allows someone else to build your *requirements*,
   potentially a different way.

#. copying the lock file allows someone else to rebuild your
   *installation* exactly as you built it.

The first use case can *re-concretize* the same specs on new platforms in
order to build, but it will preserve the abstract requirements.  The
second use case (currently) requires you to be on the same machine, but
it retains all decisions made during concretization and is faithful to a
prior install.
