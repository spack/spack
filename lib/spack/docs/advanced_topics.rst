.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _verify-spack-prerequisites:

==========================
Verify Spack prerequisites
==========================

To verify if Spack prerequisites are met on your system, you can use the following command:

.. code-block:: console

   $ spack bootstrap status --optional

If Spack is ready to be used, with all of its features, the output will show only ``[PASS]`` tests, and the exit code of the command will be ``0``.

When a prerequisite is missing, Spack shows which test failed, and the exit code of the command will be  ``1``.
For instance, if you started from a clean checkout of Spack, it's likely you see an output similar to:

.. code-block:: console

   $ spack bootstrap status --optional
   Spack v1.0.0.dev0 - python@3.13

   [FAIL] Core Functionalities
     [B] MISSING "clingo": required to concretize specs

   [PASS] Binary packages

   [PASS] Optional Features


   Spack will take care of bootstrapping any missing dependency marked as [B]. Dependencies marked as [-] are instead required to be found on the system.

Bootstrappable dependencies can be installed explicitly, with the following command:

.. code-block:: console

   $ spack bootstrap now

Alternatively, Spack will try to bootstrap them lazily, the first time they are needed.

.. admonition:: Installing prerequisites system-wide on Linux
   :class: tip
   :collapsible:

   Spack's requirements can be easily installed on most modern Linux systems
   A build matrix showing which packages are working on which systems is shown below.

   .. tab-set::

      .. tab-item:: Debian/Ubuntu

         .. code-block:: console

            apt update
            apt install bzip2 ca-certificates g++ gcc gfortran git gzip lsb-release patch python3 tar unzip xz-utils zstd

      .. tab-item:: RHEL

         .. code-block:: console

            dnf install epel-release
            dnf group install "Development Tools"
            dnf install gcc-gfortran redhat-lsb-core python3 unzip

.. admonition:: Installing prerequisites on macOS
   :class: tip
   :collapsible:

   On macOS, the Command Line Tools package is required, and a full Xcode suite may be necessary for some packages such as Qt and apple-gl.


.. _mixed-toolchains:

==========================
Fortran compilers on macOS
==========================

Modern compilers typically come with related compilers for C, C++ and
Fortran bundled together.  When possible, results are best if the same
compiler is used for all languages.

In some cases, this is not possible.  For example, Xcode on macOS provides no Fortran compilers.
The user is therefore forced to use a mixed toolchain: Xcode-provided Clang for C/C++ and e.g.
GNU ``gfortran`` for Fortran.

#. You need to make sure that Xcode is installed. Run the following command:

   .. code-block:: console

      $ xcode-select --install


   If the Xcode command-line tools are already installed, you will see an
   error message:

   .. code-block:: none

      xcode-select: error: command line tools are already installed, use "Software Update" to install updates


#. For most packages, the Xcode command-line tools are sufficient. However,
   some packages like ``qt`` require the full Xcode suite. You can check
   to see which you have installed by running:

   .. code-block:: console

      $ xcode-select -p


   If the output is:

   .. code-block:: none

      /Applications/Xcode.app/Contents/Developer


   you already have the full Xcode suite installed. If the output is:

   .. code-block:: none

      /Library/Developer/CommandLineTools


   you only have the command-line tools installed. The full Xcode suite can
   be installed through the App Store. Make sure you launch the Xcode
   application and accept the license agreement before using Spack.
   It may ask you to install additional components. Alternatively, the license
   can be accepted through the command line:

   .. code-block:: console

      $ sudo xcodebuild -license accept


   Note: the flag is ``-license``, not ``--license``.

#. There are different ways to get ``gfortran`` on macOS. For example, you can
   install GCC with Spack (``spack install gcc``), with Homebrew (``brew install
   gcc``), or from a `DMG installer
   <https://github.com/fxcoudert/gfortran-for-macOS/releases>`_.

#. Run ``spack compiler find`` to locate both Apple-Clang and GCC.

Since languages in Spack are modeled as virtual packages, ``apple-clang`` will be used to provide
C and C++, while GCC will be used for Fortran.


=============================
Deprecating Insecure Packages
=============================

``spack deprecate`` allows for the removal of insecure packages with
minimal impact to their dependents.

.. warning::

  The ``spack deprecate`` command is designed for use only in
  extraordinary circumstances. This is a VERY big hammer to be used
  with care.

The ``spack deprecate`` command will remove one package and replace it
with another by replacing the deprecated package's prefix with a link
to the deprecator package's prefix.

