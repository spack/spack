.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _verify-spack-prerequisites:

==============================
Installing Spack prerequisites
==============================

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

.. admonition:: Installing system prerequisites on Linux
   :class: tip
   :collapsible:

   Spack's requirements can be easily installed on most modern Linux systems.
   A build matrix showing which packages are working on which systems is shown below.

   .. tab-set::

      .. tab-item:: Debian/Ubuntu

         .. code-block:: console

            sudo apt update
            sudo apt install bzip2 ca-certificates g++ gcc gfortran git gzip lsb-release patch python3 tar unzip xz-utils zstd

      .. tab-item:: RHEL

         .. code-block:: console

            dnf install epel-release
            dnf group install "Development Tools"
            dnf install gcc-gfortran redhat-lsb-core python3 unzip

.. admonition:: Installing system prerequisites on macOS
   :class: tip
   :collapsible:

   On macOS, the Command Line Tools package is required, and a full Xcode suite may be necessary for some packages such as Qt and apple-gl.
   To install Xcode you can use the following command:

   .. code-block:: console

      $ xcode-select --install

   For most packages, the Xcode command-line tools are sufficient.
   However, some packages like ``qt`` require the full Xcode suite.
   You can check to see which you have installed by running:

   .. code-block:: console

      $ xcode-select -p

   If the output is:

   .. code-block:: none

      /Applications/Xcode.app/Contents/Developer

   you already have the full Xcode suite installed. If the output is:

   .. code-block:: none

      /Library/Developer/CommandLineTools

   you only have the command-line tools installed.
   The full Xcode suite can be installed through the App Store.
   Make sure you launch the Xcode application and accept the license agreement before using Spack.
   It may ask you to install additional components.
   Alternatively, the license can be accepted through the command line:

   .. code-block:: console

      $ sudo xcodebuild -license accept

   To get a Fortran compiler, in case you need it, you can ask spack to compile one for you:

   .. code-block:: console

      $ spack install gcc@14 languages:=c,cxx,fortran


