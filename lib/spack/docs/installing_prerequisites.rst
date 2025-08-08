.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Find instructions on how to install the necessary prerequisites for Spack on various operating systems, including Linux and macOS.

.. _verify-spack-prerequisites:

Spack Prerequisites
===================

Spack relies on a few basic utilities to be present on the system where it runs, depending on the operating system.
To install them, follow the instructions below.

.. tab-set::

   .. tab-item:: Linux

      .. tab-set::

         .. tab-item:: Debian/Ubuntu

            .. code-block:: console

               $ apt update
               $ apt install file bzip2 ca-certificates g++ gcc gfortran git gzip lsb-release patch python3 tar unzip xz-utils zstd

         .. tab-item:: RHEL/AlmaLinux/Rocky Linux

            .. code-block:: console

               $ dnf install epel-release
               $ dnf install file bzip2 ca-certificates git gzip patch python3 tar unzip xz zstd gcc gcc-c++ gcc-gfortran

   .. tab-item:: macOS

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
