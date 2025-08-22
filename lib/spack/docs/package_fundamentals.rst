.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Learn the fundamental Spack commands for managing software packages, including how to find, inspect, install, and remove them.

.. _basic-usage:

Package Fundamentals
====================

Spack provides a comprehensive ecosystem of software packages that you can install.
In this section you'll learn:

1. How to discover which packages are available,
2. How to get detailed information about specific packages,
3. How to install/uninstall packages, and
4. How to discover, and use, software that has been installed



.. _basic-list-and-info-packages:

Listing Available Packages
--------------------------

To install software with Spack, you need to know what software is available.
You can search for available packages on the `packages.spack.io <https://packages.spack.io>`_ website or by using the ``spack list`` command.

.. _cmd-spack-list:

``spack list``
^^^^^^^^^^^^^^

The ``spack list`` command prints out a list of all of the packages Spack can install:

.. code-block:: spec

   $ spack list

Packages are listed by name in alphabetical order.
A pattern can be used to narrow the list, and the following rules apply:

* A pattern with no wildcards (``*`` or ``?``) is treated as if it starts and ends with ``*``
* All patterns are case-insensitive

To search for all packages whose names contain the word ``sql`` you can run the following command:

.. code-block:: spec

   $ spack list sql

A few options are also provided for more specific searches.
For instance, it is possible to search the description of packages for a match.
A way to list all the packages whose names or descriptions contain the word ``quantum`` is the following:

.. code-block:: spec

   $ spack list -d quantum


.. _cmd-spack-info:

``spack info``
^^^^^^^^^^^^^^

To get more information about a particular package from `spack list`, use `spack info`.
Just supply the name of a package:

.. command-output:: spack info mpich
   :language: spec

Most of the information is self-explanatory.
The *safe versions* are versions for which Spack knows the checksum.
Spack uses this checksum to verify that the versions are downloaded without errors or malicious changes.

:ref:`Dependencies <sec-specs>` and :ref:`virtual dependencies <sec-virtual-dependencies>` are described in more detail later.

.. _cmd-spack-versions:

``spack versions``
^^^^^^^^^^^^^^^^^^

To see *more* available versions of a package, run ``spack versions``.
For example:

.. command-output:: spack versions libelf
   :language: spec

There are two sections in the output.
*Safe versions* are versions for which Spack has a checksum on file.
It can verify that these versions are downloaded correctly.

In many cases, Spack can also show you what versions are available out on the web -- these are *remote versions*.
Spack gets this information by scraping it directly from package web pages.
Depending on the package and how its releases are organized, Spack may or may not be able to find remote versions.

.. _cmd-spack-providers:

``spack providers``
^^^^^^^^^^^^^^^^^^^

You can see what packages provide a particular virtual package using ``spack providers``.
If you wanted to see what packages provide ``mpi``, you would just run:

.. command-output:: spack providers mpi
   :language: spec

And if you *only* wanted to see packages that provide MPI-2, you would add a version specifier to the spec:

.. command-output:: spack providers mpi@2
   :language: spec

Notice that the package versions that provide insufficient MPI versions are now filtered out.

Installing and Uninstalling
---------------------------

.. _cmd-spack-install:

``spack install``
^^^^^^^^^^^^^^^^^

``spack install`` will install any package shown by ``spack list``.
For example, to install the latest version of the ``mpileaks`` package, you might type this:

.. code-block:: spec

   $ spack install mpileaks

If ``mpileaks`` depends on other packages, Spack will install the dependencies first.
It then fetches the ``mpileaks`` tarball, expands it, verifies that it was downloaded without errors, builds it, and installs it in its own directory under ``$SPACK_ROOT/opt``.
You'll see a number of messages from Spack, a lot of build output, and a message that the package is installed.

.. code-block:: spec

   $ spack install mpileaks
   ... dependency build output ...
   ==> Installing mpileaks-1.0-ph7pbnhl334wuhogmugriohcwempqry2
   ==> No binary for mpileaks-1.0-ph7pbnhl334wuhogmugriohcwempqry2 found: installing from source
   ==> mpileaks: Executing phase: 'autoreconf'
   ==> mpileaks: Executing phase: 'configure'
   ==> mpileaks: Executing phase: 'build'
   ==> mpileaks: Executing phase: 'install'
   [+] ~/spack/opt/linux-rhel7-broadwell/gcc-8.1.0/mpileaks-1.0-ph7pbnhl334wuhogmugriohcwempqry2

