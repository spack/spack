.. Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _basics-tutorial:

=========================================
Basic Installation Tutorial
=========================================

This tutorial will guide you through the process of installing
software using Spack. We will first cover the `spack install` command,
focusing on the power of the spec syntax and the flexibility it gives
to users. We will also cover the `spack find` command for viewing
installed packages and the `spack uninstall` command. Finally, we will
touch on how Spack manages compilers, especially as it relates to
using Spack-built compilers within Spack. We will include full output
from all of the commands demonstrated, although we will frequently
call attention to only small portions of that output (or merely to the
fact that it succeeded). The provided output is all from an AWS
instance running Ubuntu 16.04

.. _basics-tutorial-install:

----------------
Installing Spack
----------------

Spack works out of the box. Simply clone spack and get going. We will
clone Spack and immediately checkout the most recent release, v0.11.2.

.. code-block:: console

  $  git clone https://github.com/spack/spack
  Cloning into 'spack'...
  remote: Enumerating objects: 60, done.
  remote: Counting objects: 100% (60/60), done.
  remote: Compressing objects: 100% (54/54), done.
  remote: Total 135310 (delta 31), reused 11 (delta 5), pack-reused 135250
  Receiving objects: 100% (135310/135310), 47.30 MiB | 12.83 MiB/s, done.
  Resolving deltas: 100% (64369/64369), done.
  $ cd spack
  $ git checkout releases/v0.11.3
  Branch releases/v0.11.3 set up to track remote branch releases/v0.11.3 from origin.
  Switched to a new branch 'releases/v0.11.3'

Next add Spack to your path. Spack has some nice command line
integration tools, so instead of simply appending to your ``PATH``
variable, source the spack setup script.  Then add Spack to your path.

.. code-block:: console

  $ . share/spack/setup-env.sh

You're good to go!

-----------------
What is in Spack?
-----------------

The ``spack list`` command shows available packages.

.. code-block:: console

  $ spack list
  ==> 2907 packages.
  abinit                           libgpuarray                             py-espresso                     r-mlrmbo
  abyss                            libgridxc                               py-espressopp                   r-mmwrweek
  accfft                           libgtextutils                           py-et-xmlfile                   r-mnormt
  ...

The ``spack list`` command can also take a query string. Spack
automatically adds wildcards to both ends of the string. For example,
we can view all available python packages.

.. code-block:: console

  $ spack list py-
  ==> 479 packages.
  py-3to2                                py-functools32       py-numpydoc         py-pywavelets
  py-4suite-xml                          py-future            py-olefile          py-pyyaml
  py-abipy                               py-futures           py-ont-fast5-api    py-qtawesome
  ...

-------------------
Installing Packages
-------------------

Installing a package with Spack is very simple. To install a piece of
software, simply type ``spack install <package_name>``.

