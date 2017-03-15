.. _basics-tutorial:

=========================================
Basic Installation Tutorial
=========================================

This tutorial will guide you through the process of installing software
using Spack. We will first cover the `spack install` command, focusing on
the power of the spec syntax and the flexibility it gives to users. We
will also cover the `spack find` command for viewing installed packages
and the `spack uninstall` command. Finally, we will touch on how Spack
manages compilers, especially as it relates to using Spack-built
compilers within Spack. We will include full output from all of the
commands demonstrated, although we will frequently call attention to only
small portions of that output (or merely to the fact that it
succeeded). The provided output is all from a cluster running Red Hat
Enterprise Linux.

.. _basics-tutorial-install:

----------------
Installing Spack
----------------

Spack works out of the box. Simply clone spack and get going.

.. code-block:: console

  $ git clone https://github.com/LLNL/spack.git
  Initialized empty Git repository in ~/spack/.git/
  remote: Counting objects: 47125, done.
  remote: Compressing objects: 100% (68/68), done.
  remote: Total 47125 (delta 16), reused 2 (delta 2), pack-reused 47047
  Receiving objects: 100% (47125/47125), 12.02 MiB | 2.11 MiB/s, done.
  Resolving deltas: 100% (23044/23044), done.
  $ cd spack

Then add Spack to your path.

.. code-block:: console

  $ export PATH=~/spack/bin:$PATH

You're good to go!

-----------------
What is in Spack?
-----------------

The ``spack list`` command shows available packages.

.. code-block:: console

  $ spack list
  ==> 1016 packages.
  abinit                           hwloc                  piranha              r-rjava
  ack                              hydra                  pixman               r-rjson
  activeharmony                    hypre                  pkg-config           r-rjsonio
  ...

The ``spack list`` command can also take a query string. Spack
automatically adds wildcards to both ends of the string. For example,
we can view all available python packages.

.. code-block:: console

  $ spack list py
  ==> 129 packages.
  py-3to2            py-epydoc          py-nestle         py-pycparser         py-six
  py-alabaster       py-flake8          py-netcdf         py-pydatalog         py-sncosmo
  py-argcomplete     py-funcsigs        py-networkx       py-pyelftools        py-snowballstemmer
  ...

-------------------
Installing Packages
-------------------

Installing a package with Spack is very simple. To install a piece of
software, simply type ``spack install <package_name>``

.. code-block:: console

  $ spack install libelf
  ==> Installing libelf
  ==> Trying to fetch from ~/spack/var/spack/cache/libelf/libelf-0.8.13.tar.gz
  curl: (37) Couldn't open file ~/spack/var/spack/cache/libelf/libelf-0.8.13.tar.gz
  ==> Fetching from ~/spack/var/spack/cache/libelf/libelf-0.8.13.tar.gz failed.
  ==> Trying to fetch from http://www.mr511.de/software/libelf-0.8.13.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: ~/spack/var/spack/stage/libelf-0.8.13-csrt4qxfkhjgn5xg3zjpkir7xdnszl2a/libelf-0.8.13.tar.gz
  ==> Created stage in ~/spack/var/spack/stage/libelf-0.8.13-csrt4qxfkhjgn5xg3zjpkir7xdnszl2a
  ==> No patches needed for libelf
  ==> Building libelf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
    Fetch: 1.21s.  Build: 8.42s.  Total: 9.62s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libelf-0.8.13-csrt4qxfkhjgn5xg3zjpkir7xdnszl2a


Spack's spec syntax is the interface by which we can request specific
configurations of the package. The ``%`` sigil is used to specify
compilers.

.. code-block:: console

  $ spack install libelf %intel
  ==> Installing libelf
  ==> Trying to fetch from ~/spack/var/spack/cache/libelf/libelf-0.8.13.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: ~/spack/var/spack/stage/libelf-0.8.13-7wgp32xksatkvw2tbssmehw2t5tnxndj/libelf-0.8.13.tar.gz
  ==> Created stage in ~/spack/var/spack/stage/libelf-0.8.13-7wgp32xksatkvw2tbssmehw2t5tnxndj
  ==> No patches needed for libelf
  ==> Building libelf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
    Fetch: 0.09s.  Build: 50.64s.  Total: 50.72s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/intel-16.0.3/libelf-0.8.13-7wgp32xksatkvw2tbssmehw2t5tnxndj

Note that this installation is located separately from the previous
one. We will discuss this in more detail later, but this is part of what
allows Spack to support arbitrarily versioned software.

You can check for particular versions before requesting them. We will
use the ``spack versions`` command to see the available versions, and then
install a different version of ``libelf``.

.. code-block:: console

  $ spack versions libelf
  ==> Safe versions (already checksummed):
    0.8.13
    0.8.12
  ==> Remote versions (not yet checksummed):
    0.8.11
    0.8.10
    0.8.9
    0.8.8
    0.8.7
    0.8.6
    0.8.5
    0.8.4
    0.8.3
    0.8.2
    0.8.0
    0.7.0
    0.6.4
    0.5.2


The ``@`` sigil is used to specify versions, both of packages and of
compilers.

.. code-block:: console

  $ spack install libelf @0.8.12
  ==> Installing libelf
  ==> Trying to fetch from ~/spack/var/spack/cache/libelf/libelf-0.8.12.tar.gz
  curl: (37) Couldn't open file ~/spack/var/spack/cache/libelf/libelf-0.8.12.tar.gz
  ==> Fetching from ~/spack/var/spack/cache/libelf/libelf-0.8.12.tar.gz failed.
  ==> Trying to fetch from http://www.mr511.de/software/libelf-0.8.12.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: ~/spack/var/spack/stage/libelf-0.8.12-ipggckv6i7h44iryzfa4dwdela32a7fy/libelf-0.8.12.tar.gz
  ==> Created stage in ~/spack/var/spack/stage/libelf-0.8.12-ipggckv6i7h44iryzfa4dwdela32a7fy
  ==> No patches needed for libelf
  ==> Building libelf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
    Fetch: 1.12s.  Build: 7.88s.  Total: 9.00s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libelf-0.8.12-ipggckv6i7h44iryzfa4dwdela32a7fy



  $ spack install libelf %intel@15.0.4
  ==> Installing libelf
  ==> Trying to fetch from ~/spack/var/spack/cache/libelf/libelf-0.8.13.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: ~/spack/var/spack/stage/libelf-0.8.13-w33hrejdyqu2j2gggdswitls2zv6kdsi/libelf-0.8.13.tar.gz
  ==> Created stage in ~/spack/var/spack/stage/libelf-0.8.13-w33hrejdyqu2j2gggdswitls2zv6kdsi
  ==> No patches needed for libelf
  ==> Building libelf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
    Fetch: 0.09s.  Build: 55.51s.  Total: 55.60s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/intel-15.0.4/libelf-0.8.13-w33hrejdyqu2j2gggdswitls2zv6kdsi