The last line, with the ``[+]``, indicates where the package is installed.

Add the Spack debug option (one or more times) -- ``spack -d install mpileaks`` -- to get additional (and even more verbose) output.

Building a specific version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack can also build *specific versions* of a package.
To do this, just add ``@`` after the package name, followed by a version:

.. code-block:: spec

   $ spack install mpich@3.0.4

Any number of versions of the same package can be installed at once without interfering with each other.
This is useful for multi-user sites, as installing a version that one user needs will not disrupt existing installations for other users.

In addition to different versions, Spack can customize the compiler, compile-time options (variants), compiler flags, and target architecture of an installation.
Spack is unique in that it can also configure the *dependencies* a package is built with.
For example, two configurations of the same version of a package, one built with boost 1.39.0, and the other version built with version 1.43.0, can coexist.

This can all be done on the command line using the *spec* syntax.
Spack calls the descriptor used to refer to a particular package configuration a **spec**.
In the commands above, ``mpileaks`` and ``mpileaks@3.0.4`` are both valid *specs*.
We'll talk more about how you can use them to customize an installation in :ref:`sec-specs`.

Reusing installed dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, when you run ``spack install``, Spack tries hard to reuse existing installations as dependencies, either from a local store or from remote buildcaches, if configured.
This minimizes unwanted rebuilds of common dependencies, in particular if you update Spack frequently.

In case you want the latest versions and configurations to be installed instead, you can add the ``--fresh`` option:

.. code-block:: spec

   $ spack install --fresh mpich

Reusing installations in this mode is "accidental" and happens only if there's a match between existing installations and what Spack would have installed anyway.

You can use the ``spack spec -I mpich`` command to see what will be reused and what will be built before you install.

You can configure Spack to use the ``--fresh`` behavior by default in ``concretizer.yaml``:

.. code-block:: yaml

   concretizer:
     reuse: false

.. _cmd-spack-uninstall:

``spack uninstall``
^^^^^^^^^^^^^^^^^^^

To uninstall a package, run ``spack uninstall <package>``.
This will ask the user for confirmation before completely removing the directory in which the package was installed.

.. code-block:: spec

   $ spack uninstall mpich

If there are still installed packages that depend on the package to be uninstalled, Spack will refuse to uninstall it.

To uninstall a package and every package that depends on it, you may give the ``--dependents`` option.

.. code-block:: spec

   $ spack uninstall --dependents mpich

will display a list of all the packages that depend on ``mpich`` and, upon confirmation, will uninstall them in the correct order.

A command like

.. code-block:: spec

   $ spack uninstall mpich

may be ambiguous if multiple ``mpich`` configurations are installed.
For example, if both ``mpich@3.0.2`` and ``mpich@3.1`` are installed, ``mpich`` could refer to either one.
Because it cannot determine which one to uninstall, Spack will ask you either to provide a version number to remove the ambiguity or use the ``--all`` option to uninstall all matching packages.

You may force uninstall a package with the ``--force`` option

.. code-block:: spec

   $ spack uninstall --force mpich

but you risk breaking other installed packages.
In general, it is safer to remove dependent packages *before* removing their dependencies or to use the ``--dependents`` option.


.. _nondownloadable:

Garbage collection
^^^^^^^^^^^^^^^^^^

When Spack builds software from sources, it often installs tools that are needed only to build or test other software.
These are not necessary at runtime.
To support cases where removing these tools can be a benefit, Spack provides the ``spack gc`` ("garbage collector") command, which will uninstall all unneeded packages:

.. code-block:: console

   $ spack find
   ==> 24 installed packages
   -- linux-ubuntu18.04-broadwell / gcc@9.0.1 ----------------------
   autoconf@2.69    findutils@4.6.0  libiconv@1.16        libszip@2.1.1  m4@1.4.18    openjpeg@2.3.1  pkgconf@1.6.3  util-macros@1.19.1
   automake@1.16.1  gdbm@1.18.1      libpciaccess@0.13.5  libtool@2.4.6  mpich@3.3.2  openssl@1.1.1d  readline@8.0   xz@5.2.4
   cmake@3.16.1     hdf5@1.10.5      libsigsegv@2.12      libxml2@2.9.9  ncurses@6.1  perl@5.30.0     texinfo@6.5    zlib@1.2.11

   $ spack gc
   ==> The following packages will be uninstalled:

       -- linux-ubuntu18.04-broadwell / gcc@9.0.1 ----------------------
       vn47edz autoconf@2.69    6m3f2qn findutils@4.6.0  ubl6bgk libtool@2.4.6  pksawhz openssl@1.1.1d  urdw22a readline@8.0
       ki6nfw5 automake@1.16.1  fklde6b gdbm@1.18.1      b6pswuo m4@1.4.18      k3s2csy perl@5.30.0     lp5ya3t texinfo@6.5
       ylvgsov cmake@3.16.1     5omotir libsigsegv@2.12  leuzbbh ncurses@6.1    5vmfbrq pkgconf@1.6.3   5bmv4tg util-macros@1.19.1

   ==> Do you want to proceed? [y/N] y

   [ ... ]

   $ spack find
   ==> 9 installed packages
   -- linux-ubuntu18.04-broadwell / gcc@9.0.1 ----------------------
   hdf5@1.10.5  libiconv@1.16  libpciaccess@0.13.5  libszip@2.1.1  libxml2@2.9.9  mpich@3.3.2  openjpeg@2.3.1  xz@5.2.4  zlib@1.2.11

In the example above, ``spack gc`` scans the package database.
It keeps only the packages that were explicitly installed by a user, along with their required ``link`` and ``run`` dependencies (including transitive dependencies).
All other packages, such as build-only dependencies or orphaned packages, are identified as "garbage" and removed.

You can check :ref:`cmd-spack-find-metadata` to see how to query for explicitly installed packages or :ref:`dependency-types` for a more thorough treatment of dependency types.

Marking packages explicit or implicit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, Spack will mark packages a user installs as explicitly installed, while all of its dependencies will be marked as implicitly installed.
Packages can be marked manually as explicitly or implicitly installed by using ``spack mark``.
This can be used in combination with ``spack gc`` to clean up packages that are no longer required.

.. code-block:: spec

  $ spack install m4
  ==> 29005: Installing libsigsegv
  [...]
  ==> 29005: Installing m4
  [...]

  $ spack install m4 ^libsigsegv@2.11
  ==> 39798: Installing libsigsegv
  [...]
  ==> 39798: Installing m4
  [...]

  $ spack find -d
  ==> 4 installed packages
  -- linux-fedora32-haswell / gcc@10.1.1 --------------------------
  libsigsegv@2.11

  libsigsegv@2.12

  m4@1.4.18
      libsigsegv@2.12

  m4@1.4.18
      libsigsegv@2.11

  $ spack gc
  ==> There are no unused specs. Spack's store is clean.

  $ spack mark -i m4 ^libsigsegv@2.11
  ==> m4@1.4.18 : marking the package implicit

  $ spack gc
  ==> The following packages will be uninstalled:

      -- linux-fedora32-haswell / gcc@10.1.1 --------------------------
      5fj7p2o libsigsegv@2.11  c6ensc6 m4@1.4.18

  ==> Do you want to proceed? [y/N]

In the example above, we ended up with two versions of ``m4`` because they depend on different versions of ``libsigsegv``.
``spack gc`` will not remove any of the packages because both versions of ``m4`` have been installed explicitly and both versions of ``libsigsegv`` are required by the ``m4`` packages.

``spack mark`` can also be used to implement upgrade workflows.
The following example demonstrates how ``spack mark`` and ``spack gc`` can be used to only keep the current version of a package installed.

When updating Spack via ``git pull``, new versions for either ``libsigsegv`` or ``m4`` might be introduced.
This will cause Spack to install duplicates.
Because we only want to keep one version, we mark everything as implicitly installed before updating Spack.
If there is no new version for either of the packages, ``spack install`` will simply mark them as explicitly installed, and ``spack gc`` will not remove them.

