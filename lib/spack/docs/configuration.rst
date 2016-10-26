.. _configuration:

=============
Configuration
=============

.. _temp-space:

---------------
Temporary space
---------------

.. warning::

   Temporary space configuration will eventually be moved to
   configuration files, but currently these settings are in
   ``lib/spack/spack/__init__.py``

By default, Spack will try to do all of its building in temporary
space.  There are two main reasons for this.  First, Spack is designed
to run out of a user's home directory, and on may systems the home
directory is network mounted and potentially not a very fast
filesystem.  We create build stages in a temporary directory to avoid
this.  Second, many systems impose quotas on home directories, and
``/tmp`` or similar directories often have more available space.  This
helps conserve space for installations in users' home directories.

You can customize temporary directories by editing
``lib/spack/spack/__init__.py``.  Specifically, find this part of the file:

.. code-block:: python

   # Whether to build in tmp space or directly in the stage_path.
   # If this is true, then spack will make stage directories in
   # a tmp filesystem, and it will symlink them into stage_path.
   use_tmp_stage = True

   # Locations to use for staging and building, in order of preference
   # Use a %u to add a username to the stage paths here, in case this
   # is a shared filesystem.  Spack will use the first of these paths
   # that it can create.
   tmp_dirs = ['/nfs/tmp2/%u/spack-stage',
               '/var/tmp/%u/spack-stage',
               '/tmp/%u/spack-stage']

The ``use_tmp_stage`` variable controls whether Spack builds
**directly** inside the ``var/spack/`` directory.  Normally, Spack
will try to find a temporary directory for a build, then it *symlinks*
that temporary directory into ``var/spack/`` so that you can keep
track of what temporary directories Spack is using.

The ``tmp_dirs`` variable is a list of paths Spack should search when
trying to find a temporary directory.  They can optionally contain a
``%u``, which will substitute the current user's name into the path.
The list is searched in order, and Spack will create a temporary stage
in the first directory it finds to which it has write access.  Add
more elements to the list to indicate where your own site's temporary
directory is.

.. _sec-external_packages:

-----------------
External Packages
-----------------

Spack can be configured to use externally-installed
packages rather than building its own packages. This may be desirable
if machines ship with system packages, such as a customized MPI
that should be used instead of Spack building its own MPI.

External packages are configured through the ``packages.yaml`` file found
in a Spack installation's ``etc/spack/`` or a user's ``~/.spack/``
directory. Here's an example of an external configuration:

.. code-block:: yaml

   packages:
     openmpi:
       paths:
         openmpi@1.4.3%gcc@4.4.7 arch=linux-x86_64-debian7: /opt/openmpi-1.4.3
         openmpi@1.4.3%gcc@4.4.7 arch=linux-x86_64-debian7+debug: /opt/openmpi-1.4.3-debug
         openmpi@1.6.5%intel@10.1 arch=linux-x86_64-debian7: /opt/openmpi-1.6.5-intel

This example lists three installations of OpenMPI, one built with gcc,
one built with gcc and debug information, and another built with Intel.
If Spack is asked to build a package that uses one of these MPIs as a
dependency, it will use the the pre-installed OpenMPI in
the given directory. Packages.yaml can also be used to specify modules

Each ``packages.yaml`` begins with a ``packages:`` token, followed
by a list of package names.  To specify externals, add a ``paths`` or ``modules``
token under the package name, which lists externals in a
``spec: /path`` or ``spec: module-name`` format.  Each spec should be as
well-defined as reasonably possible.  If a
package lacks a spec component, such as missing a compiler or
package version, then Spack will guess the missing component based
on its most-favored packages, and it may guess incorrectly.

Each package version and compilers listed in an external should
have entries in Spack's packages and compiler configuration, even
though the package and compiler may not every be built.

The packages configuration can tell Spack to use an external location
for certain package versions, but it does not restrict Spack to using
external packages.  In the above example, if an OpenMPI 1.8.4 became
available Spack may choose to start building and linking with that version
rather than continue using the pre-installed OpenMPI versions.

To prevent this, the ``packages.yaml`` configuration also allows packages
to be flagged as non-buildable.  The previous example could be modified to
be:

.. code-block:: yaml

   packages:
     openmpi:
       paths:
         openmpi@1.4.3%gcc@4.4.7 arch=linux-x86_64-debian7: /opt/openmpi-1.4.3
         openmpi@1.4.3%gcc@4.4.7 arch=linux-x86_64-debian7+debug: /opt/openmpi-1.4.3-debug
         openmpi@1.6.5%intel@10.1 arch=linux-x86_64-debian7: /opt/openmpi-1.6.5-intel
       buildable: False

