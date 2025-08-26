.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      A guide to setting up and using Spack on Windows, including installing prerequisites and configuring the environment.

.. _windows_support:

Spack On Windows
================

Windows support for Spack is currently under development.
While this work is still in an early stage, it is currently possible to set up Spack and perform a few operations on Windows.
This section will guide you through the steps needed to install Spack and start running it on a fresh Windows machine.

Step 1: Install prerequisites
-----------------------------

To use Spack on Windows, you will need the following packages.

Required:

* Microsoft Visual Studio
* Python
* Git
* 7z

Optional:

* Intel Fortran (needed for some packages)

.. note::

  Currently MSVC is the only compiler tested for C/C++ projects.
  Intel OneAPI provides Fortran support.

Microsoft Visual Studio
^^^^^^^^^^^^^^^^^^^^^^^

Microsoft Visual Studio provides the only Windows C/C++ compiler that is currently supported by Spack.
Spack additionally requires that the Windows SDK (including WGL) to be installed as part of your Visual Studio installation as it is required to build many packages from source.

We require several specific components to be included in the Visual Studio installation.
One is the C/C++ toolset, which can be selected as "Desktop development with C++" or "C++ build tools," depending on installation type (Professional, Build Tools, etc.)
The other required component is "C++ CMake tools for Windows," which can be selected from among the optional packages.
This provides CMake and Ninja for use during Spack configuration.


If you already have Visual Studio installed, you can make sure these components are installed by rerunning the installer.
Next to your installation, select "Modify" and look at the "Installation details" pane on the right.

Intel Fortran
^^^^^^^^^^^^^

For Fortran-based packages on Windows, we strongly recommend Intel's oneAPI Fortran compilers.
The suite is free to download from Intel's website, located at https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/fortran-compiler.html.
The executable of choice for Spack will be Intel's Beta Compiler, ifx, which supports the classic compiler's (ifort's) frontend and runtime libraries by using LLVM.

Python
^^^^^^

As Spack is a Python-based package, an installation of Python will be needed to run it.
Python 3 can be downloaded and installed from the Windows Store, and will be automatically added to your ``PATH`` in this case.

.. note::
   Spack currently supports Python versions later than 3.2 inclusive.

Git
^^^

A bash console and GUI can be downloaded from https://git-scm.com/downloads.
If you are unfamiliar with Git, there are a myriad of resources online to help guide you through checking out repositories and switching development branches.

When given the option of adjusting your ``PATH``, choose the ``Git from the command line and also from 3rd-party software`` option.
This will automatically update your ``PATH`` variable to include the ``git`` command.

Spack support on Windows is currently dependent on installing the Git for Windows project as the project providing Git support on Windows.
This is additionally the recommended method for installing Git on Windows, a link to which can be found above.
Spack requires the utilities vendored by this project.

7zip
^^^^

A tool for extracting ``.xz`` files is required for extracting source tarballs.
The latest 7-Zip can be located at https://sourceforge.net/projects/sevenzip/.

Step 2: Install and setup Spack
-------------------------------

We are now ready to get the Spack environment set up on our machine.
We begin by using Git to clone the Spack repo, hosted at https://github.com/spack/spack.git into a desired directory, for our purposes today, called ``spack_install``.

In order to install Spack with Windows support, run the following one-liner in a Windows CMD prompt.

.. code-block:: console

   $ git clone https://github.com/spack/spack.git

.. note::
   If you chose to install Spack into a directory on Windows that is set up to require Administrative Privileges, Spack will require elevated privileges to run.
   Administrative Privileges can be denoted either by default, such as ``C:\Program Files``, or administrator-applied administrative restrictions on a directory that Spack installs files to such as ``C:\Users``

Step 3: Run and configure Spack
-------------------------------

On Windows, Spack supports both primary native shells, Powershell and the traditional command prompt.
To use Spack, pick your favorite shell, and run ``bin\spack_cmd.bat`` or ``share/spack/setup-env.ps1`` (you may need to Run as Administrator) from the top-level Spack directory.
This will provide a Spack-enabled shell.
If you receive a warning message that Python is not in your ``PATH`` (which may happen if you installed Python from the website and not the Windows Store), add the location of the Python executable to your ``PATH`` now.
You can permanently add Python to your ``PATH`` variable by using the ``Edit the system environment variables`` utility in Windows Control Panel.

To configure Spack, first run the following command inside the Spack console:

.. code-block:: console

   $ spack compiler find

This creates a ``.staging`` directory in our Spack prefix, along with a ``windows`` subdirectory containing a ``packages.yaml`` file.
On a fresh Windows installation with the above packages installed, this command should only detect Microsoft Visual Studio and the Intel Fortran compiler will be integrated within the first version of MSVC present in the ``packages.yaml`` output.

Spack provides a default ``config.yaml`` file for Windows that it will use unless overridden.
This file is located at ``etc\spack\defaults\windows\config.yaml``.
You can read more on how to do this and write your own configuration files in the :ref:`Configuration Files<configuration>` section of our documentation.
If you do this, pay particular attention to the ``build_stage`` block of the file as this specifies the directory that will temporarily hold the source code for the packages to be installed.
This path name must be sufficiently short for compliance with CMD, otherwise you will see build errors during installation (particularly with CMake) tied to long path names.

To allow Spack's use of external tools and dependencies already on your system, the external pieces of software must be described in the ``packages.yaml`` file.
There are two methods to populate this file:

The first and easiest choice is to use Spack to find installations on your system.
In the Spack terminal, run the following commands:

.. code-block:: console

   $ spack external find cmake
   $ spack external find ninja

The ``spack external find <name>`` will find executables on your system with the same name given.
The command will store the items found in ``packages.yaml`` in the ``.staging\`` directory.

Assuming that the command found CMake and Ninja executables in the previous step, continue to Step 4.
If no executables were found, we may need to manually direct Spack towards the CMake and Ninja installations we set up with Visual Studio.
Therefore, your ``packages.yaml`` file will look something like this, possibly with slight variations in the paths to CMake and Ninja:

.. code-block:: yaml

   packages:
     cmake:
       externals:
       - spec: cmake@3.19
         prefix: 'c:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake'
       buildable: false
     ninja:
       externals:
       - spec: ninja@1.8.2
         prefix: 'c:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja'
       buildable: false

You can also use a separate installation of CMake if you have one and prefer to use it.
If you don't have a path to Ninja analogous to the above, then you can obtain it by running the Visual Studio Installer and following the instructions at the start of this section.
Also note that YAML files use spaces for indentation and not tabs, so ensure that this is the case when editing one directly.


.. note::
   The use of Cygwin is not officially supported by Spack and is not tested.
   However, Spack will not prevent this, so if choosing to use Spack with Cygwin, know that no functionality is guaranteed.

Step 4: Use Spack
-----------------

Once the configuration is complete, it is time to give the installation a test.
Install a basic package through the Spack console via:

.. code-block:: spec

   $ spack install cpuinfo

If in the previous step, you did not have CMake or Ninja installed, running the command above should install both packages.

.. note::
   Windows has a few idiosyncrasies when it comes to the Spack spec syntax and the use of certain shells See the Spack spec syntax doc for more information


For developers
--------------

The intent is to provide a Windows installer that will automatically set up Python, Git, and Spack, instead of requiring the user to do so manually.
Instructions for creating the installer are at https://github.com/spack/spack/blob/develop/lib/spack/spack/cmd/installer/README.md