.. code-block:: spec

  $ spack install m4
  ==> 62843: Installing libsigsegv
  [...]
  ==> 62843: Installing m4
  [...]

  $ spack mark -i -a
  ==> m4@1.4.18 : marking the package implicit

  $ git pull
  [...]

  $ spack install m4
  [...]
  ==> m4@1.4.18 : marking the package explicit
  [...]

  $ spack gc
  ==> There are no unused specs. Spack's store is clean.

When using this workflow for installations that contain more packages, care must be taken to either only mark selected packages or issue ``spack install`` for all packages that should be kept.

You can check :ref:`cmd-spack-find-metadata` to see how to query for explicitly or implicitly installed packages.

Non-Downloadable Tarballs
^^^^^^^^^^^^^^^^^^^^^^^^^

The tarballs for some packages cannot be automatically downloaded by Spack.
This could be for a number of reasons:

#. The author requires users to manually accept a license agreement before downloading (e.g., ``jdk`` and ``galahad``).

#. The software is proprietary and cannot be downloaded on the open Internet.

To install these packages, one must create a mirror and manually add the tarballs in question to it (see :ref:`mirrors`):

#. Create a directory for the mirror.
   You can create this directory anywhere you like, it does not have to be inside ``~/.spack``:

   .. code-block:: console

       $ mkdir ~/.spack/manual_mirror

#. Register the mirror with Spack by creating ``~/.spack/mirrors.yaml``:

   .. code-block:: yaml

       mirrors:
         manual: file://~/.spack/manual_mirror

#. Put your tarballs in it.
   Tarballs should be named ``<package>/<package>-<version>.tar.gz``.
   For example:

   .. code-block:: console

       $ ls -l manual_mirror/galahad

       -rw-------. 1 me me 11657206 Jun 21 19:25 galahad-2.60003.tar.gz

#. Install as usual:

   .. code-block:: console

       $ spack install galahad


Seeing Installed Packages
-------------------------

We know that ``spack list`` shows you the names of available packages, but how do you figure out which are already installed?

.. _cmd-spack-find:

``spack find``
^^^^^^^^^^^^^^

``spack find`` shows the *specs* of installed packages.
A spec is like a name, but it has a version, compiler, architecture, and build options associated with it.
In Spack, you can have many installations of the same package with different specs.

Running ``spack find`` with no arguments lists installed packages:

.. code-block:: spec

   $ spack find
   ==> 74 installed packages.
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
   ImageMagick@6.8.9-10  libdwarf@20130729  py-dateutil@2.4.0
   adept-utils@1.0       libdwarf@20130729  py-ipython@2.3.1
   atk@2.14.0            libelf@0.8.12      py-matplotlib@1.4.2
   boost@1.55.0          libelf@0.8.13      py-nose@1.3.4
   bzip2@1.0.6           libffi@3.1         py-numpy@1.9.1
   cairo@1.14.0          libmng@2.0.2       py-pygments@2.0.1
   callpath@1.0.2        libpng@1.6.16      py-pyparsing@2.0.3
   cmake@3.0.2           libtiff@4.0.3      py-pyside@1.2.2
   dbus@1.8.6            libtool@2.4.2      py-pytz@2014.10
   dbus@1.9.0            libxcb@1.11        py-setuptools@11.3.1
   dyninst@8.1.2         libxml2@2.9.2      py-six@1.9.0
   fontconfig@2.11.1     libxml2@2.9.2      python@2.7.8
   freetype@2.5.3        llvm@3.0           qhull@1.0
   gdk-pixbuf@2.31.2     memaxes@0.5        qt@4.8.6
   glib@2.42.1           mesa@8.0.5         qt@5.4.0
   graphlib@2.0.0        mpich@3.0.4        readline@6.3
   gtkplus@2.24.25       mpileaks@1.0       sqlite@3.8.5
   harfbuzz@0.9.37       mrnet@4.1.0        stat@2.1.0
   hdf5@1.8.13           ncurses@5.9        tcl@8.6.3
   icu@54.1              netcdf@4.3.3       tk@src
   jpeg@9a               openssl@1.0.1h     vtk@6.1.0
   launchmon@1.0.1       pango@1.36.8       xcb-proto@1.11
   lcms@2.6              pixman@0.32.6      xz@5.2.0
   libdrm@2.4.33         py-dateutil@2.4.0  zlib@1.2.8

   -- linux-debian7-x86_64 / gcc@4.9.2 --------------------------------
   libelf@0.8.10  mpich@3.0.4