The addition of the ``buildable`` flag tells Spack that it should never build
its own version of OpenMPI, and it will instead always rely on a pre-built
OpenMPI.  Similar to ``paths``, ``buildable`` is specified as a property under
a package name.

If an external module is specified as not buildable, then Spack will load the
external module into the build environment which can be used for linking.

The ``buildable`` does not need to be paired with external packages.
It could also be used alone to forbid packages that may be
buggy or otherwise undesirable.

.. _system-packages:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
False Paths for System Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, the externally-installed package one wishes to use with
Spack comes with the Operating System and is installed in a standard
place --- ``/usr``, for example.  Many other packages are there as
well.  If Spack adds it to build paths, then some packages might
pick up dependencies from ``/usr`` than the intended Spack version.

In order to avoid this problem, it is advisable to specify a fake path
in ``packages.yaml``, thereby preventing Spack from adding the real
path to compiler command lines.  This will work because compilers
normally search standard system paths, even if they are not on the
command line.  For example:

.. code-block:: yaml

    packages:
        # Recommended for security reasons
        # Do not install OpenSSL as non-root user.
        openssl:
            paths:
                openssl@system: /false/path
            version: [system]
            buildable: False


^^^^^^^^^^^^^^^^^^^^^^^^^^
Extracting System Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^

In some cases, using false paths for system packages will not work.
Some builds need to run binaries out of their dependencies, not just
access their libraries: the build needs to know the real location of
the system package.

In this case, one can create a Spack-like single-package tree by
creating symlinks to the files related to just that package.
Depending on the OS, it is possible to obtain a list of the files in a
single OS-installed package.  For example, on RedHat / Fedora:

.. code-block:: console

   $ repoquery --list openssl-devel
   ...
   /usr/lib/libcrypto.so
   /usr/lib/libssl.so
   /usr/lib/pkgconfig/libcrypto.pc
   /usr/lib/pkgconfig/libssl.pc
   /usr/lib/pkgconfig/openssl.pc
   ...

Spack currently does not provide an automated way to create a symlink
tree to these files.


.. _concretization-preferences:

--------------------------
Concretization Preferences
--------------------------

Spack can be configured to prefer certain compilers, package
versions, depends_on, and variants during concretization.
The preferred configuration can be controlled via the
``~/.spack/packages.yaml`` file for user configuations, or the
``etc/spack/packages.yaml`` site configuration.

Here's an example packages.yaml file that sets preferred packages:

.. code-block:: yaml

   packages:
     opencv:
       compiler: [gcc@4.9]
       variants: +debug
     gperftools:
       version: [2.2, 2.4, 2.3]
     all:
       compiler: [gcc@4.4.7, gcc@4.6:, intel, clang, pgi]
       providers:
         mpi: [mvapich, mpich, openmpi]

At a high level, this example is specifying how packages should be
concretized.  The opencv package should prefer using gcc 4.9 and
be built with debug options.  The gperftools package should prefer version
2.2 over 2.4.  Every package on the system should prefer mvapich for
its MPI and gcc 4.4.7 (except for opencv, which overrides this by preferring gcc 4.9).
These options are used to fill in implicit defaults.  Any of them can be overwritten
on the command line if explicitly requested.

Each packages.yaml file begins with the string ``packages:`` and
package names are specified on the next level. The special string ``all``
applies settings to each package. Underneath each package name is
one or more components: ``compiler``, ``variants``, ``version``,
or ``providers``.  Each component has an ordered list of spec
``constraints``, with earlier entries in the list being preferred over
later entries.

Sometimes a package installation may have constraints that forbid
the first concretization rule, in which case Spack will use the first
legal concretization rule.  Going back to the example, if a user
requests gperftools 2.3 or later, then Spack will install version 2.4
as the 2.4 version of gperftools is preferred over 2.3.

An explicit concretization rule in the preferred section will always
take preference over unlisted concretizations.  In the above example,
xlc isn't listed in the compiler list.  Every listed compiler from
gcc to pgi will thus be preferred over the xlc compiler.

The syntax for the ``provider`` section differs slightly from other
concretization rules.  A provider lists a value that packages may
``depend_on`` (e.g, mpi) and a list of rules for fulfilling that
dependency.