The spec syntax also includes compiler flags. Spack accepts
``cppflags``, ``cflags``, ``cxxflags``, ``fflags``, ``ldflags``, and
``ldlibs`` parameters.  The values of these fields must be quoted on
the command line if they include spaces. These values are injected
into the compile line automatically by the Spack compiler wrappers.

.. code-block:: console

  $ spack install libelf @0.8.12 cppflags="-O3"
  ==> Installing libelf
  ==> Trying to fetch from ~/spack/var/spack/cache/libelf/libelf-0.8.12.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: ~/spack/var/spack/stage/libelf-0.8.12-vrv2ttbd34xlfoxy4jwt6qsjrcbalmmw/libelf-0.8.12.tar.gz
  ==> Created stage in ~/spack/var/spack/stage/libelf-0.8.12-vrv2ttbd34xlfoxy4jwt6qsjrcbalmmw
  ==> No patches needed for libelf
  ==> Building libelf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
    Fetch: 0.04s.  Build: 7.95s.  Total: 7.99s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libelf-0.8.12-vrv2ttbd34xlfoxy4jwt6qsjrcbalmmw


The ``spack find`` command is used to query installed packages. Note that
some packages appear identical with the default output. The ``-l`` flag
shows the hash of each package, and the ``-f`` flag shows any non-empty
compiler flags of those packages.

.. code-block:: console

  $ spack find
  ==> 5 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
  libelf@0.8.12
  libelf@0.8.12
  libelf@0.8.13

  -- linux-redhat6-x86_64 / intel@15.0.4 --------------------------
  libelf@0.8.13

  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
  libelf@0.8.13



  $ spack find -lf
  ==> 5 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
  ipggckv libelf@0.8.12%gcc

  vrv2ttb libelf@0.8.12%gcc cppflags="-O3"

  csrt4qx libelf@0.8.13%gcc


  -- linux-redhat6-x86_64 / intel@15.0.4 --------------------------
  w33hrej libelf@0.8.13%intel


  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
  7wgp32x libelf@0.8.13%intel


Spack generates a hash for each spec. This hash is a function of the full
provenance of the package, so any change to the spec affects the
hash. Spack uses this value to compare specs and to generate unique
installation directories for every combinatorial version. As we move into
more complicated packages with software dependencies, we can see that
Spack reuses existing packages to satisfy a dependency only when the
existing package's hash matches the desired spec.

.. code-block:: console

  $ spack install libdwarf
  ==> Installing libdwarf
  ==> libelf is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libelf-0.8.13-csrt4qxfkhjgn5xg3zjpkir7xdnszl2a
  ==> Can not find version 20160507 in url_list
  ==> Trying to fetch from ~/spack/var/spack/cache/libdwarf/libdwarf-20160507.tar.gz
  curl: (37) Couldn't open file ~/spack/var/spack/cache/libdwarf/libdwarf-20160507.tar.gz
  ==> Fetching from ~/spack/var/spack/cache/libdwarf/libdwarf-20160507.tar.gz failed.
  ==> Trying to fetch from http://www.prevanders.net/libdwarf-20160507.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: ~/spack/var/spack/stage/libdwarf-20160507-yfx6p3g3rkmqvcqbmtb34o6pln7pqvcz/libdwarf-20160507.tar.gz
  ==> Created stage in ~/spack/var/spack/stage/libdwarf-20160507-yfx6p3g3rkmqvcqbmtb34o6pln7pqvcz
  ==> No patches needed for libdwarf
  ==> Building libdwarf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libdwarf
    Fetch: 1.56s.  Build: 33.59s.  Total: 35.15s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libdwarf-20160507-yfx6p3g3rkmqvcqbmtb34o6pln7pqvcz


Dependencies can be explicitly requested using the ``^`` sigil. Note that
the spec syntax is recursive. Anything we could specify about the
top-level package, we can also specify about a dependency using ``^``.

.. code-block:: console

  $ spack install libdwarf ^libelf @0.8.12 %intel
  ==> Installing libdwarf
  ==> Installing libelf
  ==> Trying to fetch from ~/spack/var/spack/cache/libelf/libelf-0.8.12.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: ~/spack/var/spack/stage/libelf-0.8.12-4blbe3qxqct3ymrfoxxnxysmybvbxay7/libelf-0.8.12.tar.gz
  ==> Created stage in ~/spack/var/spack/stage/libelf-0.8.12-4blbe3qxqct3ymrfoxxnxysmybvbxay7
  ==> No patches needed for libelf
  ==> Building libelf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libelf
    Fetch: 0.04s.  Build: 52.16s.  Total: 52.19s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/intel-16.0.3/libelf-0.8.12-4blbe3qxqct3ymrfoxxnxysmybvbxay7
  ==> Can not find version 20160507 in url_list
  ==> Trying to fetch from ~/spack/var/spack/cache/libdwarf/libdwarf-20160507.tar.gz
  ################################################################################################################################################################################# 100.0%
  ==> Staging archive: ~/spack/var/spack/stage/libdwarf-20160507-csruprgucaujkfkrcywhwou7nbeis5fo/libdwarf-20160507.tar.gz
  ==> Created stage in ~/spack/var/spack/stage/libdwarf-20160507-csruprgucaujkfkrcywhwou7nbeis5fo
  ==> No patches needed for libdwarf
  ==> Building libdwarf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libdwarf
    Fetch: 0.40s.  Build: 2m 17.29s.  Total: 2m 17.69s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/intel-16.0.3/libdwarf-20160507-csruprgucaujkfkrcywhwou7nbeis5fo


Packages can also be referred to from the command line by their package
hash. Using the ``spack find -lf`` command earlier we saw that the hash
of our optimized installation of libelf (``cppflags="-O3"``) began with
``vrv2ttb``. We can now explicitly build with that package without typing
the entire spec, by using the ``/`` sigil to refer to it by hash. As with
other tools like git, you do not need to specify an *entire* hash on the
command line.  You can specify just enough digits to identify a hash
uniquely.  If a hash prefix is ambiguous (i.e., two or more installed
packages share the prefix) then spack will report an error.

.. code-block:: console

  $ spack install libdwarf ^/vrv2ttb
  ==> Installing libdwarf
  ==> libelf is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libelf-0.8.12-vrv2ttbd34xlfoxy4jwt6qsjrcbalmmw
  ==> Can not find version 20160507 in url_list
  ==> Trying to fetch from ~/spack/var/spack/cache/libdwarf/libdwarf-20160507.tar.gz
  #################################################################################################################################################################################################################################################### 100.0%
  ==> Staging archive: ~/spack/var/spack/stage/libdwarf-20160507-dtg3tgnp7htccoly26gduqlrgvnwcp5t/libdwarf-20160507.tar.gz
  ==> Created stage in ~/spack/var/spack/stage/libdwarf-20160507-dtg3tgnp7htccoly26gduqlrgvnwcp5t
  ==> No patches needed for libdwarf
  ==> Building libdwarf [Package]
  ==> Executing phase : 'install'
  ==> Successfully installed libdwarf
    Fetch: 0.96s.  Build: 24.03s.  Total: 24.99s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libdwarf-20160507-dtg3tgnp7htccoly26gduqlrgvnwcp5t


