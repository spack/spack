.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _getting_started:

===============
Getting Started
===============

Getting Spack is easy.  You can clone it from the `GitHub repository
<https://github.com/spack/spack>`_ using this command:

.. code-block:: console

   $ git clone --depth=2 https://github.com/spack/spack.git

This will create a directory called ``spack``. Once you have cloned Spack, we recommend sourcing the appropriate script for your shell:

.. tab-set::

   .. tab-item:: bash/zsh/sh

      .. code-block:: console

         $ . spack/share/spack/setup-env.sh

   .. tab-item:: tcsh/csh

      .. code-block:: console

         $ source spack/share/spack/setup-env.csh

   .. tab-item:: fish

      .. code-block:: console

         $ . spack/share/spack/setup-env.fish

Now you're ready to use Spack!

-----------------------------
List packages you can install
-----------------------------

Once Spack is ready you can list all the packages it knows about with the following command:

.. code-block:: console

   $ spack list

If you want to get more information on a specific package, for instance ``hdf5``, you can use:

.. code-block:: console

   $ spack info hdf5

This command shows information about ``hdf5``, including a brief description, the versions of the package Spack knows about, and all the options you can activate when installing.

As you can see it's quite simple to gather basic information on packages, before you install them!

.. admonition:: Slowdown on the very first command
   :class: warning
   :collapsible:

   The very first command run with Spack will take a while to finish, as Spack has to build a few caches to speed-up further command execution.
   This will be just a one-off slowdown though, and subsequent command execution is much faster.

-----------------------------
Installing your first package
-----------------------------

To install most packages, Spack needs a compiler suite to be available.
To search your machine for available compilers, you can run:

.. code-block:: console

   $ spack compiler find

The command shows users if any compiler was found, and where its configuration is stored.
If the search was successful, you can now list known compilers, and get an output similar to the following:

.. code-block:: console

   $ spack compiler list
   ==> Available compilers
   -- gcc ubuntu20.04-x86_64 ---------------------------------------
   [e]  gcc@9.4.0  [e]  gcc@8.4.0  [e]  gcc@10.5.0

If no compiler was found, you need either:

* To install further prerequisites, for which we refer to :ref:`verify-spack-prerequisites`, and repeat the search above.
* To register a buildcache that provides a compiler already available as a binary

Once a compiler is available, by any of the above means, you can proceed installing your first package:

.. code-block:: console

   $ spack install tcl

The output of this command should look similar to the following:

.. code-block:: text

   [+] /usr (external gcc-10.5.0-zmjbkxxgltryn6hxwzan35qxxw4skbgl)
   ==> No binary for compiler-wrapper-1.0-lrmjw5qy3pjeynmxlyfkyzktarvnycfx found: installing from source
   ==> Installing compiler-wrapper-1.0-lrmjw5qy3pjeynmxlyfkyzktarvnycfx [2/7]
   [+] /usr (external glibc-2.31-rawvy4pmq4nwhk6ipqnesomvstwyopxq)
   ==> No binary for gcc-runtime-10.5.0-vchaib2njqlk2cud4a2n33tabq526qjj found: installing from source
   ==> Using cached archive: /tmp/try/spack/var/spack/cache/_source-cache/archive/c6/c65a9d2b2d4eef67ab5cb0684d706bb9f005bb2be94f53d82683d7055bdb837c
   ==> No patches needed for compiler-wrapper
   ==> Installing gcc-runtime-10.5.0-vchaib2njqlk2cud4a2n33tabq526qjj [4/7]
   ==> compiler-wrapper: Executing phase: 'install'
   ==> No patches needed for gcc-runtime
   ==> compiler-wrapper: Successfully installed compiler-wrapper-1.0-lrmjw5qy3pjeynmxlyfkyzktarvnycfx
     Stage: 0.00s.  Install: 0.00s.  Post-install: 0.01s.  Total: 0.07s
   [+] /home/spack/.local/spack/opt/linux-icelake/compiler-wrapper-1.0-lrmjw5qy3pjeynmxlyfkyzktarvnycfx
   ==> gcc-runtime: Executing phase: 'install'
   ==> gcc-runtime: Successfully installed gcc-runtime-10.5.0-vchaib2njqlk2cud4a2n33tabq526qjj
     Stage: 0.00s.  Install: 0.04s.  Post-install: 0.05s.  Total: 0.14s
   [+] /home/spack/.local/spack/opt/linux-icelake/gcc-runtime-10.5.0-vchaib2njqlk2cud4a2n33tabq526qjj
   ==> No binary for gmake-4.4.1-ifn6em7abtw6ozpog5ezy565vu66gsrm found: installing from source
   ==> Installing gmake-4.4.1-ifn6em7abtw6ozpog5ezy565vu66gsrm [5/7]
   ==> Using cached archive: /tmp/try/spack/var/spack/cache/_source-cache/archive/dd/dd16fb1d67bfab79a72f5e8390735c49e3e8e70b4945a15ab1f81ddb78658fb3.tar.gz
   ==> No patches needed for gmake
   ==> gmake: Executing phase: 'install'
   ==> gmake: Successfully installed gmake-4.4.1-ifn6em7abtw6ozpog5ezy565vu66gsrm
     Stage: 0.05s.  Install: 15.91s.  Post-install: 0.01s.  Total: 16.00s
   [+] /home/spack/.local/spack/opt/linux-icelake/gmake-4.4.1-ifn6em7abtw6ozpog5ezy565vu66gsrm
   ==> No binary for zlib-ng-2.2.4-j5ddfaq7nyykn2bovorx73gykhjcl5nz found: installing from source
   ==> Installing zlib-ng-2.2.4-j5ddfaq7nyykn2bovorx73gykhjcl5nz [6/7]
   ==> Using cached archive: /tmp/try/spack/var/spack/cache/_source-cache/archive/a7/a73343c3093e5cdc50d9377997c3815b878fd110bf6511c2c7759f2afb90f5a3.tar.gz
   ==> No patches needed for zlib-ng
   ==> zlib-ng: Executing phase: 'autoreconf'
   ==> zlib-ng: Executing phase: 'configure'
   ==> zlib-ng: Executing phase: 'build'
   ==> zlib-ng: Executing phase: 'install'
   ==> zlib-ng: Successfully installed zlib-ng-2.2.4-j5ddfaq7nyykn2bovorx73gykhjcl5nz
     Stage: 0.03s.  Autoreconf: 0.00s.  Configure: 3.63s.  Build: 2.52s.  Install: 0.09s.  Post-install: 0.02s.  Total: 6.49s
   [+] /home/spack/.local/spack/opt/linux-icelake/zlib-ng-2.2.4-j5ddfaq7nyykn2bovorx73gykhjcl5nz
   ==> No binary for tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv found: installing from source
   ==> Installing tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv [7/7]
   ==> Fetching https://mirror.spack.io/_source-cache/archive/26/26c995dd0f167e48b11961d891ee555f680c175f7173ff8cb829f4ebcde4c1a6.tar.gz
       [100%]   10.35 MB @   48.5 MB/s
   ==> No patches needed for tcl
   ==> tcl: Executing phase: 'autoreconf'
   ==> tcl: Executing phase: 'configure'
   ==> tcl: Executing phase: 'build'
   ==> tcl: Executing phase: 'install'
   ==> tcl: Successfully installed tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv
     Stage: 0.46s.  Autoreconf: 0.00s.  Configure: 9.25s.  Build: 1m 8.71s.  Install: 3.32s.  Post-install: 0.68s.  Total: 1m 22.61s
   [+] /home/spack/.local/spack/opt/linux-icelake/tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv

Congratulations! You just installed your first package with Spack!

-----------------------------------
Use the software you just installed
-----------------------------------

Once you installed ``tcl`` you can immediately use it starting the ``tcsh`` with its absolute path:

.. code-block:: console

   $ /home/spack/.local/spack/opt/linux-icelake/tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv/bin/tclsh
   >% echo "Hello world!"
   Hello world!

This works because of how Spack builds packages, setting the ``RPATH`` of their dependencies, but using such a long absolute path is not the most ergonomic way to refer to an executable.

The simplest way to have ``tcsh`` directory added to your ``PATH`` is to:

.. code-block:: console

   $ spack load tcl