.. code-block:: console

  $ spack install zlib
  ==> Installing zlib
  ==> Fetching http://zlib.net/fossils/zlib-1.2.11.tar.gz
  ######################################################################## 100.0%
  ==> Staging archive: /home/spack1/spack/var/spack/stage/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi/zlib-1.2.11.tar.gz
  ==> Created stage in /home/spack1/spack/var/spack/stage/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi
  ==> No patches needed for zlib
  ==> Building zlib [Package]
  ==> Executing phase: 'install'
  ==> Successfully installed zlib
    Fetch: 0.58s.  Build: 1.15s.  Total: 1.73s.
    [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi

Spack can install software either from source or from a binary
cache. Packages in the binary cache are signed with GPG for
security. For the tutorial we have prepared a binary cache so you
don't have to wait on slow compilation from source. To be able to
install from the binary cache, we will need to configure Spack to use
the binary cache and trust the GPG key that the binary cache was
prepared with.

.. code-block:: console

  $ spack mirror add tutorial /mirror
  $ spack mirror list
  tutorial    file:///mirror
  $  spack gpg trust /mirror/public.key 
  gpg: keybox '/home/spack1/spack/opt/spack/gpg/pubring.kbx' created
  gpg: /home/spack1/spack/opt/spack/gpg/trustdb.gpg: trustdb created
  gpg: key 9CFA4A453B7C69B2: public key "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" imported
  gpg: Total number processed: 1
  gpg:               imported: 1

The Spack install command will install the binary cached package if it
exists and fall back on installing from source. To bypass the binary
cache, use the ``--no-cache`` option to ``spack install``.

Spack's spec syntax is the interface by which we can request specific
configurations of the package. The ``%`` sigil is used to specify
compilers.

.. code-block:: console

  $ spack install --use-cache zlib %clang
  ...
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64-gcc-7.3.0-libxml2-2.9.8-xhsbjjjj4jdo5vv4nszwu5edip4fhebh.spec.yaml
  ########################################################################################################################### 100.0%
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64-gcc-7.2.0-diffutils-3.6-amfzwbi2qieghszbyq6kvjfi7n6be5qy.spec.yaml
  ########################################################################################################################### 100.0%
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64-gcc-7.3.0-netlib-scalapack-2.0.2-nz5mzhstb7lfnobzwuye65uonn67agyh.spec.yaml
  ########################################################################################################################### 100.0%
  ==> Installing zlib from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/clang-6.0.0-1ubuntu2/zlib-1.2.11/linux-ubuntu18.04-x86_64-clang-6.0.0-1ubuntu2-zlib-1.2.11-37pzrwcovpu5wxaldr5l4eg6i255dv4h.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:11:24 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed zlib from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/clang-6.0.0-1ubuntu2/zlib-1.2.11-37pzrwcovpu5wxaldr5l4eg6i255dv4h

Note that this installation is located separately from the previous
one. We will discuss this in more detail later, but this is part of what
allows Spack to support arbitrarily versioned software.

You can check for particular versions before requesting them. We will
use the ``spack versions`` command to see the available versions, and then
install a different version of ``zlib``.

.. code-block:: console

  $ spack versions zlib
  ==> Safe versions (already checksummed):
    1.2.11  1.2.8  1.2.3
  ==> Remote versions (not yet checksummed):
    1.2.10   1.2.7    1.2.5.1  1.2.4.2  1.2.3.7
    ...

The ``@`` sigil is used to specify versions, both of packages and of
compilers.

.. code-block:: console

  $ spack install zlib@1.2.8
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing zlib from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.8/linux-ubuntu18.04-x86_64-gcc-7.3.0-zlib-1.2.8-dpawgwuohqphts4z7vyrmzzrw6ljfvlg.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:12:09 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed zlib from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.8-dpawgwuohqphts4z7vyrmzzrw6ljfvlg

  $ spack install zlib %gcc@6.4
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing zlib from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-6.4/zlib-1.2.11/linux-ubuntu18.04-x86_64-gcc-6.4-zlib-1.2.11-ul42kj4zp2log5aqz6cdku4joxlrjtyt.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:12:00 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed zlib from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-6.4/zlib-1.2.11-ul42kj4zp2log5aqz6cdku4joxlrjtyt

The spec syntax also includes compiler flags. Spack accepts
``cppflags``, ``cflags``, ``cxxflags``, ``fflags``, ``ldflags``, and
``ldlibs`` parameters.  The values of these fields must be quoted on
the command line if they include spaces. These values are injected
into the compile line automatically by the Spack compiler wrappers.

.. code-block:: console

  $ spack install zlib @1.2.8 cppflags=-O3
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing zlib from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.8/linux-ubuntu18.04-x86_64-gcc-7.3.0-zlib-1.2.8-6fcmnppflzf6ia3yk7t32uw5wjyy64jg.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:27:48 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed zlib from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.8-6fcmnppflzf6ia3yk7t32uw5wjyy64jg

The ``spack find`` command is used to query installed packages. Note that
some packages appear identical with the default output. The ``-l`` flag
shows the hash of each package, and the ``-f`` flag shows any non-empty
compiler flags of those packages.

.. code-block:: console

  $ spack find
  ==> 5 installed packages.
  -- linux-ubuntu18.04-x86_64 / clang@6.0.0-1ubuntu2 --------------
  zlib@1.2.11

  -- linux-ubuntu18.04-x86_64 / gcc@6.4 ---------------------------
  zlib@1.2.11

  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
  zlib@1.2.8  zlib@1.2.8  zlib@1.2.11


  $ spack find -lf
  ==> 5 installed packages.
  -- linux-ubuntu18.04-x86_64 / clang@6.0.0-1ubuntu2 --------------
  37pzrwc zlib@1.2.11%clang


  -- linux-ubuntu18.04-x86_64 / gcc@6.4 ---------------------------
  ul42kj4 zlib@1.2.11%gcc


  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
  dpawgwu zlib@1.2.8%gcc

  6fcmnpp zlib@1.2.8%gcc cppflags="-O3" 

  av3mmgf zlib@1.2.11%gcc

Spack generates a hash for each spec. This hash is a function of the full
provenance of the package, so any change to the spec affects the
hash. Spack uses this value to compare specs and to generate unique
installation directories for every combinatorial version. As we move into
more complicated packages with software dependencies, we can see that
Spack reuses existing packages to satisfy a dependency only when the
existing package's hash matches the desired spec.

.. code-block:: console

  $ spack install tcl
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi
  ==> Installing tcl
  ==> Searching for binary cache of tcl
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing tcl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/tcl-8.6.8/linux-ubuntu18.04-x86_64-gcc-7.3.0-tcl-8.6.8-ddd4sqiwshbudadbap3nangd3iobx5c6.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:11:59 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed tcl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/tcl-8.6.8-ddd4sqiwshbudadbap3nangd3iobx5c6

Dependencies can be explicitly requested using the ``^`` sigil. Note that
the spec syntax is recursive. Anything we could specify about the
top-level package, we can also specify about a dependency using ``^``.

.. code-block:: console

  $ spack install tcl ^zlib @1.2.8 %clang
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing zlib from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/clang-6.0.0-1ubuntu2/zlib-1.2.8/linux-ubuntu18.04-x86_64-clang-6.0.0-1ubuntu2-zlib-1.2.8-4z4djeow35uyjzfnjy7dval6zo7ul4wz.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:57:57 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed zlib from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/clang-6.0.0-1ubuntu2/zlib-1.2.8-4z4djeow35uyjzfnjy7dval6zo7ul4wz
  ==> Installing tcl
  ==> Searching for binary cache of tcl
  ==> Installing tcl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/clang-6.0.0-1ubuntu2/tcl-8.6.8/linux-ubuntu18.04-x86_64-clang-6.0.0-1ubuntu2-tcl-8.6.8-5u7fuxk7pqe5nllvn4abpvta5dbuq4sp.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:04:20 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed tcl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/clang-6.0.0-1ubuntu2/tcl-8.6.8-5u7fuxk7pqe5nllvn4abpvta5dbuq4sp

Packages can also be referred to from the command line by their package
hash. Using the ``spack find -lf`` command earlier we saw that the hash
of our optimized installation of zlib (``cppflags="-O3"``) began with
``6fcmnpp``. We can now explicitly build with that package without typing
the entire spec, by using the ``/`` sigil to refer to it by hash. As with
other tools like git, you do not need to specify an *entire* hash on the
command line.  You can specify just enough digits to identify a hash
uniquely.  If a hash prefix is ambiguous (i.e., two or more installed
packages share the prefix) then spack will report an error.

.. code-block:: console

  $ spack install tcl ^/6fcm
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.8-6fcmnppflzf6ia3yk7t32uw5wjyy64jg
  ==> Installing tcl
  ==> Searching for binary cache of tcl
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing tcl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/tcl-8.6.8/linux-ubuntu18.04-x86_64-gcc-7.3.0-tcl-8.6.8-ua7zdu4dlg2n2yvszxfymk4i6ayrjere.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:14:26 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed tcl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/tcl-8.6.8-ua7zdu4dlg2n2yvszxfymk4i6ayrjere

The ``spack find`` command can also take a ``-d`` flag, which can show
dependency information. Note that each package has a top-level entry,
even if it also appears as a dependency.

.. code-block:: console

  $ spack find -ldf
  ==> 9 installed packages.
  -- linux-ubuntu18.04-x86_64 / clang@6.0.0-1ubuntu2 --------------
  5u7fuxk    tcl@8.6.8%clang
  4z4djeo        ^zlib@1.2.8%clang

  4z4djeo    zlib@1.2.8%clang

  37pzrwc    zlib@1.2.11%clang


  -- linux-ubuntu18.04-x86_64 / gcc@6.4 ---------------------------
  ul42kj4    zlib@1.2.11%gcc


  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
  ddd4sqi    tcl@8.6.8%gcc
  av3mmgf        ^zlib@1.2.11%gcc

  ua7zdu4    tcl@8.6.8%gcc
  6fcmnpp        ^zlib@1.2.8%gcc cppflags="-O3" 

  dpawgwu    zlib@1.2.8%gcc

  6fcmnpp    zlib@1.2.8%gcc cppflags="-O3" 

  av3mmgf    zlib@1.2.11%gcc

Let's move on to slightly more complicated packages. ``HDF5`` is a
good example of a more complicated package, with an MPI dependency. If
we install it "out of the box," it will build with ``openmpi``.

.. code-block:: console

  $ spack install hdf5
  ==> Installing libsigsegv
  ==> Searching for binary cache of libsigsegv
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing libsigsegv from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/libsigsegv-2.11/linux-ubuntu18.04-x86_64-gcc-7.3.0-libsigsegv-2.11-oromhtnsg3whjgy4ufgufwwwxe3iadp7.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:15:25 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed libsigsegv from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libsigsegv-2.11-oromhtnsg3whjgy4ufgufwwwxe3iadp7
  ==> Installing m4
  ==> Searching for binary cache of m4
  ==> Installing m4 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/m4-1.4.18/linux-ubuntu18.04-x86_64-gcc-7.3.0-m4-1.4.18-vypfbpxo4do2ieh3hf7fbxpyz66b5zav.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:44:39 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed m4 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/m4-1.4.18-vypfbpxo4do2ieh3hf7fbxpyz66b5zav
  ==> Installing libtool
  ==> Searching for binary cache of libtool
  ==> Installing libtool from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/libtool-2.4.6/linux-ubuntu18.04-x86_64-gcc-7.3.0-libtool-2.4.6-jher54m7efbgqjarpywxcb3yxmelyswk.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:09:16 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed libtool from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libtool-2.4.6-jher54m7efbgqjarpywxcb3yxmelyswk
  ==> Installing pkgconf
  ==> Searching for binary cache of pkgconf
  ==> Installing pkgconf from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/pkgconf-1.4.2/linux-ubuntu18.04-x86_64-gcc-7.3.0-pkgconf-1.4.2-gavqfquorv7kyfjbib5w3w5odhfkuggc.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:11:11 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed pkgconf from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/pkgconf-1.4.2-gavqfquorv7kyfjbib5w3w5odhfkuggc
  ==> Installing util-macros
  ==> Searching for binary cache of util-macros
  ==> Installing util-macros from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/util-macros-1.19.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-util-macros-1.19.1-325c2mbwiy55522757xear34254ihlub.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:15:25 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed util-macros from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/util-macros-1.19.1-325c2mbwiy55522757xear34254ihlub
  ==> Installing libpciaccess
  ==> Searching for binary cache of libpciaccess
  ==> Installing libpciaccess from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/libpciaccess-0.13.5/linux-ubuntu18.04-x86_64-gcc-7.3.0-libpciaccess-0.13.5-7x2dp3quycimjbqwi6plzfi5huj2xnef.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:08:51 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed libpciaccess from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libpciaccess-0.13.5-7x2dp3quycimjbqwi6plzfi5huj2xnef
  ==> Installing xz
  ==> Searching for binary cache of xz
  ==> Installing xz from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/xz-5.2.4/linux-ubuntu18.04-x86_64-gcc-7.3.0-xz-5.2.4-buhe32jt3hgxzvpi4hzsiwoo7kbecfjq.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:27:01 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed xz from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/xz-5.2.4-buhe32jt3hgxzvpi4hzsiwoo7kbecfjq
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi
  ==> Installing libxml2
  ==> Searching for binary cache of libxml2
  ==> Installing libxml2 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/libxml2-2.9.8/linux-ubuntu18.04-x86_64-gcc-7.3.0-libxml2-2.9.8-xhsbjjjj4jdo5vv4nszwu5edip4fhebh.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:46:05 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed libxml2 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libxml2-2.9.8-xhsbjjjj4jdo5vv4nszwu5edip4fhebh
  ==> Installing ncurses
  ==> Searching for binary cache of ncurses
  ==> Installing ncurses from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/ncurses-6.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-ncurses-6.1-c4iq7eli75yuf5rkigpk7is63eurr6rp.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:15:21 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed ncurses from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/ncurses-6.1-c4iq7eli75yuf5rkigpk7is63eurr6rp
  ==> Installing readline
  ==> Searching for binary cache of readline
  ==> Installing readline from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/readline-7.0/linux-ubuntu18.04-x86_64-gcc-7.3.0-readline-7.0-lg4ce4zttwtp6ajkdhyw62rx2i4ctpvl.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:43:55 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed readline from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/readline-7.0-lg4ce4zttwtp6ajkdhyw62rx2i4ctpvl
  ==> Installing gdbm
  ==> Searching for binary cache of gdbm
  ==> Installing gdbm from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/gdbm-1.14.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-gdbm-1.14.1-64j7o2pwuhpt5yurbcheljveamvpyfsl.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:46:14 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed gdbm from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/gdbm-1.14.1-64j7o2pwuhpt5yurbcheljveamvpyfsl
  ==> Installing perl
  ==> Searching for binary cache of perl
  ==> Installing perl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/perl-5.26.2/linux-ubuntu18.04-x86_64-gcc-7.3.0-perl-5.26.2-kpukrzpbnqfob42y5lpffsc6bksqee7h.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:09:14 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed perl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/perl-5.26.2-kpukrzpbnqfob42y5lpffsc6bksqee7h
  ==> Installing autoconf
  ==> Searching for binary cache of autoconf
  ==> Installing autoconf from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/autoconf-2.69/linux-ubuntu18.04-x86_64-gcc-7.3.0-autoconf-2.69-7mf25r4qp3msoto4peybu677rxe622re.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:03:37 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed autoconf from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/autoconf-2.69-7mf25r4qp3msoto4peybu677rxe622re
  ==> Installing automake
  ==> Searching for binary cache of automake
  ==> Installing automake from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/automake-1.16.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-automake-1.16.1-p2omviwtyjez7ba5cfhofw3tlr5l7jog.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:57:20 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed automake from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/automake-1.16.1-p2omviwtyjez7ba5cfhofw3tlr5l7jog
  ==> Installing numactl
  ==> Searching for binary cache of numactl
  ==> Installing numactl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/numactl-2.0.11/linux-ubuntu18.04-x86_64-gcc-7.3.0-numactl-2.0.11-jvoj2ptukcmnqwenwjljytzmtfyezxvs.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:15:22 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed numactl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/numactl-2.0.11-jvoj2ptukcmnqwenwjljytzmtfyezxvs
  ==> Installing hwloc
  ==> Searching for binary cache of hwloc
  ==> Installing hwloc from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/hwloc-1.11.9/linux-ubuntu18.04-x86_64-gcc-7.3.0-hwloc-1.11.9-uslokkifia23o3n4ne4r72owoyx2dynb.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:12:51 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hwloc from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hwloc-1.11.9-uslokkifia23o3n4ne4r72owoyx2dynb
  ==> Installing openmpi
  ==> Searching for binary cache of openmpi
  ==> Installing openmpi from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/openmpi-3.1.3/linux-ubuntu18.04-x86_64-gcc-7.3.0-openmpi-3.1.3-tfegwcywpztpm57cl44hxf64kbckdjmu.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:14:45 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed openmpi from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/openmpi-3.1.3-tfegwcywpztpm57cl44hxf64kbckdjmu
  ==> Installing hdf5
  ==> Searching for binary cache of hdf5
  ==> Installing hdf5 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4/linux-ubuntu18.04-x86_64-gcc-7.3.0-hdf5-1.10.4-z33coumgesxxse2zr2k5bffvnyhjl2t7.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:09:32 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hdf5 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4-z33coumgesxxse2zr2k5bffvnyhjl2t7

Spack packages can also have variants. Boolean variants can be specified
using the ``+`` and ``~`` or ``-`` sigils. There are two sigils for
``False`` to avoid conflicts with shell parsing in different
situations. Variants (boolean or otherwise) can also be specified using
the same syntax as compiler flags.  Here we can install HDF5 without MPI
support.

.. code-block:: console

   $ spack install hdf5~mpi
   ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi
   ==> Installing hdf5
   ==> Searching for binary cache of hdf5
   ==> Finding buildcaches in /mirror/build_cache
   ==> Installing hdf5 from binary cache
   ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4/linux-ubuntu18.04-x86_64-gcc-7.3.0-hdf5-1.10.4-uggv4drbokmhq6bhlkftbvoeneaj5do4.spack
   ########################################################################################################################### 100.0%
   gpg: Signature made Thu Nov  8 01:27:09 2018 UTC
   gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
   gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
   gpg: WARNING: This key is not certified with a trusted signature!
   gpg:          There is no indication that the signature belongs to the owner.
   Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
   ==> Successfully installed hdf5 from binary cache
   [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4-uggv4drbokmhq6bhlkftbvoeneaj5do4

We might also want to install HDF5 with a different MPI
implementation. While MPI is not a package itself, packages can depend on
abstract interfaces like MPI. Spack handles these through "virtual
dependencies." A package, such as HDF5, can depend on the MPI
interface. Other packages (``openmpi``, ``mpich``, ``mvapich``, etc.)
provide the MPI interface.  Any of these providers can be requested for
an MPI dependency. For example, we can build HDF5 with MPI support
provided by mpich by specifying a dependency on ``mpich``. Spack also
supports versioning of virtual dependencies. A package can depend on the
MPI interface at version 3, and provider packages specify what version of
the interface *they* provide. The partial spec ``^mpi@3`` can be safisfied
by any of several providers.

.. code-block:: console

  $ spack install hdf5+hl+mpi ^mpich
  ==> libsigsegv is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libsigsegv-2.11-oromhtnsg3whjgy4ufgufwwwxe3iadp7
  ==> m4 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/m4-1.4.18-vypfbpxo4do2ieh3hf7fbxpyz66b5zav
  ==> pkgconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/pkgconf-1.4.2-gavqfquorv7kyfjbib5w3w5odhfkuggc
  ==> ncurses is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/ncurses-6.1-c4iq7eli75yuf5rkigpk7is63eurr6rp
  ==> readline is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/readline-7.0-lg4ce4zttwtp6ajkdhyw62rx2i4ctpvl
  ==> gdbm is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/gdbm-1.14.1-64j7o2pwuhpt5yurbcheljveamvpyfsl
  ==> perl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/perl-5.26.2-kpukrzpbnqfob42y5lpffsc6bksqee7h
  ==> autoconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/autoconf-2.69-7mf25r4qp3msoto4peybu677rxe622re
  ==> automake is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/automake-1.16.1-p2omviwtyjez7ba5cfhofw3tlr5l7jog
  ==> libtool is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libtool-2.4.6-jher54m7efbgqjarpywxcb3yxmelyswk
  ==> Installing texinfo
  ==> Searching for binary cache of texinfo
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing texinfo from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/texinfo-6.5/linux-ubuntu18.04-x86_64-gcc-7.3.0-texinfo-6.5-onnlt2r2gnjths3f2w4otltihd4p2s5h.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:03:30 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed texinfo from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/texinfo-6.5-onnlt2r2gnjths3f2w4otltihd4p2s5h
  ==> Installing findutils
  ==> Searching for binary cache of findutils
  ==> Installing findutils from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/findutils-4.6.0/linux-ubuntu18.04-x86_64-gcc-7.3.0-findutils-4.6.0-capl6zymtrqxltqnfqiykagcciyumy6z.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:10:37 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed findutils from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/findutils-4.6.0-capl6zymtrqxltqnfqiykagcciyumy6z
  ==> Installing mpich
  ==> Searching for binary cache of mpich
  ==> Installing mpich from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/mpich-3.2.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-mpich-3.2.1-yf2xknkwvuopv7bslicv4x66fd4ntpbc.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:45:38 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed mpich from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/mpich-3.2.1-yf2xknkwvuopv7bslicv4x66fd4ntpbc
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi
  ==> Installing hdf5
  ==> Searching for binary cache of hdf5
  ==> Installing hdf5 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4/linux-ubuntu18.04-x86_64-gcc-7.3.0-hdf5-1.10.4-qtza2jxt57pcimpjomr5zxveonvfadap.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:11:34 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hdf5 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4-qtza2jxt57pcimpjomr5zxveonvfadap

We'll do a quick check in on what we have installed so far.

.. code-block:: console

  $ spack find -ldf
  ==> 32 installed packages.
  -- linux-ubuntu18.04-x86_64 / clang@6.0.0-1ubuntu2 --------------
  5u7fuxk    tcl@8.6.8%clang
  4z4djeo        ^zlib@1.2.8%clang

  4z4djeo    zlib@1.2.8%clang

  37pzrwc    zlib@1.2.11%clang


  -- linux-ubuntu18.04-x86_64 / gcc@6.4 ---------------------------
  ul42kj4    zlib@1.2.11%gcc


  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
  7mf25r4    autoconf@2.69%gcc
  vypfbpx        ^m4@1.4.18%gcc
  oromhtn            ^libsigsegv@2.11%gcc
  kpukrzp        ^perl@5.26.2%gcc
  64j7o2p            ^gdbm@1.14.1%gcc
  lg4ce4z                ^readline@7.0%gcc
  c4iq7el                    ^ncurses@6.1%gcc

  p2omviw    automake@1.16.1%gcc
  kpukrzp        ^perl@5.26.2%gcc
  64j7o2p            ^gdbm@1.14.1%gcc
  lg4ce4z                ^readline@7.0%gcc
  c4iq7el                    ^ncurses@6.1%gcc

  capl6zy    findutils@4.6.0%gcc

  64j7o2p    gdbm@1.14.1%gcc
  lg4ce4z        ^readline@7.0%gcc
  c4iq7el            ^ncurses@6.1%gcc

  uggv4dr    hdf5@1.10.4%gcc
  av3mmgf        ^zlib@1.2.11%gcc

  z33coum    hdf5@1.10.4%gcc
  tfegwcy        ^openmpi@3.1.3%gcc
  uslokki            ^hwloc@1.11.9%gcc
  7x2dp3q                ^libpciaccess@0.13.5%gcc
  xhsbjjj                ^libxml2@2.9.8%gcc
  buhe32j                    ^xz@5.2.4%gcc
  av3mmgf                    ^zlib@1.2.11%gcc
  jvoj2pt                ^numactl@2.0.11%gcc

  qtza2jx    hdf5@1.10.4%gcc
  yf2xknk        ^mpich@3.2.1%gcc
  av3mmgf        ^zlib@1.2.11%gcc

  uslokki    hwloc@1.11.9%gcc
  7x2dp3q        ^libpciaccess@0.13.5%gcc
  xhsbjjj        ^libxml2@2.9.8%gcc
  buhe32j            ^xz@5.2.4%gcc
  av3mmgf            ^zlib@1.2.11%gcc
  jvoj2pt        ^numactl@2.0.11%gcc

  7x2dp3q    libpciaccess@0.13.5%gcc

  oromhtn    libsigsegv@2.11%gcc

  jher54m    libtool@2.4.6%gcc

  xhsbjjj    libxml2@2.9.8%gcc
  buhe32j        ^xz@5.2.4%gcc
  av3mmgf        ^zlib@1.2.11%gcc

  vypfbpx    m4@1.4.18%gcc
  oromhtn        ^libsigsegv@2.11%gcc

  yf2xknk    mpich@3.2.1%gcc

  c4iq7el    ncurses@6.1%gcc

  jvoj2pt    numactl@2.0.11%gcc

  tfegwcy    openmpi@3.1.3%gcc
  uslokki        ^hwloc@1.11.9%gcc
  7x2dp3q            ^libpciaccess@0.13.5%gcc
  xhsbjjj            ^libxml2@2.9.8%gcc
  buhe32j                ^xz@5.2.4%gcc
  av3mmgf                ^zlib@1.2.11%gcc
  jvoj2pt            ^numactl@2.0.11%gcc

  kpukrzp    perl@5.26.2%gcc
  64j7o2p        ^gdbm@1.14.1%gcc
  lg4ce4z            ^readline@7.0%gcc
  c4iq7el                ^ncurses@6.1%gcc

  gavqfqu    pkgconf@1.4.2%gcc

  lg4ce4z    readline@7.0%gcc
  c4iq7el        ^ncurses@6.1%gcc

  ddd4sqi    tcl@8.6.8%gcc
  av3mmgf        ^zlib@1.2.11%gcc

  ua7zdu4    tcl@8.6.8%gcc
  6fcmnpp        ^zlib@1.2.8%gcc cppflags="-O3" 

  onnlt2r    texinfo@6.5%gcc
  kpukrzp        ^perl@5.26.2%gcc
  64j7o2p            ^gdbm@1.14.1%gcc
  lg4ce4z                ^readline@7.0%gcc
  c4iq7el                    ^ncurses@6.1%gcc

  325c2mb    util-macros@1.19.1%gcc

  buhe32j    xz@5.2.4%gcc

  dpawgwu    zlib@1.2.8%gcc

  6fcmnpp    zlib@1.2.8%gcc cppflags="-O3" 

  av3mmgf    zlib@1.2.11%gcc

Spack models the dependencies of packages as a directed acyclic graph
(DAG). The ``spack find -d`` command shows the tree representation of
that graph.  We can also use the ``spack graph`` command to view the entire
DAG as a graph.

.. code-block:: console

  $ spack graph hdf5+hl+mpi ^mpich
  o  hdf5
  |\
  o |  zlib
  /
  o  mpich
  o  findutils
  |\
  | |\
  | | |\
  | | | |\
  o | | | |  texinfo
  | | | o |  automake
  | |_|/| | 
  |/| | | | 
  | | | |/
  | | | o  autoconf
  | |_|/| 
  |/| |/
  | |/| 
  o | |  perl
  o | |  gdbm
  o | |  readline
  o | |  ncurses
  o | |  pkgconf
  / /
  | o  libtool
  |/
  o  m4
  o  libsigsegv

You may also have noticed that there are some packages shown in the
``spack find -d`` output that we didn't install explicitly. These are
dependencies that were installed implicitly. A few packages installed
implicitly are not shown as dependencies in the ``spack find -d``
output. These are build dependencies. For example, ``libpciaccess`` is
a dependency of openmpi and requires ``m4`` to build. Spack will build
``m4`` as part of the installation of ``openmpi``, but it is not shown
as a dependency in the ``spack find -d`` output because it is not
linked in at run time. Spack handles build dependencies differently
because of their different (less strict) consistency requirements. 

``HDF5`` is more complicated than our basic example of zlib and
openssl, but it's still within the realm of software that an experienced
HPC user could reasonably expect to install given a bit of time. Now
let's look at an even more complicated package.

.. code-block:: console

  $ spack install trilinos
  ==> Installing diffutils
  ==> Searching for binary cache of diffutils
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing diffutils from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/diffutils-3.6/linux-ubuntu18.04-x86_64-gcc-7.3.0-diffutils-3.6-cj7oc5hii5l5karvq4t5adcde2wueh6u.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:25:44 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed diffutils from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/diffutils-3.6-cj7oc5hii5l5karvq4t5adcde2wueh6u
  ==> Installing bzip2
  ==> Searching for binary cache of bzip2
  ==> Installing bzip2 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/bzip2-1.0.6/linux-ubuntu18.04-x86_64-gcc-7.3.0-bzip2-1.0.6-4orv5thyrbaev7odgm5g6r3ungzj5yxv.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:04:35 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed bzip2 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/bzip2-1.0.6-4orv5thyrbaev7odgm5g6r3ungzj5yxv
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi
  ==> Installing boost
  ==> Searching for binary cache of boost
  ==> Installing boost from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/boost-1.68.0/linux-ubuntu18.04-x86_64-gcc-7.3.0-boost-1.68.0-6sfdq2hey6zrvfozln6tekynrqdd7ilw.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:06:58 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed boost from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/boost-1.68.0-6sfdq2hey6zrvfozln6tekynrqdd7ilw
  ==> pkgconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/pkgconf-1.4.2-gavqfquorv7kyfjbib5w3w5odhfkuggc
  ==> ncurses is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/ncurses-6.1-c4iq7eli75yuf5rkigpk7is63eurr6rp
  ==> readline is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/readline-7.0-lg4ce4zttwtp6ajkdhyw62rx2i4ctpvl
  ==> gdbm is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/gdbm-1.14.1-64j7o2pwuhpt5yurbcheljveamvpyfsl
  ==> perl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/perl-5.26.2-kpukrzpbnqfob42y5lpffsc6bksqee7h
  ==> Installing openssl
  ==> Searching for binary cache of openssl
  ==> Installing openssl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/openssl-1.0.2o/linux-ubuntu18.04-x86_64-gcc-7.3.0-openssl-1.0.2o-pa4pdntn53dnoix7lxy2xj7b2nrbkg3g.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:46:13 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed openssl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/openssl-1.0.2o-pa4pdntn53dnoix7lxy2xj7b2nrbkg3g
  ==> Installing cmake
  ==> Searching for binary cache of cmake
  ==> Installing cmake from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/cmake-3.12.3/linux-ubuntu18.04-x86_64-gcc-7.3.0-cmake-3.12.3-2r7i4lbc4xcbd342rwcmm3ungaraukuz.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:46:49 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed cmake from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/cmake-3.12.3-2r7i4lbc4xcbd342rwcmm3ungaraukuz
  ==> Installing glm
  ==> Searching for binary cache of glm
  ==> Installing glm from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/glm-0.9.7.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-glm-0.9.7.1-ijgngc3jpc7ifmpek3wff2fevmg33k3u.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:15:25 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed glm from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/glm-0.9.7.1-ijgngc3jpc7ifmpek3wff2fevmg33k3u
  ==> libsigsegv is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libsigsegv-2.11-oromhtnsg3whjgy4ufgufwwwxe3iadp7
  ==> m4 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/m4-1.4.18-vypfbpxo4do2ieh3hf7fbxpyz66b5zav
  ==> libtool is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libtool-2.4.6-jher54m7efbgqjarpywxcb3yxmelyswk
  ==> util-macros is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/util-macros-1.19.1-325c2mbwiy55522757xear34254ihlub
  ==> libpciaccess is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libpciaccess-0.13.5-7x2dp3quycimjbqwi6plzfi5huj2xnef
  ==> xz is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/xz-5.2.4-buhe32jt3hgxzvpi4hzsiwoo7kbecfjq
  ==> libxml2 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libxml2-2.9.8-xhsbjjjj4jdo5vv4nszwu5edip4fhebh
  ==> autoconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/autoconf-2.69-7mf25r4qp3msoto4peybu677rxe622re
  ==> automake is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/automake-1.16.1-p2omviwtyjez7ba5cfhofw3tlr5l7jog
  ==> numactl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/numactl-2.0.11-jvoj2ptukcmnqwenwjljytzmtfyezxvs
  ==> hwloc is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hwloc-1.11.9-uslokkifia23o3n4ne4r72owoyx2dynb
  ==> openmpi is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/openmpi-3.1.3-tfegwcywpztpm57cl44hxf64kbckdjmu
  ==> Installing hdf5
  ==> Searching for binary cache of hdf5
  ==> Installing hdf5 from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4/linux-ubuntu18.04-x86_64-gcc-7.3.0-hdf5-1.10.4-j62lfgyl7c3xe3knxyzpvg5byzdrrhqv.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:13:02 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hdf5 from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4-j62lfgyl7c3xe3knxyzpvg5byzdrrhqv
  ==> Installing openblas
  ==> Searching for binary cache of openblas
  ==> Installing openblas from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/openblas-0.3.3/linux-ubuntu18.04-x86_64-gcc-7.3.0-openblas-0.3.3-yhseekqc2vd4mcg3fjso7gwedvlcbgyt.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:13:46 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed openblas from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/openblas-0.3.3-yhseekqc2vd4mcg3fjso7gwedvlcbgyt
  ==> Installing hypre
  ==> Searching for binary cache of hypre
  ==> Installing hypre from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/hypre-2.15.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-hypre-2.15.1-qmggyor2ch6mdavtu3nt47y62frxkpvp.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:45:54 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hypre from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hypre-2.15.1-qmggyor2ch6mdavtu3nt47y62frxkpvp
  ==> Installing matio
  ==> Searching for binary cache of matio
  ==> Installing matio from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/matio-1.5.9/linux-ubuntu18.04-x86_64-gcc-7.3.0-matio-1.5.9-2i447ydxxb2rkgdip27j5qhddnssipb3.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:13:50 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed matio from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/matio-1.5.9-2i447ydxxb2rkgdip27j5qhddnssipb3
  ==> Installing metis
  ==> Searching for binary cache of metis
  ==> Installing metis from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/metis-5.1.0/linux-ubuntu18.04-x86_64-gcc-7.3.0-metis-5.1.0-efcmkg7mh3tdvxa4wihkb2mvmwyrqcrv.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:13:24 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed metis from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/metis-5.1.0-efcmkg7mh3tdvxa4wihkb2mvmwyrqcrv
  ==> Installing netlib-scalapack
  ==> Searching for binary cache of netlib-scalapack
  ==> Installing netlib-scalapack from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/netlib-scalapack-2.0.2/linux-ubuntu18.04-x86_64-gcc-7.3.0-netlib-scalapack-2.0.2-dlmeefzhqipuwl4owhieyysae6rr5qwg.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:13:06 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed netlib-scalapack from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/netlib-scalapack-2.0.2-dlmeefzhqipuwl4owhieyysae6rr5qwg
  ==> Installing mumps
  ==> Searching for binary cache of mumps
  ==> Installing mumps from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/mumps-5.1.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-mumps-5.1.1-v2ixotr77j5jvcnzij5tfltaubtumcj4.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:27:15 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed mumps from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/mumps-5.1.1-v2ixotr77j5jvcnzij5tfltaubtumcj4
  ==> Installing netcdf
  ==> Searching for binary cache of netcdf
  ==> Installing netcdf from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/netcdf-4.6.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-netcdf-4.6.1-27tbthghj3jv7eb4vf7jeiqekhdqcr3l.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:03:36 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed netcdf from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/netcdf-4.6.1-27tbthghj3jv7eb4vf7jeiqekhdqcr3l
  ==> Installing parmetis
  ==> Searching for binary cache of parmetis
  ==> Installing parmetis from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/parmetis-4.0.3/linux-ubuntu18.04-x86_64-gcc-7.3.0-parmetis-4.0.3-tkah54bzprrucyfcncqq4pttbl7vjjlx.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:14:00 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed parmetis from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/parmetis-4.0.3-tkah54bzprrucyfcncqq4pttbl7vjjlx
  ==> Installing suite-sparse
  ==> Searching for binary cache of suite-sparse
  ==> Installing suite-sparse from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/suite-sparse-5.3.0/linux-ubuntu18.04-x86_64-gcc-7.3.0-suite-sparse-5.3.0-y2424h57ll3r75ievmqc56dwk7gfm7rh.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:12:07 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed suite-sparse from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/suite-sparse-5.3.0-y2424h57ll3r75ievmqc56dwk7gfm7rh
  ==> Installing trilinos
  ==> Searching for binary cache of trilinos
  ==> Installing trilinos from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/trilinos-12.12.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-trilinos-12.12.1-gewozsklxkt5girwxttucevh5p2rtjob.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:57:01 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed trilinos from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/trilinos-12.12.1-gewozsklxkt5girwxttucevh5p2rtjob

Now we're starting to see the power of Spack. Trilinos has 11 top
level dependecies, many of which have dependencies of their
own. Installing more complex packages can take days or weeks even for
an experienced user. Although we've done a binary installation for the
tutorial, a source installation of trilinos using Spack takes about 3
hours (depending on the system), but only 20 seconds of programmer
time.

Spack manages constistency of the entire DAG. Every MPI dependency will
be satisfied by the same configuration of MPI, etc. If we install
``trilinos`` again specifying a dependency on our previous HDF5 built
with ``mpich``:

.. code-block:: console

  $ spack install --use-cache trilinos +hdf5 ^hdf5+hl+mpi ^mpich
  ==> diffutils is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/diffutils-3.6-cj7oc5hii5l5karvq4t5adcde2wueh6u
  ==> bzip2 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/bzip2-1.0.6-4orv5thyrbaev7odgm5g6r3ungzj5yxv
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi
  ==> boost is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/boost-1.68.0-6sfdq2hey6zrvfozln6tekynrqdd7ilw
  ==> pkgconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/pkgconf-1.4.2-gavqfquorv7kyfjbib5w3w5odhfkuggc
  ==> ncurses is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/ncurses-6.1-c4iq7eli75yuf5rkigpk7is63eurr6rp
  ==> readline is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/readline-7.0-lg4ce4zttwtp6ajkdhyw62rx2i4ctpvl
  ==> gdbm is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/gdbm-1.14.1-64j7o2pwuhpt5yurbcheljveamvpyfsl
  ==> perl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/perl-5.26.2-kpukrzpbnqfob42y5lpffsc6bksqee7h
  ==> openssl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/openssl-1.0.2o-pa4pdntn53dnoix7lxy2xj7b2nrbkg3g
  ==> cmake is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/cmake-3.12.3-2r7i4lbc4xcbd342rwcmm3ungaraukuz
  ==> glm is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/glm-0.9.7.1-ijgngc3jpc7ifmpek3wff2fevmg33k3u
  ==> libsigsegv is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libsigsegv-2.11-oromhtnsg3whjgy4ufgufwwwxe3iadp7
  ==> m4 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/m4-1.4.18-vypfbpxo4do2ieh3hf7fbxpyz66b5zav
  ==> autoconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/autoconf-2.69-7mf25r4qp3msoto4peybu677rxe622re
  ==> automake is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/automake-1.16.1-p2omviwtyjez7ba5cfhofw3tlr5l7jog
  ==> libtool is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libtool-2.4.6-jher54m7efbgqjarpywxcb3yxmelyswk
  ==> texinfo is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/texinfo-6.5-onnlt2r2gnjths3f2w4otltihd4p2s5h
  ==> findutils is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/findutils-4.6.0-capl6zymtrqxltqnfqiykagcciyumy6z
  ==> mpich is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/mpich-3.2.1-yf2xknkwvuopv7bslicv4x66fd4ntpbc
  ==> hdf5 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4-qtza2jxt57pcimpjomr5zxveonvfadap
  ==> openblas is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/openblas-0.3.3-yhseekqc2vd4mcg3fjso7gwedvlcbgyt
  ==> Installing hypre
  ==> Searching for binary cache of hypre
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing hypre from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/hypre-2.15.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-hypre-2.15.1-kdenuxtjlnqaz3m3uy6nh2gllkdkhzq3.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:12:23 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed hypre from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hypre-2.15.1-kdenuxtjlnqaz3m3uy6nh2gllkdkhzq3
  ==> Installing matio
  ==> Searching for binary cache of matio
  ==> Installing matio from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/matio-1.5.9/linux-ubuntu18.04-x86_64-gcc-7.3.0-matio-1.5.9-fego2zhdipiybn3mri7oi6ikzjaoywep.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:27:14 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed matio from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/matio-1.5.9-fego2zhdipiybn3mri7oi6ikzjaoywep
  ==> metis is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/metis-5.1.0-efcmkg7mh3tdvxa4wihkb2mvmwyrqcrv
  ==> Installing netlib-scalapack
  ==> Searching for binary cache of netlib-scalapack
  ==> Installing netlib-scalapack from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/netlib-scalapack-2.0.2/linux-ubuntu18.04-x86_64-gcc-7.3.0-netlib-scalapack-2.0.2-nz5mzhstb7lfnobzwuye65uonn67agyh.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:58:05 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed netlib-scalapack from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/netlib-scalapack-2.0.2-nz5mzhstb7lfnobzwuye65uonn67agyh
  ==> Installing mumps
  ==> Searching for binary cache of mumps
  ==> Installing mumps from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/mumps-5.1.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-mumps-5.1.1-pki3jrzhxkkvjllug465uq64slzqdizm.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:13:29 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed mumps from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/mumps-5.1.1-pki3jrzhxkkvjllug465uq64slzqdizm
  ==> Installing netcdf
  ==> Searching for binary cache of netcdf
  ==> Installing netcdf from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/netcdf-4.6.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-netcdf-4.6.1-amcwqsk3ah4fqh67iljj4axzxxtevxck.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 00:57:18 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed netcdf from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/netcdf-4.6.1-amcwqsk3ah4fqh67iljj4axzxxtevxck
  ==> Installing parmetis
  ==> Searching for binary cache of parmetis
  ==> Installing parmetis from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/parmetis-4.0.3/linux-ubuntu18.04-x86_64-gcc-7.3.0-parmetis-4.0.3-usnl2ga47ycfd32med3xgw6vxp2atizv.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:27:48 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed parmetis from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/parmetis-4.0.3-usnl2ga47ycfd32med3xgw6vxp2atizv
  ==> suite-sparse is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/suite-sparse-5.3.0-y2424h57ll3r75ievmqc56dwk7gfm7rh
  ==> Installing trilinos
  ==> Searching for binary cache of trilinos
  ==> Installing trilinos from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/trilinos-12.12.1/linux-ubuntu18.04-x86_64-gcc-7.3.0-trilinos-12.12.1-g5kay24y3iyykgp4o7tq4vvh6bfnq3ry.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:24:53 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed trilinos from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/trilinos-12.12.1-g5kay24y3iyykgp4o7tq4vvh6bfnq3ry

We see that every package in the trilinos DAG that depends on MPI now
uses ``mpich``.

.. code-block:: console

  $ spack find -d trilinos
  ==> 2 installed packages.
  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
      trilinos@12.12.1
	  ^boost@1.68.0
	      ^bzip2@1.0.6
	      ^zlib@1.2.11
	  ^glm@0.9.7.1
	  ^hdf5@1.10.4
	      ^openmpi@3.1.3
		  ^hwloc@1.11.9
		      ^libpciaccess@0.13.5
		      ^libxml2@2.9.8
			  ^xz@5.2.4
		      ^numactl@2.0.11
	  ^hypre@2.15.1
	      ^openblas@0.3.3
	  ^matio@1.5.9
	  ^metis@5.1.0
	  ^mumps@5.1.1
	      ^netlib-scalapack@2.0.2
	  ^netcdf@4.6.1
	  ^parmetis@4.0.3
	  ^suite-sparse@5.3.0

      trilinos@12.12.1
	  ^boost@1.68.0
	      ^bzip2@1.0.6
	      ^zlib@1.2.11
	  ^glm@0.9.7.1
	  ^hdf5@1.10.4
	      ^mpich@3.2.1
	  ^hypre@2.15.1
	      ^openblas@0.3.3
	  ^matio@1.5.9
	  ^metis@5.1.0
	  ^mumps@5.1.1
	      ^netlib-scalapack@2.0.2
	  ^netcdf@4.6.1
	  ^parmetis@4.0.3
          ^suite-sparse@5.3.0

As we discussed before, the ``spack find -d`` command shows the
dependency information as a tree. While that is often sufficient, many
complicated packages, including trilinos, have dependencies that
cannot be fully represented as a tree. Again, the ``spack graph``
command shows the full DAG of the dependency information.

.. code-block:: console

  $ spack graph trilinos
o  trilinos
|\
| |\
| | |\
| | | |\
| | | | |\
| | | | | |\
| | | | | | |\
| | | | | | | |\
| | | | | | | | |\
| | | | | | | | | |\
| | | | | | | | | | |\
| | | | | | | | | | | |\
| | | | | | | | | | | | |\
o | | | | | | | | | | | | |  suite-sparse
|\ \ \ \ \ \ \ \ \ \ \ \ \ \
| |_|_|/ / / / / / / / / / /
|/| | | | | | | | | | | | | 
| |\ \ \ \ \ \ \ \ \ \ \ \ \
| | |_|_|_|_|_|/ / / / / / /
| |/| | | | | | | | | | | | 
| | | |_|_|_|_|_|_|_|/ / /
| | |/| | | | | | | | | | 
| | | o | | | | | | | | |  parmetis
| | |/| | | | | | | | | | 
| |/|/| | | | | | | | | | 
| | | |/ / / / / / / / /
| | | | | | o | | | | |  mumps
| |_|_|_|_|/| | | | | | 
|/| | | |_|/| | | | | | 
| | | |/| |/ / / / / /
| | | | |/| | | | | | 
| | | | o | | | | | |  netlib-scalapack
| |_|_|/| | | | | | | 
|/| | |/| | | | | | | 
| | |/|/ / / / / / /
| o | | | | | | | |  metis
| |/ / / / / / / /
| | | | | | | o |  glm
| | |_|_|_|_|/ /
| |/| | | | | | 
| o | | | | | |  cmake
| |\ \ \ \ \ \ \
| o | | | | | | |  openssl
| |\ \ \ \ \ \ \ \
| | | | | o | | | |  netcdf
| | |_|_|/| | | | | 
| |/| | |/| | | | | 
| | | | | |\ \ \ \ \
| | | | | | | |_|/ /
| | | | | | |/| | | 
| | | | | | | o | |  matio
| | |_|_|_|_|/| | | 
| |/| | | | |/ / /
| | | | | | | o |  hypre
| |_|_|_|_|_|/| | 
|/| | | | |_|/ /
| | | | |/| | | 
| | | | | | o |  hdf5
| | |_|_|_|/| | 
| |/| | | |/ /
| | | | |/| | 
| | | | o | |  openmpi
| | |_|/| | | 
| |/| | | | | 
| | | | |\ \ \
| | | | | o | |  hwloc
| | | | |/| | | 
| | | | | |\ \ \
| | | | | | |\ \ \
| | | | | | o | | |  libxml2
| | |_|_|_|/| | | | 
| |/| | | |/| | | | 
| | | | | | | | | o  boost
| | |_|_|_|_|_|_|/| 
| |/| | | | | | | | 
| o | | | | | | | |  zlib
|  / / / / / / / /
| | | | | o | | |  xz
| | | | |  / / /
| | | | | o | |  libpciaccess
| | | | |/| | | 
| | | | | |\ \ \
| | | | | o | | |  util-macros
| | | | |  / / /
| | | o | | | |  numactl
| | | |\ \ \ \ \
| | | | |_|_|/ /
| | | |/| | | | 
| | | | |\ \ \ \
| | | | | |_|/ /
| | | | |/| | | 
| | | | | |\ \ \
| | | | | o | | |  automake
| | |_|_|/| | | | 
| |/| | | | | | | 
| | | | | |/ / /
| | | | | o | |  autoconf
| | |_|_|/| | | 
| |/| | |/ / /
| | | |/| | | 
| o | | | | |  perl
| o | | | | |  gdbm
| o | | | | |  readline
| |/ / / / /
| o | | | |  ncurses
| | |_|/ /
| |/| | | 
| o | | |  pkgconf
|  / / /
o | | |  openblas
 / / /
| o |  libtool
|/ /
o |  m4
o |  libsigsegv
 /
o  bzip2
o  diffutils

You can control how the output is displayed with a number of options.

The ASCII output from ``spack graph`` can be difficult to parse for
complicated packages. The output can be changed to the ``graphviz``
``.dot`` format using the ``--dot`` flag.

.. code-block:: console

  $ spack graph --dot trilinos | dot -Tpdf trilinos_graph.pdf

.. _basics-tutorial-uninstall:

---------------------
Uninstalling Packages
---------------------

Earlier we installed many configurations each of zlib and
openssl. Now we will go through and uninstall some of those packages
that we didn't really need.

.. code-block:: console

  $ spack find -d openssl
  ==> 3 installed packages.
  -- linux-ubuntu18.04-x86_64 / clang@6.0.0-1ubuntu2 --------------
      tcl@8.6.8
          ^zlib@1.2.8


  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
      tcl@8.6.8
          ^zlib@1.2.11

      tcl@8.6.8
          ^zlib@1.2.8
	
  $ spack find zlib
  ==> 6 installed packages.
  -- linux-ubuntu18.04-x86_64 / clang@6.0.0-1ubuntu2 --------------
  zlib@1.2.8  zlib@1.2.11

  -- linux-ubuntu18.04-x86_64 / gcc@6.4 ---------------------------
  zlib@1.2.11

  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
  zlib@1.2.8  zlib@1.2.8  zlib@1.2.11

We can uninstall packages by spec using the same syntax as install.

.. code-block:: console

  $ spack uninstall zlib %gcc@4.7
  ==> The following packages will be uninstalled:

  -- linux-ubuntu18.04-x86_64 / gcc@6.4 ---------------------------
  ul42kj4 zlib@1.2.11%gcc+optimize+pic+shared

  ==> Do you want to proceed? [y/N] y
  ==> Successfully uninstalled zlib@1.2.11%gcc@6.4+optimize+pic+shared arch=linux-ubuntu18.04-x86_64 /ul42kj4

  $ spack find -lf zlib
  ==> 5 installed packages.
  -- linux-ubuntu18.04-x86_64 / clang@6.0.0-1ubuntu2 --------------
  4z4djeo zlib@1.2.8%clang

  37pzrwc zlib@1.2.11%clang


  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
  dpawgwu zlib@1.2.8%gcc

  6fcmnpp zlib@1.2.8%gcc cppflags="-O3" 

  av3mmgf zlib@1.2.11%gcc

We can also uninstall packages by referring only to their hash.

We can use either ``-f`` (force) or ``-R`` (remove dependents as well) to
remove packages that are required by another installed package.

.. code-block:: console

  spack uninstall zlib/4z4d
  ==> Error: Will not uninstall zlib@1.2.8%clang@6.0.0-1ubuntu2/4z4djeo

  The following packages depend on it:
  -- linux-ubuntu18.04-x86_64 / clang@6.0.0-1ubuntu2 --------------
  5u7fuxk tcl@8.6.8%clang


  ==> Error: Use `spack uninstall --dependents` to uninstall these dependencies as well.
  $ spack uninstall -R zlib/4z4d
  ==> The following packages will be uninstalled:

  -- linux-ubuntu18.04-x86_64 / clang@6.0.0-1ubuntu2 --------------
  5u7fuxk tcl@8.6.8%clang

  4z4djeo zlib@1.2.8%clang+optimize+pic+shared

  ==> Do you want to proceed? [y/N] y
  ==> Successfully uninstalled tcl@8.6.8%clang@6.0.0-1ubuntu2 arch=linux-ubuntu18.04-x86_64 /5u7fuxk
  ==> Successfully uninstalled zlib@1.2.8%clang@6.0.0-1ubuntu2+optimize+pic+shared arch=linux-ubuntu18.04-x86_64 /4z4djeo

Spack will not uninstall packages that are not sufficiently
specified. The ``-a`` (all) flag can be used to uninstall multiple
packages at once.

.. code-block:: console

  $ spack uninstall trilinos
  ==> Error: trilinos matches multiple packages:

  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
  gewozsk trilinos@12.12.1%gcc~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2

  g5kay24 trilinos@12.12.1%gcc~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2


  ==> Error: You can either:
      a) use a more specific spec, or
      b) use `spack uninstall --all` to uninstall ALL matching specs.

  $ spack uninstall /gewo
  ==> The following packages will be uninstalled:
  
  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
  gewozsk trilinos@12.12.1%gcc~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2

  ==> Do you want to proceed? [y/N] y
  ==> Successfully uninstalled trilinos@12.12.1%gcc@7.3.0~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2~intrepid~intrepid2~isorropia+kokkos+metis~minitensor+ml+muelu+mumps~nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2 arch=linux-ubuntu18.04-x86_64 /gewozsk