The ``spack find`` command can also take a ``-d`` flag, which can show
dependency information. Note that each package has a top-level entry,
even if it also appears as a dependency.

.. code-block:: console

  $ spack find -ldf
  ==> 9 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
  dtg3tgn    libdwarf@20160507%gcc
  vrv2ttb        ^libelf@0.8.12%gcc cppflags="-O3"

  yfx6p3g    libdwarf@20160507%gcc
  csrt4qx        ^libelf@0.8.13%gcc

  ipggckv    libelf@0.8.12%gcc

  vrv2ttb    libelf@0.8.12%gcc cppflags="-O3"

  csrt4qx    libelf@0.8.13%gcc


  -- linux-redhat6-x86_64 / intel@15.0.4 --------------------------
  w33hrej    libelf@0.8.13%intel


  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
  csruprg    libdwarf@20160507%intel
  4blbe3q        ^libelf@0.8.12%intel

  4blbe3q    libelf@0.8.12%intel

  7wgp32x    libelf@0.8.13%intel


As we get to more complex packages, full installs will take too long to
build in the time allotted for this tutorial. Our collaborators at CERN
have been working on binary caching for Spack, which would allow for very
fast installs of previously built packages. We are still working out the
security ramifications of the feature, but it is coming soon.

For now, we will switch to doing "fake" installs. When supplied with the
``--fake`` flag (primarily used for debugging), Spack computes build
metadata the same way it normally would, but it does not download the
source or run the install script for a pacakge. We can use this to
quickly demonstrate some of the more advanced Spack features in our
limited tutorial time.

``HDF5`` is an example of a more complicated package, with an MPI
dependency. If we install it "out of the box," it will build with
``openmpi``.

.. code-block:: console

  $ spack install --fake hdf5
  ==> Installing hdf5
  ==> Installing zlib
  ==> Building zlib [Package]
  ==> Successfully installed zlib
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> Installing openmpi
  ==> Installing hwloc
  ==> Installing libpciaccess
  ==> Installing util-macros
  ==> Building util-macros [Package]
  ==> Successfully installed util-macros
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/util-macros-1.19.0-pc6zhs4cnkmg2cv4et4fizsp6scuvacg
  ==> Installing libtool
  ==> Installing m4
  ==> Installing libsigsegv
  ==> Building libsigsegv [Package]
  ==> Successfully installed libsigsegv
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libsigsegv-2.10-q4cok3yber7lhf3jswg6mysg7oi53unh
  ==> Building m4 [Package]
  ==> Successfully installed m4
    Fetch: .  Build: 0.23s.  Total: 0.23s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/m4-1.4.17-qijdzvhjyybrtwbqm73vykhmkaqro3je
  ==> Building libtool [Package]
  ==> Successfully installed libtool
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libtool-2.4.6-rdx5nkfjwlvcanz5il3ys2pe34j4vxx5
  ==> Installing pkg-config
  ==> Building pkg-config [Package]
  ==> Successfully installed pkg-config
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/pkg-config-0.29.1-wpjnlzahdw6ahkrgmqyeugkj2zhv4tui
  ==> Building libpciaccess [Package]
  ==> Successfully installed libpciaccess
    Fetch: .  Build: 0.10s.  Total: 0.10s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libpciaccess-0.13.4-m2f6fpm22rpprq2ihkmfx6llf363264m
  ==> Building hwloc [Package]
  ==> Successfully installed hwloc
    Fetch: .  Build: 0.23s.  Total: 0.23s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hwloc-1.11.4-xpb6hbl2hsze25cgdgfnoppn6rchhzaz
  ==> Building openmpi [Package]
  ==> Successfully installed openmpi
    Fetch: .  Build: 0.35s.  Total: 0.35s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openmpi-2.0.1-j4cgoq4furxvr73pq72r2qgywgksw3qn
  ==> Building hdf5 [AutotoolsPackage]
  ==> Successfully installed hdf5
    Fetch: .  Build: 0.61s.  Total: 0.61s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hdf5-1.10.0-patch1-ezvtnox35albuaxqryuondweyjgeo6es


Spack packages can also have variants. Boolean variants can be specified
using the ``+`` and ``~`` or ``-`` sigils. There are two sigils for
``False`` to avoid conflicts with shell parsing in different
situations. Variants (boolean or otherwise) can also be specified using
the same syntax as compiler flags.  Here we can install HDF5 without MPI
support.

.. code-block:: console

  $ spack install --fake hdf5~mpi
  ==> Installing hdf5
  ==> zlib is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> Building hdf5 [AutotoolsPackage]
  ==> Successfully installed hdf5
    Fetch: .  Build: 0.22s.  Total: 0.22s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hdf5-1.10.0-patch1-twppaioxqn6lti4grgopnmhwcq3h2rpw


We might also want to install HDF5 with a different MPI
implementation. While MPI is not a package itself, packages can depend on
abstract interfaces like MPI. Spack handles these through "virtual
dependencies." A package, such as HDF5, can depend on the MPI
interface. Other packages (``openmpi``, ``mpich``, ``mvapich``, etc.)
provide the MPI interface.  Any of these providers can be requested for
an MPI dependency. For example, we can build HDF5 with MPI support
provided by mpich by specifying a dependency on ``mpich``. Spack also
supports versioning of virtual dependencies. A package can depend on the
MPI interface at version 3, and provider packages specify what version of
the interface *they* provide. The partial spec ``^mpi@3`` can be safisfied
by any of several providers.

.. code-block:: console

  $ spack install --fake hdf5+mpi ^mpich
  ==> Installing hdf5
  ==> mpich is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mpich-3.2-5jlp2ndnsb67txggraglu47vjmayx5za
  ==> zlib is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> Building hdf5 [AutotoolsPackage]
  ==> Successfully installed hdf5
    Fetch: .  Build: 0.38s.  Total: 0.38s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hdf5-1.10.0-patch1-j36yfw25i6gdd3q4vwlupgkpwic4ua6m


We'll do a quick check in on what we have installed so far.

