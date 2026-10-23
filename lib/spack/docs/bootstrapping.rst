..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Learn how Spack's bootstrapping feature automatically fetches and installs essential build tools when they are not available on the host system.

.. _cmd-spack-bootstrap:
.. _cmd-spack-bootstrap-status:
.. _cmd-spack-bootstrap-now:

.. index::
   single: bootstrap; managing
   single: spack bootstrap
   :name: bootstrapping

Bootstrapping
=============

In the :ref:`Getting started <getting_started>` section, we already mentioned that Spack can bootstrap some of its dependencies, including ``clingo``.
In fact, there is an entire command dedicated to the management of every aspect of bootstrapping:

.. command-output:: spack bootstrap --help

Spack bootstraps its dependencies automatically the first time they are needed.
You can readily check if any prerequisite for using Spack is missing by running:

.. code-block:: console

   % spack bootstrap status
   Spack v0.19.0 - python@3.8

   [FAIL] Core Functionalities
     [B] MISSING "clingo": required to concretize specs

   [FAIL] Binary packages
     [B] MISSING "gpg2": required to sign/verify buildcaches


   Spack will take care of bootstrapping any missing dependency marked as [B]. Dependencies marked as [-] are instead required to be found on the system.

   % echo $?
   1

In the case of the output shown above, Spack detected that both ``clingo`` and ``gnupg`` are missing, and it's giving detailed information on why they are needed and whether they can be bootstrapped.
The return code of this command summarizes the results; if any dependencies are missing, the return code is ``1``, otherwise ``0``.
Running a command that concretizes a spec, like:

.. code-block:: console

   % spack solve zlib
   ==> Bootstrapping clingo-bootstrap from pre-built binaries
   [e] cqy5gwu python@3.9 /Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9 (0s)
   [+] 7xm6itd python-venv@1.0 /Users/spack/.spack/bootstrap/store/darwin-aarch64/python-venv-1.0-7xm6itd35g5wfwebvwffsmpx5ekpdfnm (0s)
   [+] sttzv6g clingo-bootstrap@spack /Users/spack/.spack/bootstrap/store/darwin-aarch64/clingo-bootstrap-spack-sttzv6ggizrkss7mjeln7pigo52i2oi4 (1s)
   [ ... ]

automatically triggers the bootstrapping of clingo from pre-built binaries as expected.

Users can also bootstrap all Spack's dependencies in a single command, which is useful to set up containers or other similar environments:

.. code-block:: console

   $ spack bootstrap now
   ==> Bootstrapping patchelf from pre-built binaries
   [e] 7s7rcbh glibc@2.39 /usr (0s)
   [+] zif26uy gcc-runtime@10.2.1 /root/.spack/bootstrap/store/linux-aarch64/gcc-runtime-10.2.1-zif26uy22eplr37dqfcjoffkllpayilj (2s)
   [+] c7jtmhh patchelf@0.17.2 /root/.spack/bootstrap/store/linux-aarch64/patchelf-0.17.2-c7jtmhhiy7tvvissvzlzgti7gpwdskzi (1s)
   [ ... ]

.. _cmd-spack-bootstrap-root:

The Bootstrapping Store
-----------------------

The software installed for bootstrapping purposes is deployed in a separate store.
You can check its location with the following command:

.. code-block:: console

   % spack bootstrap root

You can also change it by specifying the desired path:

.. code-block:: console

   % spack bootstrap root /opt/spack/bootstrap

You can check what is installed in the bootstrapping store at any time using:

.. code-block:: console

   % spack -b find
   ==> Showing internal bootstrap store at "/Users/spack/.spack/bootstrap/store"
   ==> 11 installed packages
   -- darwin-catalina-x86_64 / apple-clang@12.0.0 ------------------
   clingo-bootstrap@spack  libassuan@2.5.5  libgpg-error@1.42  libksba@1.5.1  pinentry@1.1.1  zlib@1.2.11
   gnupg@2.3.1             libgcrypt@1.9.3  libiconv@1.16      npth@1.6       python@3.8

