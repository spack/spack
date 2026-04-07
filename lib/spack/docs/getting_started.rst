..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

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
* Register a build cache that provides a compiler already available as a binary

Once a compiler is available, you can proceed installing your first package:

.. code-block:: spec

   $ spack install tcl

The output of this command should look similar to the following:

.. code-block:: text

   [e] zmjbkxx gcc@10.5.0 /usr (0s)
   [e] rawvy4p glibc@2.31 /usr (0s)
   [+] 5qfbgng compiler-wrapper@1.0 /home/spack/.local/spack/opt/linux-icelake/compiler-wrapper-1.0-5qfbgngzoqcjfbwrjn2vh75fr3g25c35 (0s)
   [+] vchaib2 gcc-runtime@10.5.0 /home/spack/.local/spack/opt/linux-icelake/gcc-runtime-10.5.0-vchaib2njqlk2cud4a2n33tabq526qjj (0s)
   [+] vzazvty gmake@4.4.1 /home/spack/.local/spack/opt/linux-icelake/gmake-4.4.1-vzazvtyn5cjdmg3vkkuau35x7hzu7pyl (12s)
   [+] soedrhb zlib-ng@2.3.3 /home/spack/.local/spack/opt/linux-icelake/zlib-ng-2.3.3-soedrhbnpeordiixaib6utcple6tpgya (3s)
   [+] u6nztpk tcl@8.6.17 /home/spack/.local/spack/opt/linux-icelake/tcl-8.6.17-u6nztpkhzbga4ul665qqhxucxqk3cins (49s)


Congratulations!
You just installed your first package with Spack!

Use the software you just installed
-----------------------------------

Once you have installed ``tcl``, you can immediately use it by starting the ``tclsh`` with its absolute path:

.. code-block:: console

   $ /home/spack/.local/spack/opt/linux-icelake/tcl-8.6.17-u6nztpkhzbga4ul665qqhxucxqk3cins/bin/tclsh
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

   :doc:`Spack Environments <environments_basics>` are a better way to install and load a set of packages that are frequently used together.
   The discussion of this topic goes beyond this ``Getting Started`` guide, and we refer to :ref:`environments` for more information.

Next steps
----------

This section helped you get Spack installed and running quickly.
There are further resources in the documentation that cover both basic and advanced topics in more detail:

Basic Usage
   1. :ref:`basic-usage`
   2. :ref:`compiler-config`
   3. :doc:`environments_basics`

Advanced Topics
   1. :ref:`toolchains`
   2. :ref:`cmd-spack-audit`
   3. :ref:`cmd-spack-verify`