.. code-block:: console

  $ spack find -ldf
  ==> 22 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
  twppaio    hdf5@1.10.0-patch1%gcc
  ayc4jq7        ^zlib@1.2.8%gcc

  j36yfw2    hdf5@1.10.0-patch1%gcc
  5jlp2nd        ^mpich@3.2%gcc
  ayc4jq7        ^zlib@1.2.8%gcc

  ezvtnox    hdf5@1.10.0-patch1%gcc
  j4cgoq4        ^openmpi@2.0.1%gcc
  xpb6hbl            ^hwloc@1.11.4%gcc
  m2f6fpm                ^libpciaccess@0.13.4%gcc
  ayc4jq7        ^zlib@1.2.8%gcc

  xpb6hbl    hwloc@1.11.4%gcc
  m2f6fpm        ^libpciaccess@0.13.4%gcc

  dtg3tgn    libdwarf@20160507%gcc
  vrv2ttb        ^libelf@0.8.12%gcc cppflags="-O3"

  yfx6p3g    libdwarf@20160507%gcc
  csrt4qx        ^libelf@0.8.13%gcc

  ipggckv    libelf@0.8.12%gcc

  vrv2ttb    libelf@0.8.12%gcc cppflags="-O3"

  csrt4qx    libelf@0.8.13%gcc

  m2f6fpm    libpciaccess@0.13.4%gcc

  q4cok3y    libsigsegv@2.10%gcc

  rdx5nkf    libtool@2.4.6%gcc

  qijdzvh    m4@1.4.17%gcc
  q4cok3y        ^libsigsegv@2.10%gcc

  5jlp2nd    mpich@3.2%gcc

  j4cgoq4    openmpi@2.0.1%gcc
  xpb6hbl        ^hwloc@1.11.4%gcc
  m2f6fpm            ^libpciaccess@0.13.4%gcc

  wpjnlza    pkg-config@0.29.1%gcc

  pc6zhs4    util-macros@1.19.0%gcc

  ayc4jq7    zlib@1.2.8%gcc


  -- linux-redhat6-x86_64 / intel@15.0.4 --------------------------
  w33hrej    libelf@0.8.13%intel


  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
  csruprg    libdwarf@20160507%intel
  4blbe3q        ^libelf@0.8.12%intel

  4blbe3q    libelf@0.8.12%intel

  7wgp32x    libelf@0.8.13%intel


Spack models the dependencies of packages as a directed acyclic graph
(DAG). The ``spack find -d`` command shows the tree representation of
that graph.  We can also use the ``spack graph`` command to view the entire
DAG as a graph.

.. code-block:: console

  $ spack graph hdf5+mpi ^mpich
  o  hdf5
  |\
  o |  zlib
   /
  o  mpich