.. warning::

  The ``spack deprecate`` command makes no promises about binary
  compatibility. It is up to the user to ensure the deprecator is
  suitable for the deprecated package.

Spack tracks concrete deprecated specs and ensures that no future packages
concretize to a deprecated spec.

The first spec given to the ``spack deprecate`` command is the package
to deprecate. It is an abstract spec that must describe a single
installed package. The second spec argument is the deprecator
spec. By default it must be an abstract spec that describes a single
installed package, but with the ``-i/--install-deprecator`` it can be
any abstract spec that Spack will install and then use as the
deprecator. The ``-I/--no-install-deprecator`` option will ensure
the default behavior.

By default, ``spack deprecate`` will deprecate all dependencies of the
deprecated spec, replacing each by the dependency of the same name in
the deprecator spec. The ``-d/--dependencies`` option will ensure the
default, while the ``-D/--no-dependencies`` option will deprecate only
the root of the deprecate spec in favor of the root of the deprecator
spec.

``spack deprecate`` can use symbolic links or hard links. The default
behavior is symbolic links, but the ``-l/--link-type`` flag can take
options ``hard`` or ``soft``.

=======================
Verifying Installations
=======================

The ``spack verify`` command can be used to verify the validity of
Spack-installed packages any time after installation.


-------------------------
``spack verify manifest``
-------------------------

At installation time, Spack creates a manifest of every file in the
installation prefix. For links, Spack tracks the mode, ownership, and
destination. For directories, Spack tracks the mode and
ownership. For files, Spack tracks the mode, ownership, modification
time, hash, and size. The ``spack verify manifest`` command will check,
for every file in each package, whether any of those attributes have
changed. It will also check for newly added files or deleted files from
the installation prefix. Spack can either check all installed packages
using the ``-a,--all`` option or accept specs listed on the command line to
verify.

The ``spack verify manifest`` command can also verify for individual files
that they haven't been altered since installation time. If the given file
is not in a Spack installation prefix, Spack will report that it is
not owned by any package. To check individual files instead of specs,
use the ``-f,--files`` option.

Spack installation manifests are part of the tarball signed by Spack
for binary package distribution. When installed from a binary package,
Spack uses the packaged installation manifest instead of creating one
at install time.

The ``spack verify`` command also accepts the ``-l,--local`` option to
check only local packages (as opposed to those used transparently from
``upstream`` Spack instances) and the ``-j,--json`` option to output
machine-readable JSON data for any errors.

--------------------------
``spack verify libraries``
--------------------------

The ``spack verify libraries`` command can be used to verify that packages
do not have accidental system dependencies. This command scans the install
prefixes of packages for executables and shared libraries, and resolves
their needed libraries in their RPATHs. When needed libraries cannot be
located, an error is reported. This typically indicates that a package
was linked against a system library instead of a library provided by
a Spack package.

This verification can also be enabled as a post-install hook by setting
``config:shared_linking:missing_library_policy`` to ``error`` or ``warn``
in :ref:`config.yaml <config-yaml>`.


.. _toolchains:

==========
Toolchains
==========

Spack can be configured to associate certain combinations of specs for
easy reference on the command line and in config and environment
files. These combinations are called ``toolchains``, because their
primary intended use is for associating compiler combinations to
apply. Toolchains are referenced by name like a direct dependency,
using the ``%`` sigil. There are two styles of toolchain config, one
using conditional dependencies through the spec syntax and one with
conditionals explicitly in the yaml:

.. code-block:: yaml

   toolchains:
     gcc_all: cflags=-O3 '%[when=%c virtuals=c]gcc %[when=%cxx virtuals=cxx]gcc %[when=%fortran virtuals=fortran]gcc'
     llvm_gfortran:
     - spec: cflags=-O3
     - spec: '%[virtuals=c]llvm'
       when: '%c'
     - spec: '%[virtuals=cxx]llvm'
       when: '%cxx'
     - spec: '%[virtuals=fortran]gcc'
       when: '%fortran'

The two syntaxes are equivalent. It is not necessary to use
conditional dependencies with toolchains, but in most cases it his
highly recommended. Similarly, while any spec constraint can be
included, it is most useful to use compiler flags, architectures, and
conditional dependencies. With the above config, the ``gcc_all``
toolchain imposes conditional dependencies such that gcc is used as
the provider for ``c``, ``cxx``, and ``fortran`` for any package using
that toolchain that depends on each language. The conditional
dependencies allow the toolchain to be applied to any package
regardless of which languages it depends on. The ``llvm_gfortran``
toolchain is the same, except it uses ``llvm`` for ``c`` and ``cxx``
and ``gcc`` for ``fortran``.

