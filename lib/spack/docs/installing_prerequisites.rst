..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Find instructions on how to install the necessary prerequisites for Spack on various operating systems, including Linux and macOS.

.. _verify-spack-prerequisites:

Spack Prerequisites
===================

Spack relies on a few basic utilities to be present on the system where it runs, depending on the operating system.
To install them, follow the instructions below.

Linux
-----

For **Debian** and **Ubuntu** users:

.. code-block:: console

   $ apt update
   $ apt install file bzip2 ca-certificates g++ gcc gfortran git gzip lsb-release patch python3 tar unzip xz-utils zstd

For **RHEL**, **AlmaLinux**, and **Rocky Linux** users:

.. code-block:: console

   $ dnf install epel-release
   $ dnf install file bzip2 ca-certificates git gzip patch python3 tar unzip xz zstd gcc gcc-c++ gcc-gfortran

macOS
-----

On macOS, the Command Line Tools package is required, and the full Xcode suite may be necessary for some packages, such as Qt and apple-gl.
To install Xcode, you can use the following command:

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

you already have the full Xcode suite installed.
If the output is:

.. code-block:: none

   /Library/Developer/CommandLineTools

you only have the command-line tools installed.
The full Xcode suite can be installed through the App Store.
Make sure to launch the Xcode application and accept the license agreement before using Spack.
It may ask you to install additional components.
Alternatively, the Xcode license can be accepted through the command line:

.. code-block:: console

   $ sudo xcodebuild -license accept

Fortran
^^^^^^^

Xcode provides the Apple Clang compilers, which support C and C++ but not Fortran.
Many scientific packages, or their dependencies (for example MPI implementations), need a Fortran compiler.
If you need one, you have two options.

You can have Spack build a compiler for you:

.. code-block:: console

   $ spack install gcc

Alternatively, you can install ``gfortran`` from another package manager, after which Spack will detect it as an external compiler:

.. code-block:: console

   $ brew install gcc
   $ spack compiler find

Once a Fortran compiler is available, Spack will use it automatically for packages that require Fortran.

.. note::

   Spack will not build a compiler on the fly to satisfy a Fortran dependency.
   A compiler providing Fortran must already be installed or detected as external before concretizing such packages.