You may also have noticed that there are some packages shown in the
``spack find -d`` output that we didn't install explicitly. These are
dependencies that were installed implicitly. A few packages installed
implicitly are not shown as dependencies in the ``spack find -d``
output. These are build dependencies. For example, ``libpciaccess`` is a
dependency of openmpi and requires m4 to build. Spack will build `m4`` as
part of the installation of ``openmpi``, but it does not become a part of
the DAG because it is not linked in at run time. Spack handles build
dependencies differently because of their different (less strict)
consistency requirements. It is entirely possible to have two packages
using different versions of a dependency to build, which obviously cannot
be done with linked dependencies.

``HDF5`` is more complicated than our basic example of libelf and
libdwarf, but it's still within the realm of software that an experienced
HPC user could reasonably expect to install given a bit of time. Now
let's look at a more complicated package.

.. code-block:: console

  $ spack install --fake trilinos
  ==> Installing trilinos
  ==> Installing superlu-dist
  ==> openmpi is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openmpi-2.0.1-j4cgoq4furxvr73pq72r2qgywgksw3qn
  ==> Installing parmetis
  ==> openmpi is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openmpi-2.0.1-j4cgoq4furxvr73pq72r2qgywgksw3qn
  ==> Installing cmake
  ==> Installing bzip2
  ==> Building bzip2 [Package]
  ==> Successfully installed bzip2
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/bzip2-1.0.6-gll2xsahysy7ji5gkmfxwkofdt3mwjhs
  ==> expat is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/expat-2.2.0-mg5kwd3kluxdgorj32vzbp7aksg3vqej
  ==> Installing ncurses
  ==> Building ncurses [Package]
  ==> Successfully installed ncurses
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/ncurses-6.0-fttg4astvrtq2buey4wq66tnyu7bgj2c
  ==> zlib is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> Installing openssl
  ==> zlib is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> Building openssl [Package]
  ==> Successfully installed openssl
    Fetch: .  Build: 0.23s.  Total: 0.23s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openssl-1.0.2j-kt5xyk2dkho6tzadnqlbnbujmljprylg
  ==> Installing libarchive
  ==> Installing lzma
  ==> Building lzma [Package]
  ==> Successfully installed lzma
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/lzma-4.32.7-hah2cdo3zbulz6yg5do6dvnfn6en5v5c
  ==> Installing nettle
  ==> m4 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/m4-1.4.17-qijdzvhjyybrtwbqm73vykhmkaqro3je
  ==> Installing gmp
  ==> m4 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/m4-1.4.17-qijdzvhjyybrtwbqm73vykhmkaqro3je
  ==> Building gmp [AutotoolsPackage]
  ==> Successfully installed gmp
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/gmp-6.1.1-uwn4gfdtq3sywy5uf4f7znrh66oybikf
  ==> Building nettle [Package]
  ==> Successfully installed nettle
    Fetch: .  Build: 0.18s.  Total: 0.18s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/nettle-3.2-w4ieitifcmrldo4ra7as63apagzf56ja
  ==> bzip2 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/bzip2-1.0.6-gll2xsahysy7ji5gkmfxwkofdt3mwjhs
  ==> expat is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/expat-2.2.0-mg5kwd3kluxdgorj32vzbp7aksg3vqej
  ==> Installing libxml2
  ==> Installing xz
  ==> Building xz [Package]
  ==> Successfully installed xz
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/xz-5.2.2-bxh6cpyqqozazm5okvjqk23sww3gccnf
  ==> zlib is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> Building libxml2 [Package]
  ==> Successfully installed libxml2
    Fetch: .  Build: 0.35s.  Total: 0.35s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libxml2-2.9.4-un323rppyu5qipkegyf7flmymvtmunrx
  ==> zlib is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> Installing lz4
  ==> Building lz4 [Package]
  ==> Successfully installed lz4
    Fetch: .  Build: 0.12s.  Total: 0.12s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/lz4-131-ivy2fcaw7ywujx74weebdi5bsm7q4vkc
  ==> openssl is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openssl-1.0.2j-kt5xyk2dkho6tzadnqlbnbujmljprylg
  ==> xz is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/xz-5.2.2-bxh6cpyqqozazm5okvjqk23sww3gccnf
  ==> Installing lzo
  ==> Building lzo [AutotoolsPackage]
  ==> Successfully installed lzo
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/lzo-2.09-dlgnm74ozo6baactkft5oah2jre2ri2i
  ==> Building libarchive [Package]
  ==> Successfully installed libarchive
    Fetch: .  Build: 1.35s.  Total: 1.35s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libarchive-3.2.1-biq3kebw7vel7njusill7vv7mjldkqjv
  ==> xz is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/xz-5.2.2-bxh6cpyqqozazm5okvjqk23sww3gccnf
  ==> Installing curl
  ==> zlib is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> openssl is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openssl-1.0.2j-kt5xyk2dkho6tzadnqlbnbujmljprylg
  ==> Building curl [Package]
  ==> Successfully installed curl
    Fetch: .  Build: 0.36s.  Total: 0.36s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/curl-7.50.3-oze4gqutj4x2isbkcn5ob2bhhxbskod4
  ==> Building cmake [Package]
  ==> Successfully installed cmake
    Fetch: .  Build: 1.64s.  Total: 1.64s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/cmake-3.6.1-n2nkknrku6dvuneo3rjumim7axt7n36e
  ==> Installing metis
  ==> cmake is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/cmake-3.6.1-n2nkknrku6dvuneo3rjumim7axt7n36e
  ==> Building metis [Package]
  ==> Successfully installed metis
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/metis-5.1.0-ithifyl4xvqbn76js23wsb4tjnztrbdv
  ==> Building parmetis [Package]
  ==> Successfully installed parmetis
    Fetch: .  Build: 0.62s.  Total: 0.62s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/parmetis-4.0.3-rtg6hml5t6acdcnxomn3l5zfiful4d2t
  ==> Installing openblas
  ==> Building openblas [Package]
  ==> Successfully installed openblas
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> metis is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/metis-5.1.0-ithifyl4xvqbn76js23wsb4tjnztrbdv
  ==> Building superlu-dist [Package]
  ==> Successfully installed superlu-dist
    Fetch: .  Build: 0.85s.  Total: 0.85s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/superlu-dist-5.1.1-25r6jlvkpjnkiuwt2rtbzhk3l3htuxs7
  ==> cmake is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/cmake-3.6.1-n2nkknrku6dvuneo3rjumim7axt7n36e
  ==> Installing glm
  ==> cmake is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/cmake-3.6.1-n2nkknrku6dvuneo3rjumim7axt7n36e
  ==> Building glm [Package]
  ==> Successfully installed glm
    Fetch: .  Build: 0.12s.  Total: 0.12s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/glm-0.9.7.1-7a6oho4aerz7vftxd5ur7lywscht2iry
  ==> Installing hypre
  ==> openmpi is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openmpi-2.0.1-j4cgoq4furxvr73pq72r2qgywgksw3qn
  ==> openblas is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> Building hypre [Package]
  ==> Successfully installed hypre
    Fetch: .  Build: 0.61s.  Total: 0.61s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hypre-2.11.1-lf7hcejiiww5peesh57quda72z67veit
  ==> metis is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/metis-5.1.0-ithifyl4xvqbn76js23wsb4tjnztrbdv
  ==> Installing netlib-scalapack
  ==> openmpi is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openmpi-2.0.1-j4cgoq4furxvr73pq72r2qgywgksw3qn
  ==> cmake is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/cmake-3.6.1-n2nkknrku6dvuneo3rjumim7axt7n36e
  ==> openblas is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> Building netlib-scalapack [Package]
  ==> Successfully installed netlib-scalapack
    Fetch: .  Build: 0.61s.  Total: 0.61s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/netlib-scalapack-2.0.2-dvcanz2qq4dfcexznbhbmzbxfj43uz4q
  ==> Installing suite-sparse
  ==> Installing tbb
  ==> Building tbb [Package]
  ==> Successfully installed tbb
    Fetch: .  Build: 0.12s.  Total: 0.12s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/tbb-4.4.4-zawzkkhrmdonbjpj3a5bb6gkgnqlrjeu
  ==> openblas is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> metis is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/metis-5.1.0-ithifyl4xvqbn76js23wsb4tjnztrbdv
  ==> Building suite-sparse [Package]
  ==> Successfully installed suite-sparse
    Fetch: .  Build: 0.49s.  Total: 0.49s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/suite-sparse-4.5.3-lvur6hriy2j7xfjwh5punp3exwpynzm6
  ==> openmpi is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openmpi-2.0.1-j4cgoq4furxvr73pq72r2qgywgksw3qn
  ==> Installing netcdf
  ==> m4 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/m4-1.4.17-qijdzvhjyybrtwbqm73vykhmkaqro3je
  ==> curl is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/curl-7.50.3-oze4gqutj4x2isbkcn5ob2bhhxbskod4
  ==> zlib is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> hdf5 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hdf5-1.10.0-patch1-ezvtnox35albuaxqryuondweyjgeo6es
  ==> Building netcdf [Package]
  ==> Successfully installed netcdf
    Fetch: .  Build: 0.90s.  Total: 0.90s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/netcdf-4.4.1-tcl4zbrmdfrit2cqlaxig6xieu5h552j
  ==> Installing mumps
  ==> netlib-scalapack is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/netlib-scalapack-2.0.2-dvcanz2qq4dfcexznbhbmzbxfj43uz4q
  ==> openmpi is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openmpi-2.0.1-j4cgoq4furxvr73pq72r2qgywgksw3qn
  ==> openblas is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> Building mumps [Package]
  ==> Successfully installed mumps
    Fetch: .  Build: 0.74s.  Total: 0.74s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mumps-5.0.2-kr5r4nnx5tfcacxnk3ii5dsxbe6pu5fy
  ==> Installing matio
  ==> Building matio [Package]
  ==> Successfully installed matio
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/matio-1.5.2-4zrozucookychlvc4q53omp2zyfk2bed
  ==> Installing boost
  ==> bzip2 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/bzip2-1.0.6-gll2xsahysy7ji5gkmfxwkofdt3mwjhs
  ==> zlib is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> Building boost [Package]
  ==> Successfully installed boost
    Fetch: .  Build: 0.35s.  Total: 0.35s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/boost-1.62.0-je7eqvzt74kezwhh55y5lwt5dy6pnali
  ==> parmetis is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/parmetis-4.0.3-rtg6hml5t6acdcnxomn3l5zfiful4d2t
  ==> openblas is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> hdf5 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hdf5-1.10.0-patch1-ezvtnox35albuaxqryuondweyjgeo6es
  ==> Building trilinos [Package]
  ==> Successfully installed trilinos
    Fetch: .  Build: 2.63s.  Total: 2.63s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/trilinos-12.8.1-uvd6dfd7x4uyvck4awo3r3frudihn4ar


Now we're starting to see the power of Spack. Trilinos has 11 top level
dependecies, many of which have dependencies of their own. Installing
more complex packages can take days or weeks even for an experienced
user. Although we've done a fake installation for the tutorial, a real
installation of trilinos using Spack takes about 3 hours (depending on
the system), but only 20 seconds of programmer time.

Spack manages constistency of the entire DAG. Every MPI dependency will
be satisfied by the same configuration of MPI, etc. If we install
``trilinos`` again specifying a dependency on our previous HDF5 built
with ``mpich``:

.. code-block:: console

  $ spack install --fake trilinos ^hdf5+mpi ^mpich
  ==> Installing trilinos
  ==> Installing superlu-dist
  ==> mpich is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mpich-3.2-5jlp2ndnsb67txggraglu47vjmayx5za
  ==> metis is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/metis-5.1.0-ithifyl4xvqbn76js23wsb4tjnztrbdv
  ==> Installing parmetis
  ==> mpich is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mpich-3.2-5jlp2ndnsb67txggraglu47vjmayx5za
  ==> metis is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/metis-5.1.0-ithifyl4xvqbn76js23wsb4tjnztrbdv
  ==> cmake is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/cmake-3.6.1-n2nkknrku6dvuneo3rjumim7axt7n36e
  ==> Building parmetis [Package]
  ==> Successfully installed parmetis
    Fetch: .  Build: 0.38s.  Total: 0.38s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/parmetis-4.0.3-43kbtni6p5y446c6qdkybq4htj7ot4zn
  ==> openblas is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> Building superlu-dist [Package]
  ==> Successfully installed superlu-dist
    Fetch: .  Build: 0.61s.  Total: 0.61s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/superlu-dist-5.1.1-46uuupehmonx5jicc6xnegnud2n5jqyl
  ==> cmake is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/cmake-3.6.1-n2nkknrku6dvuneo3rjumim7axt7n36e
  ==> glm is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/glm-0.9.7.1-7a6oho4aerz7vftxd5ur7lywscht2iry
  ==> Installing hypre
  ==> mpich is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mpich-3.2-5jlp2ndnsb67txggraglu47vjmayx5za
  ==> openblas is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> Building hypre [Package]
  ==> Successfully installed hypre
    Fetch: .  Build: 0.37s.  Total: 0.37s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hypre-2.11.1-6ajnyymoivs5apajd7thjisae36jv4lz
  ==> metis is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/metis-5.1.0-ithifyl4xvqbn76js23wsb4tjnztrbdv
  ==> Installing netlib-scalapack
  ==> mpich is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mpich-3.2-5jlp2ndnsb67txggraglu47vjmayx5za
  ==> cmake is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/cmake-3.6.1-n2nkknrku6dvuneo3rjumim7axt7n36e
  ==> openblas is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> Building netlib-scalapack [Package]
  ==> Successfully installed netlib-scalapack
    Fetch: .  Build: 0.37s.  Total: 0.37s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/netlib-scalapack-2.0.2-dayeep27omm26wksd3iqvbu3gezc2eoh
  ==> suite-sparse is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/suite-sparse-4.5.3-lvur6hriy2j7xfjwh5punp3exwpynzm6
  ==> Installing netcdf
  ==> m4 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/m4-1.4.17-qijdzvhjyybrtwbqm73vykhmkaqro3je
  ==> curl is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/curl-7.50.3-oze4gqutj4x2isbkcn5ob2bhhxbskod4
  ==> zlib is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/zlib-1.2.8-ayc4jq7vxuzge5n444gutvskeytfdruh
  ==> hdf5 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hdf5-1.10.0-patch1-j36yfw25i6gdd3q4vwlupgkpwic4ua6m
  ==> Building netcdf [Package]
  ==> Successfully installed netcdf
    Fetch: .  Build: 0.67s.  Total: 0.67s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/netcdf-4.4.1-gfemi4jk4qltvp33xhtpkam7dozbqvhq
  ==> Installing mumps
  ==> mpich is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mpich-3.2-5jlp2ndnsb67txggraglu47vjmayx5za
  ==> netlib-scalapack is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/netlib-scalapack-2.0.2-dayeep27omm26wksd3iqvbu3gezc2eoh
  ==> openblas is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> Building mumps [Package]
  ==> Successfully installed mumps
    Fetch: .  Build: 0.49s.  Total: 0.49s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mumps-5.0.2-w7t5pl3jhhwitfiyer63zj6zv7idkt3m
  ==> mpich is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mpich-3.2-5jlp2ndnsb67txggraglu47vjmayx5za
  ==> matio is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/matio-1.5.2-4zrozucookychlvc4q53omp2zyfk2bed
  ==> boost is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/boost-1.62.0-je7eqvzt74kezwhh55y5lwt5dy6pnali
  ==> parmetis is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/parmetis-4.0.3-43kbtni6p5y446c6qdkybq4htj7ot4zn
  ==> openblas is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/openblas-0.2.19-bwofa7fhff6od5zn56vy3j4eeyupsqgt
  ==> hdf5 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hdf5-1.10.0-patch1-j36yfw25i6gdd3q4vwlupgkpwic4ua6m
  ==> Building trilinos [Package]
  ==> Successfully installed trilinos
    Fetch: .  Build: 2.42s.  Total: 2.42s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/trilinos-12.8.1-ffwrpxnq7lhiw2abxn2u7ffr4jjsdwep

We see that every package in the trilinos DAG that depends on MPI now
uses ``mpich``.

.. code-block:: console

  $ spack find -d trilinos
  ==> 2 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
      trilinos@12.8.1
          ^boost@1.62.0
              ^bzip2@1.0.6
              ^zlib@1.2.8
          ^glm@0.9.7.1
          ^hdf5@1.10.0-patch1
              ^mpich@3.2
          ^hypre@2.11.1
              ^openblas@0.2.19
          ^matio@1.5.2
          ^metis@5.1.0
          ^mumps@5.0.2
              ^netlib-scalapack@2.0.2
          ^netcdf@4.4.1
              ^curl@7.50.3
                  ^openssl@1.0.2j
          ^parmetis@4.0.3
          ^suite-sparse@4.5.3
              ^tbb@4.4.4
          ^superlu-dist@5.1.1

      trilinos@12.8.1
          ^boost@1.62.0
              ^bzip2@1.0.6
              ^zlib@1.2.8
          ^glm@0.9.7.1
          ^hdf5@1.10.0-patch1
              ^openmpi@2.0.1
                  ^hwloc@1.11.4
                      ^libpciaccess@0.13.4
          ^hypre@2.11.1
              ^openblas@0.2.19
          ^matio@1.5.2
          ^metis@5.1.0
          ^mumps@5.0.2
              ^netlib-scalapack@2.0.2
          ^netcdf@4.4.1
              ^curl@7.50.3
                  ^openssl@1.0.2j
          ^parmetis@4.0.3
          ^suite-sparse@4.5.3
              ^tbb@4.4.4
          ^superlu-dist@5.1.1


As we discussed before, the ``spack find -d`` command shows the
dependency information as a tree. While that is often sufficient, many
complicated packages, including trilinos, have dependencies that
cannot be fully represented as a tree. Again, the ``spack graph``
command shows the full DAG of the dependency information.

.. code-block:: console

  $ spack graph trilinos
  o  trilinos
  |\
  | |\
  | | |\
  | | | |\
  | | | | |\
  | | | | | |\
  | | | | | | |\
  | o | | | | | |  netcdf
  | |\ \ \ \ \ \ \
  | | |\ \ \ \ \ \ \
  | | | o | | | | | |  curl
  | | |/| | | | | | |
  | |/| | | | | | | |
  | | | o | | | | | |  openssl
  | | |/ / / / / / /
  | |/| | | | | | |
  | | o | | | | | |  hdf5
  | |/| | | | | | |
  | | |/ / / / / /
  | o | | | | | |  zlib
  |  / / / / / /
  o | | | | | |  swig
  o | | | | | |  pcre
   / / / / / /
  o | | | | |  mpi
   / / / / /
  o | | | |  matio
   / / / /
  o | | |  lapack
   / / /
  o | |  glm
   / /
  o |  boost
   /
  o  blas


You can control how the output is displayed with a number of options.

The ASCII output from ``spack graph`` can be difficult to parse for
complicated packages. The output can be changed to the ``graphviz``
``.dot`` format using the `--dot` flag.

.. code-block:: console

  $ spack graph --dot trilinos | dot -Tpdf trilinos_graph.pdf

.. _basics-tutorial-uninstall:

---------------------
Uninstalling Packages
---------------------

Earlier we installed many configurations each of libelf and
libdwarf. Now we will go through and uninstall some of those packages
that we didn't really need.

.. code-block:: console

  $ spack find -d libdwarf
  ==> 3 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
      libdwarf@20160507
          ^libelf@0.8.12

      libdwarf@20160507
          ^libelf@0.8.13


  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
      libdwarf@20160507
          ^libelf@0.8.12

  $ spack find libelf
  ==> 6 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
  libelf@0.8.12  libelf@0.8.12  libelf@0.8.13

  -- linux-redhat6-x86_64 / intel@15.0.4 --------------------------
  libelf@0.8.13

  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
  libelf@0.8.12  libelf@0.8.13


We can uninstall packages by spec using the same syntax as install.

.. code-block:: console

  $ spack uninstall libelf%intel@15.0.4
  ==> The following packages will be uninstalled :

  -- linux-redhat6-x86_64 / intel@15.0.4 --------------------------
  w33hrej libelf@0.8.13%intel


  ==> Do you want to proceed ? [y/n]
  y
  ==> Successfully uninstalled libelf@0.8.13%intel@15.0.4 arch=linux-redhat6-x86_64-w33hrej



  $ spack find -lf libelf
  ==> 5 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
  ipggckv libelf@0.8.12%gcc

  vrv2ttb libelf@0.8.12%gcc cppflags="-O3"

  csrt4qx libelf@0.8.13%gcc


  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
  4blbe3q libelf@0.8.12%intel

  7wgp32x libelf@0.8.13%intel


We can uninstall packages by referring only to their hash.


We can use either ``-f`` (force) or ``-d`` (remove dependents as well) to
remove packages that are required by another installed package.

.. code-block:: console

  $ spack uninstall /4blb
  ==> Error: Will not uninstall libelf@0.8.12%intel@16.0.3-4blbe3q

  The following packages depend on it:
  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
  csruprg libdwarf@20160507%intel


  ==> Error: You can use spack uninstall --dependents to uninstall these dependencies as well
  $ spack uninstall -d /4blb
  ==> The following packages will be uninstalled :

  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
  csruprg libdwarf@20160507%intel

  4blbe3q libelf@0.8.12%intel


  ==> Do you want to proceed ? [y/n]
  y
  ==> Successfully uninstalled libdwarf@20160507%intel@16.0.3 arch=linux-redhat6-x86_64-csruprg
  ==> Successfully uninstalled libelf@0.8.12%intel@16.0.3 arch=linux-redhat6-x86_64-4blbe3q


Spack will not uninstall packages that are not sufficiently
specified. The ``-a`` (all) flag can be used to uninstall multiple
packages at once.

.. code-block:: console

  $ spack uninstall trilinos
  ==> Error: trilinos matches multiple packages:

  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
  ffwrpxn trilinos@12.8.1%gcc+boost~debug+hdf5+hypre+metis+mumps~python+shared+suite-sparse+superlu-dist

  uvd6dfd trilinos@12.8.1%gcc+boost~debug+hdf5+hypre+metis+mumps~python+shared+suite-sparse+superlu-dist


  ==> Error: You can either:
      a) Use a more specific spec, or
      b) use spack uninstall -a to uninstall ALL matching specs.



  $ spack uninstall /ffwr
  ==> The following packages will be uninstalled :

  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
  ffwrpxn trilinos@12.8.1%gcc+boost~debug+hdf5+hypre+metis+mumps~python+shared+suite-sparse+superlu-dist


  ==> Do you want to proceed ? [y/n]
  y
  ==> Successfully uninstalled trilinos@12.8.1%gcc@4.4.7+boost~debug+hdf5+hypre+metis+mumps~python+shared+suite-sparse+superlu-dist arch=linux-redhat6-x86_64-ffwrpxn

-----------------------------
Advanced ``spack find`` Usage
-----------------------------

We will go over some additional uses for the `spack find` command not
already covered in the :ref:`basics-tutorial-install` and
:ref:`basics-tutorial-uninstall` sections.

The ``spack find`` command can accept what we call "anonymous specs."
These are expressions in spec syntax that do not contain a package
name. For example, `spack find %intel` will return every package built
with the intel compiler, and ``spack find cppflags="-O3"`` will
return every package which was built with ``cppflags="-O3"``.

.. code-block:: console

  $ spack find %intel
  ==> 1 installed packages.
  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
  libelf@0.8.13



  $ spack find cppflags="-O3"
  ==> 1 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
  libelf@0.8.12


The ``find`` command can also show which packages were installed
explicitly (rather than pulled in as a dependency) using the ``-e``
flag. The ``-E`` flag shows implicit installs only. The ``find`` command can
also show the path to which a spack package was installed using the ``-p``
command.

.. code-block:: console

  $ spack find -pe
  ==> 10 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
      hdf5@1.10.0-patch1  ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hdf5-1.10.0-patch1-twppaioxqn6lti4grgopnmhwcq3h2rpw
      hdf5@1.10.0-patch1  ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hdf5-1.10.0-patch1-j36yfw25i6gdd3q4vwlupgkpwic4ua6m
      hdf5@1.10.0-patch1  ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/hdf5-1.10.0-patch1-ezvtnox35albuaxqryuondweyjgeo6es
      libdwarf@20160507   ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libdwarf-20160507-dtg3tgnp7htccoly26gduqlrgvnwcp5t
      libdwarf@20160507   ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libdwarf-20160507-yfx6p3g3rkmqvcqbmtb34o6pln7pqvcz
      libelf@0.8.12       ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libelf-0.8.12-ipggckv6i7h44iryzfa4dwdela32a7fy
      libelf@0.8.12       ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libelf-0.8.12-vrv2ttbd34xlfoxy4jwt6qsjrcbalmmw
      libelf@0.8.13       ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/libelf-0.8.13-csrt4qxfkhjgn5xg3zjpkir7xdnszl2a
      trilinos@12.8.1     ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/trilinos-12.8.1-uvd6dfd7x4uyvck4awo3r3frudihn4ar

  -- linux-redhat6-x86_64 / intel@16.0.3 --------------------------
      libelf@0.8.13  ~/spack/opt/spack/linux-redhat6-x86_64/intel-16.0.3/libelf-0.8.13-7wgp32xksatkvw2tbssmehw2t5tnxndj


---------------------
Customizing Compilers
---------------------


Spack manages a list of available compilers on the system, detected
automatically from from the user's ``PATH`` variable. The ``spack
compilers`` command is an alias for the command ``spack compiler list``.

.. code-block:: console

  $ spack compilers
  ==> Available compilers
  -- gcc ----------------------------------------------------------
  gcc@4.4.7

  -- intel --------------------------------------------------------
  intel@16.0.3  intel@15.0.1  intel@14.0.0  intel@12.1.3  intel@10.0
  intel@16.0.2  intel@15.0.0  intel@13.1.1  intel@12.1.2  intel@9.1
  intel@16.0.1  intel@14.0.4  intel@13.1.0  intel@12.1.0
  intel@16.0.0  intel@14.0.3  intel@13.0.1  intel@12.0.4
  intel@15.0.4  intel@14.0.2  intel@13.0.0  intel@11.1
  intel@15.0.3  intel@14.0.1  intel@12.1.5  intel@10.1

  -- pgi ----------------------------------------------------------
  pgi@16.5-0   pgi@15.7-0   pgi@14.7-0   pgi@13.2-0  pgi@11.10-0  pgi@9.0-4
  pgi@16.3-0   pgi@15.5-0   pgi@14.3-0   pgi@13.1-1  pgi@11.1-0   pgi@8.0-1
  pgi@16.1-0   pgi@15.1-0   pgi@13.10-0  pgi@12.8-0  pgi@10.9-0   pgi@7.1-3
  pgi@15.10-0  pgi@14.10-0  pgi@13.6-0   pgi@12.1-0  pgi@10.2-0   pgi@7.0-6

The compilers are maintained in a YAML file that can be hand-edited
for special cases. Spack also has tools to add compilers, and
compilers built with Spack can be added to the configuration.

.. code-block:: console

  $ spack install --fake gcc@6.1.0
  ==> Installing gcc
  ==> gmp is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/gmp-6.1.1-uwn4gfdtq3sywy5uf4f7znrh66oybikf
  ==> Installing isl
  ==> gmp is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/gmp-6.1.1-uwn4gfdtq3sywy5uf4f7znrh66oybikf
  ==> Building isl [Package]
  ==> Successfully installed isl
    Fetch: .  Build: 0.19s.  Total: 0.19s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/isl-0.14-hs2w7mjjjaakkmbbv5yvfqf7yyzhorl6
  ==> Installing mpc
  ==> gmp is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/gmp-6.1.1-uwn4gfdtq3sywy5uf4f7znrh66oybikf
  ==> Installing mpfr
  ==> gmp is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/gmp-6.1.1-uwn4gfdtq3sywy5uf4f7znrh66oybikf
  ==> Building mpfr [Package]
  ==> Successfully installed mpfr
    Fetch: .  Build: 0.17s.  Total: 0.17s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mpfr-3.1.4-7kt5ij437khredfq4bvnyu22t3fmtfvt
  ==> Building mpc [Package]
  ==> Successfully installed mpc
    Fetch: .  Build: 0.28s.  Total: 0.28s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mpc-1.0.3-g5taq6lt3zuy5l2jtggi5lctxnl4la5u
  ==> Installing binutils
  ==> m4 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/m4-1.4.17-qijdzvhjyybrtwbqm73vykhmkaqro3je
  ==> Installing bison
  ==> m4 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/m4-1.4.17-qijdzvhjyybrtwbqm73vykhmkaqro3je
  ==> Building bison [Package]
  ==> Successfully installed bison
    Fetch: .  Build: 0.12s.  Total: 0.12s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/bison-3.0.4-hkhfysfvq5l6rsns67g2htmkpxauvnwa
  ==> Installing flex
  ==> m4 is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/m4-1.4.17-qijdzvhjyybrtwbqm73vykhmkaqro3je
  ==> bison is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/bison-3.0.4-hkhfysfvq5l6rsns67g2htmkpxauvnwa
  ==> Building flex [Package]
  ==> Successfully installed flex
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/flex-2.6.0-qd6d73rdfrozdrsdpimvl4tj7d5ps7qg
  ==> Building binutils [Package]
  ==> Successfully installed binutils
    Fetch: .  Build: 0.11s.  Total: 0.11s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/binutils-2.27-iq2hry3gvaxszmwwbnll7njgdgaek56o
  ==> mpfr is already installed in ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/mpfr-3.1.4-7kt5ij437khredfq4bvnyu22t3fmtfvt
  ==> Building gcc [Package]
  ==> Successfully installed gcc
    Fetch: .  Build: 0.66s.  Total: 0.66s.
  [+] ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/gcc-6.1.0-j5576zbsot2ydljlthjzhsirsesnogvh



  $ spack find -p gcc
  ==> 1 installed packages.
  -- linux-redhat6-x86_64 / gcc@4.4.7 -----------------------------
      gcc@6.1.0  ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/gcc-6.1.0-j5576zbsot2ydljlthjzhsirsesnogvh


If we had done a "real" install of gcc, we could add it to our
configuration now using the `spack compiler add` command, but we would
also be waiting for it to install. If we run the command now, it will
return no new compilers.

.. code-block:: console

  $ spack compiler add ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/gcc-6.1.0-j5576zbsot2ydljlthjzhsirsesnogvh/bin
  ==> Found no new compilers

If we had done a real install, the output would have been as follows:

.. code-block:: console

  $ spack compiler add ~/spack/opt/spack/linux-redhat6-x86_64/gcc-4.4.7/gcc-6.1.0-j5576zbsot2ydljlthjzhsirsesnogvh/bin
  ==> Added 1 new compiler to ~/.spack/linux/compilers.yaml
      gcc@6.1.0