Now the environment of the current shell has been modified, and you can use:

.. code-block:: console

   $ tcsh

directly. To undo these modifications, you can:

.. code-block:: console

   $ spack unload tcl

.. admonition:: Environments and views
   :class: tip

   A better way to install and load a set of packages that are frequently used are Spack Environments with views.
   The discussion of this topic is outside of the boundary of this "Getting Started" guide, and we refer to :ref:`environments` for more information.

----------
Next steps
----------

This section just helped you getting Spack installed, and running, quickly.
There are further resources in the documentation, for more advanced use cases:

1. **Getting information on packages**: see :ref:`basic-list-and-info-packages`
2. **Verify Spack prerequisites on a given system**: see :ref:`verify-spack-prerequisites`


.. _windows_support:

----------------
Spack On Windows
----------------

Windows support for Spack is currently under development. While this work is still in an early stage,
it is currently possible to set up Spack and perform a few operations on Windows.  This section will guide
you through the steps needed to install Spack and start running it on a fresh Windows machine.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Step 1: Install prerequisites
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To use Spack on Windows, you will need the following packages:

Required:
* Microsoft Visual Studio
* Python
* Git
* 7z

Optional:
* Intel Fortran (needed for some packages)

.. note::

  Currently MSVC is the only compiler tested for C/C++ projects. Intel OneAPI provides Fortran support.

"""""""""""""""""""""""
Microsoft Visual Studio
"""""""""""""""""""""""

Microsoft Visual Studio provides the only Windows C/C++ compiler that is currently supported by Spack.
Spack additionally requires that the Windows SDK (including WGL) to be installed as part of your
Visual Studio installation as it is required to build many packages from source.

We require several specific components to be included in the Visual Studio installation.
One is the C/C++ toolset, which can be selected as "Desktop development with C++" or "C++ build tools,"
depending on installation type (Professional, Build Tools, etc.)  The other required component is
"C++ CMake tools for Windows," which can be selected from among the optional packages.
This provides CMake and Ninja for use during Spack configuration.


If you already have Visual Studio installed, you can make sure these components are installed by
rerunning the installer.  Next to your installation, select "Modify" and look at the
"Installation details" pane on the right.

"""""""""""""
Intel Fortran
"""""""""""""

For Fortran-based packages on Windows, we strongly recommend Intel's oneAPI Fortran compilers.
The suite is free to download from Intel's website, located at
https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/fortran-compiler.html.
The executable of choice for Spack will be Intel's Beta Compiler, ifx, which supports the classic
compiler's (ifort's) frontend and runtime libraries by using LLVM.

""""""
Python
""""""

As Spack is a Python-based package, an installation of Python will be needed to run it.
Python 3 can be downloaded and installed from the Windows Store, and will be automatically added
to your ``PATH`` in this case.

.. note::
   Spack currently supports Python versions later than 3.2 inclusive.

""""""
Git
""""""

A bash console and GUI can be downloaded from https://git-scm.com/downloads.
If you are unfamiliar with Git, there are a myriad of resources online to help
guide you through checking out repositories and switching development branches.

When given the option of adjusting your ``PATH``, choose the ``Git from the
command line and also from 3rd-party software`` option. This will automatically
update your ``PATH`` variable to include the ``git`` command.

Spack support on Windows is currently dependent on installing the Git for Windows project
as the project providing Git support on Windows. This is additionally the recommended method
for installing Git on Windows, a link to which can be found above. Spack requires the
utilities vendored by this project.

""""""
7zip
""""""

A tool for extracting ``.xz`` files is required for extracting source tarballs. The latest 7-Zip
can be located at https://sourceforge.net/projects/sevenzip/.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Step 2: Install and setup Spack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We are now ready to get the Spack environment set up on our machine. We
begin by using Git to clone the Spack repo, hosted at https://github.com/spack/spack.git
into a desired directory, for our purposes today, called ``spack_install``.

In order to install Spack with Windows support, run the following one-liner
in a Windows CMD prompt.

.. code-block:: console

   git clone https://github.com/spack/spack.git