-----------------------------
Advanced ``spack find`` Usage
-----------------------------

We will go over some additional uses for the ``spack find`` command not
already covered in the :ref:`basics-tutorial-install` and
:ref:`basics-tutorial-uninstall` sections.

The ``spack find`` command can accept what we call "anonymous specs."
These are expressions in spec syntax that do not contain a package
name. For example, ``spack find ^mpich`` will return every installed
package that depends on mpich, and ``spack find cppflags="-O3"`` will
return every package which was built with ``cppflags="-O3"``.

.. code-block:: console

  $ spack find ^mpich
  ==> 8 installed packages.
  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
  hdf5@1.10.4  hypre@2.15.1  matio@1.5.9  mumps@5.1.1  netcdf@4.6.1  netlib-scalapack@2.0.2  parmetis@4.0.3  trilinos@12.12.1

  $ spack find cppflags=-O3
  ==> 1 installed packages.
  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
  zlib@1.2.8

The ``find`` command can also show which packages were installed
explicitly (rather than pulled in as a dependency) using the ``-e``
flag. The ``-E`` flag shows implicit installs only. The ``find`` command can
also show the path to which a spack package was installed using the ``-p``
command.

.. code-block:: console

  $ spack find -pe
  ==> 10 installed packages.
  -- linux-ubuntu18.04-x86_64 / clang@6.0.0-1ubuntu2 --------------
      zlib@1.2.11  /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/clang-6.0.0-1ubuntu2/zlib-1.2.11-37pzrwcovpu5wxaldr5l4eg6i255dv4h

  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
      hdf5@1.10.4       /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4-uggv4drbokmhq6bhlkftbvoeneaj5do4
      hdf5@1.10.4       /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4-z33coumgesxxse2zr2k5bffvnyhjl2t7
      hdf5@1.10.4       /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/hdf5-1.10.4-qtza2jxt57pcimpjomr5zxveonvfadap
      tcl@8.6.8         /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/tcl-8.6.8-ddd4sqiwshbudadbap3nangd3iobx5c6
      tcl@8.6.8         /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/tcl-8.6.8-ua7zdu4dlg2n2yvszxfymk4i6ayrjere
      trilinos@12.12.1  /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/trilinos-12.12.1-g5kay24y3iyykgp4o7tq4vvh6bfnq3ry
      zlib@1.2.8        /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.8-dpawgwuohqphts4z7vyrmzzrw6ljfvlg
      zlib@1.2.8        /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.8-6fcmnppflzf6ia3yk7t32uw5wjyy64jg
      zlib@1.2.11       /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi

---------------------
Customizing Compilers
---------------------


Spack manages a list of available compilers on the system, detected
automatically from from the user's ``PATH`` variable. The ``spack
compilers`` command is an alias for the command ``spack compiler list``.

.. code-block:: console

  $ spack compilers
  ==> Available compilers
  -- clang ubuntu18.04-x86_64 -------------------------------------
  clang@6.0.0-1ubuntu2

  -- gcc ubuntu18.04-x86_64 ---------------------------------------
  gcc@7.3.0  gcc@6.4.0  ==> Available compilers

The compilers are maintained in a YAML file. Later in the tutorial you
will learn how to configure compilers by hand for special cases. Spack
also has tools to add compilers, and compilers built with Spack can be
added to the configuration.

.. code-block:: console

  $ spack install gcc@7.2.0
  ==> libsigsegv is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libsigsegv-2.11-oromhtnsg3whjgy4ufgufwwwxe3iadp7
  ==> m4 is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/m4-1.4.18-vypfbpxo4do2ieh3hf7fbxpyz66b5zav
  ==> pkgconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/pkgconf-1.4.2-gavqfquorv7kyfjbib5w3w5odhfkuggc
  ==> ncurses is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/ncurses-6.1-c4iq7eli75yuf5rkigpk7is63eurr6rp
  ==> readline is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/readline-7.0-lg4ce4zttwtp6ajkdhyw62rx2i4ctpvl
  ==> gdbm is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/gdbm-1.14.1-64j7o2pwuhpt5yurbcheljveamvpyfsl
  ==> perl is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/perl-5.26.2-kpukrzpbnqfob42y5lpffsc6bksqee7h
  ==> autoconf is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/autoconf-2.69-7mf25r4qp3msoto4peybu677rxe622re
  ==> automake is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/automake-1.16.1-p2omviwtyjez7ba5cfhofw3tlr5l7jog
  ==> libtool is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/libtool-2.4.6-jher54m7efbgqjarpywxcb3yxmelyswk
  ==> Installing gmp
  ==> Searching for binary cache of gmp
  ==> Finding buildcaches in /mirror/build_cache
  ==> Installing gmp from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/gmp-6.1.2/linux-ubuntu18.04-x86_64-gcc-7.3.0-gmp-6.1.2-qtpajf64xicepymcwmp7nasehc6v4x67.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:09:15 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed gmp from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/gmp-6.1.2-qtpajf64xicepymcwmp7nasehc6v4x67
  ==> Installing isl
  ==> Searching for binary cache of isl
  ==> Installing isl from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/isl-0.18/linux-ubuntu18.04-x86_64-gcc-7.3.0-isl-0.18-pkhrxvvkn2it3md4evarstouxqc62zsi.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:04:39 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed isl from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/isl-0.18-pkhrxvvkn2it3md4evarstouxqc62zsi
  ==> Installing mpfr
  ==> Searching for binary cache of mpfr
  ==> Installing mpfr from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/mpfr-3.1.6/linux-ubuntu18.04-x86_64-gcc-7.3.0-mpfr-3.1.6-qzj4nmvgfwe5ayksgbd6o6fqnkssno2r.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:14:29 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed mpfr from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/mpfr-3.1.6-qzj4nmvgfwe5ayksgbd6o6fqnkssno2r
  ==> Installing mpc
  ==> Searching for binary cache of mpc
  ==> Installing mpc from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/mpc-1.1.0/linux-ubuntu18.04-x86_64-gcc-7.3.0-mpc-1.1.0-nmqvwidcia55i7tgc6pexgxmytjl5b7h.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:10:36 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed mpc from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/mpc-1.1.0-nmqvwidcia55i7tgc6pexgxmytjl5b7h
  ==> zlib is already installed in /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/zlib-1.2.11-av3mmgf66zwic2i34n7o2oxtp4quy6pi
  ==> Installing gcc
  ==> Searching for binary cache of gcc
  ==> Installing gcc from binary cache
  ==> Fetching file:///mirror/build_cache/linux-ubuntu18.04-x86_64/gcc-7.3.0/gcc-7.2.0/linux-ubuntu18.04-x86_64-gcc-7.3.0-gcc-7.2.0-cia4pv3am36temh73zppwija77ytzyom.spack
  ########################################################################################################################### 100.0%
  gpg: Signature made Thu Nov  8 01:03:25 2018 UTC
  gpg:                using RSA key 95C717877AC00FFDAA8FD6E99CFA4A453B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Successfully installed gcc from binary cache
  [+] /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/gcc-7.2.0-cia4pv3am36temh73zppwija77ytzyom

  $ spack find -p gcc
  ==> 1 installed packages.
  -- linux-ubuntu18.04-x86_64 / gcc@7.3.0 -------------------------
      gcc@7.2.0  /home/spack1/spack/opt/spack/linux-ubuntu18.04-x86_64/gcc-7.3.0/gcc-7.2.0-cia4pv3am36temh73zppwija77ytzyom

We can add gcc to Spack as an available compiler using the ``spack
compiler add`` command. This will allow future packages to build with
gcc@7.2.0.

.. code-block:: console

  $ spack compiler add `spack location -i gcc@7.2.0`
  ==> Added 1 new compiler to /home/spack1/.spack/linux/compilers.yaml
      gcc@7.2.0
  ==> Compilers are defined in the following files:
      /home/spack1/.spack/linux/compilers.yaml

We can also remove compilers from our configuration using ``spack compiler remove <compiler_spec>``

.. code-block:: console

  $ spack compiler remove gcc@7.2.0
  ==> Removed compiler gcc@7.2.0