These two toolchains could be used independently or even in the same
spec, e.g. ``spack install hdf5+fortran%llvm_gfortran ^mpich
%gcc_all``. This will install an hdf5 compiled with ``llvm`` for the
C/C++ components, but with the fortran components compiled with
``gfortran``, but will build it against an MPICH installation compiled
entirely with ``gcc`` for C, C++, and Fortran.

.. note::

   Toolchains are currently limited to exclude non-direct dependencies
   (using the ``^`` syntax).

=======================
Filesystem Requirements
=======================

By default, Spack needs to be run from a filesystem that supports
``flock`` locking semantics. Nearly all local filesystems and recent
versions of NFS support this, but parallel filesystems or NFS volumes may
be configured without ``flock`` support enabled. You can determine how
your filesystems are mounted with ``mount``. The output for a Lustre
filesystem might look like this:

.. code-block:: console

   $ mount | grep lscratch
   mds1-lnet0@o2ib100:/lsd on /p/lscratchd type lustre (rw,nosuid,lazystatfs,flock)
   mds2-lnet0@o2ib100:/lse on /p/lscratche type lustre (rw,nosuid,lazystatfs,flock)

Note the ``flock`` option on both Lustre mounts.

If you do not see this or a similar option for your filesystem, you have
a few options. First, you can move your Spack installation to a
filesystem that supports locking. Second, you could ask your system
administrator to enable ``flock`` for your filesystem.

If none of those work, you can disable locking in one of two ways:

  1. Run Spack with the ``-L`` or ``--disable-locks`` option to disable
     locks on a call-by-call basis.
  2. Edit :ref:`config.yaml <config-yaml>` and set the ``locks`` option
     to ``false`` to always disable locking.

.. warning::

   If you disable locking, concurrent instances of Spack will have no way
   to avoid stepping on each other. You must ensure that there is only
   **one** instance of Spack running at a time. Otherwise, Spack may end
   up with a corrupted database file, or you may not be able to see all
   installed packages in commands like ``spack find``.

   If you are unfortunate enough to run into this situation, you may be
   able to fix it by running ``spack reindex``.

This issue typically manifests with the error below:

.. code-block:: console

   $ ./spack find
   Traceback (most recent call last):
   File "./spack", line 176, in <module>
     main()
   File "./spack", line 154,' in main
     return_val = command(parser, args)
   File "./spack/lib/spack/spack/cmd/find.py", line 170, in find
     specs = set(spack.installed_db.query(\**q_args))
   File "./spack/lib/spack/spack/database.py", line 551, in query
     with self.read_transaction():
   File "./spack/lib/spack/spack/database.py", line 598, in __enter__
     if self._enter() and self._acquire_fn:
   File "./spack/lib/spack/spack/database.py", line 608, in _enter
     return self._db.lock.acquire_read(self._timeout)
   File "./spack/lib/spack/llnl/util/lock.py", line 103, in acquire_read
     self._lock(fcntl.LOCK_SH, timeout)   # can raise LockError.
   File "./spack/lib/spack/llnl/util/lock.py", line 64, in _lock
     fcntl.lockf(self._fd, op | fcntl.LOCK_NB)
   IOError: [Errno 38] Function not implemented

A nicer error message is to be determined in future versions of Spack.

===============
Troubleshooting
===============

The ``spack audit`` command:

.. command-output:: spack audit -h

can be used to detect a number of configuration issues. This command detects
configuration settings that might not be strictly wrong but are not likely
to be useful outside of special cases.

It can also be used to detect dependency issues with packages -- for example,
cases where a package constrains a dependency with a variant that doesn't
exist (in this case, Spack could report the problem ahead of time, but
automatically performing the check would slow down most runs of Spack).

A detailed list of the checks currently implemented for each subcommand can be
printed with:

.. command-output:: spack -v audit list

Depending on the use case, users might run the appropriate subcommands to obtain
diagnostics. Issues, if found, are reported to stdout:

.. code-block:: console

   % spack audit packages lammps
   PKG-DIRECTIVES: 1 issue found
   1. lammps: wrong variant in "conflicts" directive
       the variant 'adios' does not exist
       in spack_repo/builtin/packages/lammps/package.py