.. note::
   If you chose to install Spack into a directory on Windows that is set up to require Administrative
   Privileges, Spack will require elevated privileges to run.
   Administrative Privileges can be denoted either by default, such as
   ``C:\Program Files``, or administrator-applied administrative restrictions
   on a directory that Spack installs files to such as ``C:\Users``

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Step 3: Run and configure Spack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On Windows, Spack supports both primary native shells, Powershell and the traditional command prompt.
To use Spack, pick your favorite shell, and run ``bin\spack_cmd.bat`` or ``share/spack/setup-env.ps1``
(you may need to Run as Administrator) from the top-level Spack
directory. This will provide a Spack-enabled shell. If you receive a warning message that Python is not in your ``PATH``
(which may happen if you installed Python from the website and not the Windows Store), add the location
of the Python executable to your ``PATH`` now. You can permanently add Python to your ``PATH`` variable
by using the ``Edit the system environment variables`` utility in Windows Control Panel.

To configure Spack, first run the following command inside the Spack console:

.. code-block:: console

   spack compiler find

This creates a ``.staging`` directory in our Spack prefix, along with a ``windows`` subdirectory
containing a ``packages.yaml`` file. On a fresh Windows installation with the above packages
installed, this command should only detect Microsoft Visual Studio and the Intel Fortran
compiler will be integrated within the first version of MSVC present in the ``packages.yaml``
output.

Spack provides a default ``config.yaml`` file for Windows that it will use unless overridden.
This file is located at ``etc\spack\defaults\windows\config.yaml``. You can read more on how to
do this and write your own configuration files in the :ref:`Configuration Files<configuration>` section of our
documentation. If you do this, pay particular attention to the ``build_stage`` block of the file
as this specifies the directory that will temporarily hold the source code for the packages to
be installed. This path name must be sufficiently short for compliance with CMD, otherwise you
will see build errors during installation (particularly with CMake) tied to long path names.

To allow Spack's use of external tools and dependencies already on your system, the
external pieces of software must be described in the ``packages.yaml`` file.
There are two methods to populate this file:

The first and easiest choice is to use Spack to find installations on your system. In
the Spack terminal, run the following commands:

.. code-block:: console

   spack external find cmake
   spack external find ninja

The ``spack external find <name>`` will find executables on your system
with the same name given. The command will store the items found in
``packages.yaml`` in the ``.staging\`` directory.

Assuming that the command found CMake and Ninja executables in the previous
step, continue to Step 4. If no executables were found, we may need to manually direct Spack towards the CMake
and Ninja installations we set up with Visual Studio. Therefore, your ``packages.yaml`` file will look something
like this, possibly with slight variations in the paths to CMake and Ninja:

.. code-block:: yaml

   packages:
     cmake:
       externals:
       - spec: cmake@3.19
         prefix: 'c:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake'
       buildable: False
     ninja:
       externals:
       - spec: ninja@1.8.2
         prefix: 'c:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja'
       buildable: False

You can also use a separate installation of CMake if you have one and prefer
to use it. If you don't have a path to Ninja analogous to the above, then you can
obtain it by running the Visual Studio Installer and following the instructions
at the start of this section. Also note that YAML files use spaces for indentation
and not tabs, so ensure that this is the case when editing one directly.


.. note:: Cygwin
   The use of Cygwin is not officially supported by Spack and is not tested.
   However, Spack will not prevent this, so if choosing to use Spack
   with Cygwin, know that no functionality is guaranteed.

^^^^^^^^^^^^^^^^^
Step 4: Use Spack
^^^^^^^^^^^^^^^^^

Once the configuration is complete, it is time to give the installation a test.  Install a basic package through the
Spack console via:

.. code-block:: console

   spack install cpuinfo

If in the previous step, you did not have CMake or Ninja installed, running the command above should install both packages.

.. note:: Spec Syntax Caveats
   Windows has a few idiosyncrasies when it comes to the Spack spec syntax and the use of certain shells
   See the Spack spec syntax doc for more information


^^^^^^^^^^^^^^
For developers
^^^^^^^^^^^^^^

The intent is to provide a Windows installer that will automatically set up
Python, Git, and Spack, instead of requiring the user to do so manually.
Instructions for creating the installer are at
https://github.com/spack/spack/blob/develop/lib/spack/spack/cmd/installer/README.md
