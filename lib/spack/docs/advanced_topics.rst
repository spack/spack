.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Explore advanced topics in Spack, including auditing packages and configuration, and verifying installations.

.. _audit-packages-and-configuration:

Auditing Packages and Configuration
===================================

The ``spack audit`` command detects potential issues with configuration and packages:

.. command-output:: spack audit -h

For instance, it can detect duplicate external specs in ``packages.yaml``, or the use of non-existing variants in directives.
A detailed list of the checks currently implemented for each subcommand can be printed with:

.. command-output:: spack -v audit list

Depending on the use case, users can run the appropriate subcommands to obtain diagnostics.
If issues are found, they are reported to stdout:

.. code-block:: console

   % spack audit packages lammps
   PKG-DIRECTIVES: 1 issue found
   1. lammps: wrong variant in "conflicts" directive
       the variant 'adios' does not exist
       in spack_repo/builtin/packages/lammps/package.py

.. _verify-installations:

Verifying Installations
=======================

The ``spack verify`` command can be used to verify the validity of Spack-installed packages any time after installation.


``spack verify manifest``
-------------------------

At installation time, Spack creates a manifest of every file in the installation prefix.
For links, Spack tracks the mode, ownership, and destination.
For directories, Spack tracks the mode and ownership.
For files, Spack tracks the mode, ownership, modification time, hash, and size.
The ``spack verify manifest`` command will check, for every file in each package, whether any of those attributes have changed.
It will also check for newly added files or deleted files from the installation prefix.
Spack can either check all installed packages using the ``-a,--all`` option or accept specs listed on the command line to verify.

The ``spack verify manifest`` command can also verify that individual files haven't been altered since installation time.
If the given file is not in a Spack installation prefix, Spack will report that it is not owned by any package.
To check individual files instead of specs, use the ``-f,--files`` option.

Spack installation manifests are included in the tarball signed by Spack for binary package distribution.
When installed from a binary package, Spack uses the packaged installation manifest instead of creating one at install time.

The ``spack verify`` command also accepts the ``-l,--local`` option to check only local packages (as opposed to those used transparently from ``upstream`` Spack instances) and the ``-j,--json`` option to output machine-readable JSON data for any errors.

``spack verify libraries``
--------------------------

The ``spack verify libraries`` command can be used to verify that packages do not have accidental system dependencies.
This command scans the install prefixes of packages for executables and shared libraries, and resolves their needed libraries in their RPATHs.
When needed libraries cannot be located, an error is reported.
This typically indicates that a package was linked against a system library instead of a library provided by a Spack package.

This verification can also be enabled as a post-install hook by setting ``config:shared_linking:missing_library_policy`` to ``error`` or ``warn`` in :ref:`config.yaml <config-yaml>`.

Filesystem Requirements
=======================

By default, Spack needs to be run from a filesystem that supports ``flock`` locking semantics.
Nearly all local filesystems and recent versions of NFS support this, but parallel filesystems or NFS volumes may be configured without ``flock`` support enabled.
You can determine how your filesystems are mounted with ``mount``.
The output for a Lustre filesystem might look like this:

.. code-block:: console

   $ mount | grep lscratch
   mds1-lnet0@o2ib100:/lsd on /p/lscratchd type lustre (rw,nosuid,lazystatfs,flock)
   mds2-lnet0@o2ib100:/lse on /p/lscratche type lustre (rw,nosuid,lazystatfs,flock)

Note the ``flock`` option on both Lustre mounts.

If you do not see this or a similar option for your filesystem, you have a few options.
First, you can move your Spack installation to a filesystem that supports locking.
Second, you could ask your system administrator to enable ``flock`` for your filesystem.

If none of those work, you can disable locking in one of two ways:

1. Run Spack with the ``-L`` or ``--disable-locks`` option to disable locks on a call-by-call basis.
2. Edit :ref:`config.yaml <config-yaml>` and set the ``locks`` option to ``false`` to always disable locking.

.. warning::

   If you disable locking, concurrent instances of Spack will have no way to avoid stepping on each other.
   You must ensure that there is only **one** instance of Spack running at a time.
   Otherwise, Spack may end up with a corrupted database, or you may not be able to see all installed packages when running commands like ``spack find``.

   If you are unfortunate enough to run into this situation, you may be able to fix it by running ``spack reindex``.

This issue typically manifests with the error below:

.. code-block:: console

   $ ./spack find
   Traceback (most recent call last):
   File "./spack", line 176, in <module>
     main()
   File "./spack", line 154, in main
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