Packages are divided into groups according to their architecture and compiler.
Within each group, Spack tries to keep the view simple and only shows the version of installed packages.

.. _cmd-spack-find-metadata:

Viewing more metadata
""""""""""""""""""""""""""""""""

``spack find`` can filter the package list based on the package name, spec, or a number of properties of their installation status.
For example, missing dependencies of a spec can be shown with ``--missing``, deprecated packages can be included with ``--deprecated``, packages that were explicitly installed with ``spack install <package>`` can be singled out with ``--explicit``, and those that have been pulled in only as dependencies with ``--implicit``.

In some cases, there may be different configurations of the *same* version of a package installed.
For example, there are two installations of ``libdwarf@20130729`` above.
We can look at them in more detail using ``spack find --deps`` and by asking only to show ``libdwarf`` packages:

.. code-block:: spec

   $ spack find --deps libdwarf
   ==> 2 installed packages.
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
       libdwarf@20130729-d9b90962
           ^libelf@0.8.12
       libdwarf@20130729-b52fac98
           ^libelf@0.8.13

Now we see that the two instances of ``libdwarf`` depend on *different* versions of ``libelf``: 0.8.12 and 0.8.13.
This view can become complicated for packages with many dependencies.
If you just want to know whether two packages' dependencies differ, you can use ``spack find --long``:

.. code-block:: spec

   $ spack find --long libdwarf
   ==> 2 installed packages.
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
   libdwarf@20130729-d9b90962  libdwarf@20130729-b52fac98

Now the ``libdwarf`` installs have hashes after their names.
These are hashes over all of the dependencies of each package.
If the hashes are the same, then the packages have the same dependency configuration.

If you want to know the path where each package is installed, you can use ``spack find --paths``:

.. code-block:: spec

   $ spack find --paths
   ==> 74 installed packages.
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
       ImageMagick@6.8.9-10  ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/ImageMagick@6.8.9-10-4df950dd
       adept-utils@1.0       ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/adept-utils@1.0-5adef8da
       atk@2.14.0            ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/atk@2.14.0-3d09ac09
       boost@1.55.0          ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/boost@1.55.0
       bzip2@1.0.6           ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/bzip2@1.0.6
       cairo@1.14.0          ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/cairo@1.14.0-fcc2ab44
       callpath@1.0.2        ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/callpath@1.0.2-5dce4318
   ...

You can restrict your search to a particular package by supplying its name:

.. code-block:: spec

   $ spack find --paths libelf
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
       libelf@0.8.11  ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/libelf@0.8.11
       libelf@0.8.12  ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/libelf@0.8.12
       libelf@0.8.13  ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/libelf@0.8.13

Spec queries
""""""""""""""""""""""""""""""""

``spack find`` actually does a lot more than this.
You can use *specs* to query for specific configurations and builds of each package.
If you want to find only libelf versions greater than version 0.8.12, you could say:

.. code-block:: spec

   $ spack find libelf@0.8.12:
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
       libelf@0.8.12  libelf@0.8.13

Finding just the versions of libdwarf built with a particular version of libelf would look like this:

.. code-block:: spec

   $ spack find --long libdwarf ^libelf@0.8.12
   ==> 1 installed packages.
   -- linux-debian7-x86_64 / gcc@4.4.7 --------------------------------
   libdwarf@20130729-d9b90962

We can also search for packages that have a certain attribute.
For example, ``spack find libdwarf +debug`` will show only installations of libdwarf with the 'debug' compile-time option enabled.

The full spec syntax is discussed in detail in :ref:`sec-specs`.


Machine-readable output
""""""""""""""""""""""""""""""""

If you only want to see very specific things about installed packages, Spack has some options for you.
``spack find --format`` can be used to output only specific fields:

.. code-block:: console

   $ spack find --format "{name}-{version}-{hash}"
   autoconf-2.69-icynozk7ti6h4ezzgonqe6jgw5f3ulx4
   automake-1.16.1-o5v3tc77kesgonxjbmeqlwfmb5qzj7zy
   bzip2-1.0.6-syohzw57v2jfag5du2x4bowziw3m5p67
   bzip2-1.0.8-zjny4jwfyvzbx6vii3uuekoxmtu6eyuj
   cmake-3.15.1-7cf6onn52gywnddbmgp7qkil4hdoxpcb
   ...

or:

.. code-block:: console

   $ spack find --format "{hash:7}"
   icynozk
   o5v3tc7
   syohzw5
   zjny4jw
   7cf6onn
   ...

This uses the same syntax as described in the documentation for :meth:`~spack.spec.Spec.format` -- you can use any of the options there.
This is useful for passing metadata about packages to other command-line tools.

Alternatively, if you want something even more machine readable, you can output each spec as JSON records using ``spack find --json``.
This will output metadata on specs and all dependencies as JSON:

.. code-block:: spec

    $ spack find --json sqlite@3.28.0
    [
     {
      "name": "sqlite",
      "hash": "3ws7bsihwbn44ghf6ep4s6h4y2o6eznv",
      "version": "3.28.0",
      "arch": {
       "platform": "darwin",
       "platform_os": "mojave",
       "target": "x86_64"
      },
      "compiler": {
       "name": "apple-clang",
       "version": "10.0.0"
      },
      "namespace": "builtin",
      "parameters": {
       "fts": true,
       "functions": false,
       "cflags": [],
       "cppflags": [],
       "cxxflags": [],
       "fflags": [],
       "ldflags": [],
       "ldlibs": []
      },
      "dependencies": {
       "readline": {
        "hash": "722dzmgymxyxd6ovjvh4742kcetkqtfs",
        "type": [
         "build",
         "link"
        ]
       }
      }
     },
     ...
    ]

You can use this with tools like `jq <https://stedolan.github.io/jq/>`_ to quickly create JSON records structured the way you want:

.. code-block:: console

    $ spack find --json sqlite@3.28.0 | jq -C '.[] | { name, version, hash }'
    {
      "name": "sqlite",
      "version": "3.28.0",
      "hash": "3ws7bsihwbn44ghf6ep4s6h4y2o6eznv"
    }
    {
      "name": "readline",
      "version": "7.0",
      "hash": "722dzmgymxyxd6ovjvh4742kcetkqtfs"
    }
    {
      "name": "ncurses",
      "version": "6.1",
      "hash": "zvaa4lhlhilypw5quj3akyd3apbq5gap"
    }


``spack diff``
^^^^^^^^^^^^^^

It's often the case that you have two versions of a spec that you need to disambiguate.
Let's say that we've installed two variants of zlib, one with and one without the optimize variant:

.. code-block:: spec

   $ spack install zlib
   $ spack install zlib -optimize

When we do ``spack find``, we see the two versions.

.. code-block:: spec

    $ spack find zlib
    ==> 2 installed packages
    -- linux-ubuntu20.04-skylake / gcc@9.3.0 ------------------------
    zlib@1.2.11  zlib@1.2.11


Let's say we want to uninstall ``zlib``.
We run the command and quickly encounter a problem because two versions are installed.

.. code-block:: spec

    $ spack uninstall zlib
    ==> Error: zlib matches multiple packages:

        -- linux-ubuntu20.04-skylake / gcc@9.3.0 ------------------------
        efzjziy zlib@1.2.11  sl7m27m zlib@1.2.11

    ==> Error: You can either:
        a) use a more specific spec, or
        b) specify the spec by its hash (e.g. `spack uninstall /hash`), or
        c) use `spack uninstall --all` to uninstall ALL matching specs.

Oh no!
We can see from the above that we have two different versions of zlib installed, and the only difference between the two is the hash.
This is a good use case for ``spack diff``, which can easily show us the "diff" or set difference between properties for two packages.
Let's try it out.
Because the only difference we see in the ``spack find`` view is the hash, let's use ``spack diff`` to look for more detail.
We will provide the two hashes:

.. code-block:: diff

    $ spack diff /efzjziy /sl7m27m

    --- zlib@1.2.11efzjziyc3dmb5h5u5azsthgbgog5mj7g
    +++ zlib@1.2.11sl7m27mzkbejtkrajigj3a3m37ygv4u2
    @@ variant_value @@
    -  zlib optimize False
    +  zlib optimize True


The output is colored and written in the style of a git diff.
This means that you can copy and paste it into a GitHub markdown as a code block with language "diff" and it will render nicely!
Here is an example:

.. code-block:: diff

    --- zlib@1.2.11/efzjziyc3dmb5h5u5azsthgbgog5mj7g
    +++ zlib@1.2.11/sl7m27mzkbejtkrajigj3a3m37ygv4u2
    @@ variant_value @@
    -  zlib optimize False
    +  zlib optimize True

Awesome!
Now let's read the diff.
It tells us that our first zlib was built with ``~optimize`` (``False``) and the second was built with ``+optimize`` (``True``).
You can't see it in the docs here, but the output above is also colored based on the content being an addition (+) or subtraction (-).

This is a small example, but you will be able to see differences for any attributes on the installation spec.
Running ``spack diff A B`` means we'll see which spec attributes are on ``B`` but not on ``A`` (green) and which are on ``A`` but not on ``B`` (red).
Here is another example with an additional difference type, ``version``:

.. code-block:: diff

   $ spack diff python@2.7.8 python@3.8.11

   --- python@2.7.8/tsxdi6gl4lihp25qrm4d6nys3nypufbf
   +++ python@3.8.11/yjtseru4nbpllbaxb46q7wfkyxbuvzxx
   @@ variant_value @@
   -  python patches a8c52415a8b03c0e5f28b5d52ae498f7a7e602007db2b9554df28cd5685839b8
   +  python patches 0d98e93189bc278fbc37a50ed7f183bd8aaf249a8e1670a465f0db6bb4f8cf87
   @@ version @@
   -  openssl 1.0.2u
   +  openssl 1.1.1k
   -  python 2.7.8
   +  python 3.8.11

Let's say that we were only interested in one kind of attribute above, ``version``.
We can ask the command to only output this attribute.
To do this, you'd add the ``--attribute`` for attribute parameter, which defaults to all.
Here is how you would filter to show just versions:

.. code-block:: diff

    $ spack diff --attribute version python@2.7.8 python@3.8.11

    --- python@2.7.8/tsxdi6gl4lihp25qrm4d6nys3nypufbf
    +++ python@3.8.11/yjtseru4nbpllbaxb46q7wfkyxbuvzxx
    @@ version @@
    -  openssl 1.0.2u
    +  openssl 1.1.1k
    -  python 2.7.8
    +  python 3.8.11

And you can add as many attributes as you'd like with multiple `--attribute` arguments (for lots of attributes, you can use ``-a`` for short).
Finally, if you want to view the data as JSON (and possibly pipe into an output file), just add ``--json``:


.. code-block:: spec

    $ spack diff --json python@2.7.8 python@3.8.11


This data will be much longer because along with the differences for ``A`` vs.
``B`` and ``B`` vs.
``A``, the JSON output also shows the intersection.


Using Installed Packages
------------------------

As you've seen, Spack packages are installed into long paths with hashes, and you need a way to get them into your path.
Spack has three different ways to solve this problem, which fit different use cases:

1. Spack provides :ref:`environments <environments>`, and views, with which you can "activate" a number of related packages all at once.
   This is likely the best method for most use cases.
2. Spack can generate :ref:`environment modules <modules>`, which are commonly used on supercomputing clusters.
   Module files can be generated for every installation automatically, and you can customize how this is done.
3. For one-off use, Spack provides the :ref:`spack load <cmd-spack-load>` command


.. _cmd-spack-load:

``spack load / unload``
^^^^^^^^^^^^^^^^^^^^^^^

If you sourced the appropriate shell script, as shown in :ref:`getting_started`, you can use the ``spack load`` command to quickly add a package to your ``PATH``.

For example, this will add the ``mpich`` package built with ``gcc`` to your path:

