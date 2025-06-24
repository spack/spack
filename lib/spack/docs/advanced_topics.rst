.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _advanced-topics:

===============
Advanced Topics
===============


.. _verify-spack-prerequisites:

--------------------------
Verify Spack prerequisites
--------------------------

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

--------------------------
Fortran compilers on macOS
--------------------------

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


-----------------------------
Deprecating Insecure Packages
-----------------------------

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

-----------------------
Verifying Installations
-----------------------

The ``spack verify`` command can be used to verify the validity of
Spack-installed packages any time after installation.


^^^^^^^^^^^^^^^^^^^^^^^^^
``spack verify manifest``
^^^^^^^^^^^^^^^^^^^^^^^^^

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

^^^^^^^^^^^^^^^^^^^^^^^^^^
``spack verify libraries``
^^^^^^^^^^^^^^^^^^^^^^^^^^

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