If needed, you can remove all the software in the current bootstrapping store with:

.. code-block:: console

   % spack clean -b
   ==> Removing bootstrapped software and configuration in "/Users/spack/.spack/bootstrap"

   % spack -b find
   ==> Showing internal bootstrap store at "/Users/spack/.spack/bootstrap/store"
   ==> 0 installed packages

Pre-built binaries are verified by the sha256 sums listed, by DAG hash, in the ``metadata.yaml`` file of their bootstrapping source.
They were built on another host, so Spack splices the python interpreter and the libc of the current host into them, and it creates a venv for the current interpreter instead of using a pre-built one.
The specs installed for each interpreter are recorded in an environment, in the ``environments`` directory of the bootstrapping root.

.. _cmd-spack-bootstrap-list:
.. _cmd-spack-bootstrap-disable:
.. _cmd-spack-bootstrap-enable:
.. _cmd-spack-bootstrap-reset:

Enabling and Disabling Bootstrapping Methods
--------------------------------------------

Bootstrapping is performed by trying the methods listed by:

.. command-output:: spack bootstrap list

in the order they appear, from top to bottom.
By default, Spack is configured to try bootstrapping from pre-built binaries first and to fall back to bootstrapping from sources if that fails.

If needed, you can disable bootstrapping altogether by running:

.. code-block:: console

   % spack bootstrap disable

in which case, it's your responsibility to ensure Spack runs in an environment where all its prerequisites are installed.
You can also configure Spack to skip certain bootstrapping methods by disabling them specifically:

.. code-block:: console

   % spack bootstrap disable github-actions
   ==> "github-actions" is now disabled and will not be used for bootstrapping

tells Spack to skip trying to bootstrap from binaries.
To add the "github-actions" method back, you can:

.. code-block:: console

   % spack bootstrap enable github-actions

You can also reset the bootstrapping configuration to Spack's defaults:

.. code-block:: console

   % spack bootstrap reset
   ==> Bootstrapping configuration is being reset to Spack's defaults. Current configuration will be lost.
   Do you want to continue? [Y/n]
   %

.. index:: air-gapped

.. _cmd-spack-bootstrap-mirror:
.. _cmd-spack-bootstrap-add:

Creating a Mirror for Air-Gapped Systems
----------------------------------------

Spack's default bootstrapping configuration requires internet connection to fetch precompiled binaries or source tarballs.
Sometimes, though, Spack is deployed on air-gapped systems where such access is denied.

To help in these situations, Spack provides a command to create a local mirror containing the source tarballs and/or binary packages needed for bootstrapping.

.. code-block:: console

   % spack bootstrap mirror --binary-packages /opt/bootstrap
   ==> Adding "clingo-bootstrap@spack+python platform=linux target=x86_64" and dependencies to the mirror at /opt/bootstrap/bootstrap_cache
   ==> Adding "gnupg@2.3: platform=linux target=x86_64" and dependencies to the mirror at /opt/bootstrap/bootstrap_cache
   ==> Adding "patchelf@0.13.1: platform=linux target=x86_64" and dependencies to the mirror at /opt/bootstrap/bootstrap_cache
   ==> Adding "gnuconfig" and dependencies to the mirror at /opt/bootstrap/bootstrap_cache
   ==> Adding binary packages from "https://github.com/spack/spack-bootstrap-mirrors/releases/download/v2.2/bootstrap-buildcache.tar.gz" to the mirror at /opt/bootstrap/bootstrap_cache

   To register the mirror on the platform where it's supposed to be used, move "/opt/bootstrap" to its final location and run the following command(s):

     % spack bootstrap add --trust local-sources <final-path>/metadata/sources
     % spack bootstrap add --trust local-binaries <final-path>/metadata/binaries

Run this command on a machine with internet access, then move the resulting folder to the air-gapped system.
The metadata of the local binaries lists the same sha256 sums as the default binary source, so the binaries are verified in the same way.
Once the local sources are added using the commands suggested at the prompt, they can be used to bootstrap Spack.