.. code-block:: spec

   $ spack install mpich %gcc@4.4.7

   # ... wait for install ...

   $ spack load mpich %gcc@4.4.7
   $ which mpicc
   ~/spack/opt/linux-debian7-x86_64/gcc@4.4.7/mpich@3.0.4/bin/mpicc

These commands will add appropriate directories to your ``PATH`` and ``MANPATH`` according to the :ref:`prefix inspections <customize-env-modifications>` defined in your modules configuration.
When you no longer want to use a package, you can type unload or unuse similarly:

.. code-block:: spec

   $ spack unload mpich %gcc@4.4.7


Ambiguous specs
"""""""""""""""

If a spec used with load/unload is ambiguous (i.e., more than one installed package matches it), then Spack will warn you:

.. code-block:: spec

   $ spack load libelf
   ==> Error: libelf matches multiple packages.
   Matching packages:
     qmm4kso libelf@0.8.13%gcc@4.4.7 arch=linux-debian7-x86_64
     cd2u6jt libelf@0.8.13%intel@15.0.0 arch=linux-debian7-x86_64
   Use a more specific spec

You can either type the ``spack load`` command again with a fully qualified argument, or you can add just enough extra constraints to identify one package.
For example, above, the key differentiator is that one ``libelf`` is built with the Intel compiler, while the other used ``gcc``.
You could therefore just type:

.. code-block:: spec

   $ spack load libelf %intel

To identify just the one built with the Intel compiler.
If you want to be *very* specific, you can load it by its hash.
For example, to load the first ``libelf`` above, you would run:

.. code-block:: spec

   $ spack load /qmm4kso

To see which packages that you have loaded into your environment, you would use ``spack find --loaded``.

.. code-block:: console

    $ spack find --loaded
    ==> 2 installed packages
    -- linux-debian7 / gcc@4.4.7 ------------------------------------
    libelf@0.8.13

    -- linux-debian7 / intel@15.0.0 ---------------------------------
    libelf@0.8.13

You can also use ``spack load --list`` to get the same output, but it does not have the full set of query options that ``spack find`` offers.

We'll learn more about Spack's spec syntax in :ref:`a later section <sec-specs>`.

.. _extensions:

Spack environments
^^^^^^^^^^^^^^^^^^

Spack can install a large number of Python packages.
Their names are typically prefixed with ``py-``.
Installing and using them is no different from any other package:

.. code-block:: spec

   $ spack install py-numpy
   $ spack load py-numpy
   $ python3
   >>> import numpy

The ``spack load`` command sets the ``PATH`` variable so that the correct Python executable is used and makes sure that ``numpy`` and its dependencies can be located in the ``PYTHONPATH``.

Spack is different from other Python package managers in that it installs every package into its *own* prefix.
This is in contrast to ``pip``, which installs all packages into the same prefix, whether in a virtual environment or not.

For many users, **virtual environments** are more convenient than repeated ``spack load`` commands, particularly when working with multiple Python packages.
Fortunately, Spack supports environments itself, which together with a view are no different from Python virtual environments.

The recommended way of working with Python extensions such as ``py-numpy`` is through :ref:`Environments <environments>`.
The following example creates a Spack environment with ``numpy`` in the current working directory.
It also puts a filesystem view in ``./view``, which is a more traditional combined prefix for all packages in the environment.

.. code-block:: spec

   $ spack env create --with-view view --dir .
   $ spack -e . add py-numpy
   $ spack -e . concretize
   $ spack -e . install

Now you can activate the environment and start using the packages:

.. code-block:: console

   $ spack env activate .
   $ python3
   >>> import numpy

The environment view is also a virtual environment, which is useful if you are sharing the environment with others who are unfamiliar with Spack.
They can either use the Python executable directly:

.. code-block:: console

   $ ./view/bin/python3
   >>> import numpy

or use the activation script:

.. code-block:: console

   $ source ./view/bin/activate
   $ python3
   >>> import numpy

In general, there should not be much difference between ``spack env activate`` and using the virtual environment.
The main advantage of ``spack env activate`` is that it knows about more packages than just Python packages, and it may set additional runtime variables that are not covered by the virtual environment activation script.

See :ref:`environments` for a more in-depth description of Spack environments and customizations to views.
