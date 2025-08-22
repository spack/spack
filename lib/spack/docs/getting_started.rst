.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      A beginner's guide to Spack, walking you through the initial setup, basic commands, and core concepts to get you started with managing software.

.. _getting_started:

Getting Started
===============

Getting Spack is easy.
You can clone it from the `GitHub repository <https://github.com/spack/spack>`_ using this command:

.. code-block:: console

   $ git clone --depth=2 https://github.com/spack/spack.git

This will create a directory called ``spack``.
Once you have cloned Spack, we recommend sourcing the appropriate script for your shell.

For *bash*, *zsh* and *sh* users:

.. code-block:: console

   $ . spack/share/spack/setup-env.sh

For *csh* and *tcsh* users:

.. code-block:: console

   $ source spack/share/spack/setup-env.csh

For *fish* users:

.. code-block:: console

   $ . spack/share/spack/setup-env.fish

Now you're ready to use Spack!

List packages you can install
-----------------------------

Once Spack is ready, you can list all the packages it knows about with the following command:

.. code-block:: spec

   $ spack list

If you want to get more information on a specific package, for instance ``hdf5``, you can use:

.. code-block:: spec

   $ spack info hdf5

This command shows information about ``hdf5``, including a brief description, the versions of the package Spack knows about, and all the options you can activate when installing.

As you can see, it's quite simple to gather basic information on packages before you install them!

.. admonition:: Slowdown on the very first command
   :class: warning

   The first command you run with Spack may take a while, as Spack builds caches to speed up future commands.

Installing your first package
-----------------------------

To install most packages, Spack needs a compiler suite to be available.
To search your machine for available compilers, you can run:

.. code-block:: console

   $ spack compiler find

The command shows users whether any compilers were found and where their configuration is stored.
If the search was successful, you can now list known compilers, and get an output similar to the following:

.. code-block:: console

   $ spack compiler list
   ==> Available compilers
   -- gcc ubuntu20.04-x86_64 ---------------------------------------
   [e]  gcc@9.4.0  [e]  gcc@8.4.0  [e]  gcc@10.5.0

If no compilers were found, you need to either:

* Install further prerequisites, see :ref:`verify-spack-prerequisites`, and repeat the search above.
* Register a buildcache that provides a compiler already available as a binary

Once a compiler is available, you can proceed installing your first package:

.. code-block:: spec

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

Congratulations!
You just installed your first package with Spack!

Use the software you just installed
-----------------------------------

Once you have installed ``tcl``, you can immediately use it by starting the ``tclsh`` with its absolute path:

.. code-block:: console

   $ /home/spack/.local/spack/opt/linux-icelake/tcl-8.6.12-6vo5hxeqw5plzd6gvzm74wlfz5stnzcv/bin/tclsh
   >% echo "Hello world!"
   Hello world!

This works, but using such a long absolute path is not the most convenient way to run an executable.

The simplest way to have ``tclsh`` available on the command line is:

.. code-block:: spec

   $ spack load tcl

The environment of the current shell has now been modified, and you can run

.. code-block:: console

   $ tclsh

directly.
To undo these modifications, you can:

.. code-block:: spec

   $ spack unload tcl

.. admonition:: Environments and views
   :class: tip

   :ref:`Spack Environments <spack-environments-basic-usage>` are a better way to install and load a set of packages that are frequently used together.
   The discussion of this topic goes beyond this ``Getting Started`` guide, and we refer to :ref:`environments` for more information.

Next steps
----------

This section helped you get Spack installed and running quickly.
There are further resources in the documentation that cover both basic and advanced topics in more detail:

Basic Usage
   1. :ref:`basic-usage`
   2. :ref:`compiler-config`
   3. :ref:`spack-environments-basic-usage`

Advanced Topics
   1. :ref:`toolchains`
   2. :ref:`audit-packages-and-configuration`
   3. :ref:`verify-installations`
