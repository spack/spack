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

  $ git clone https://github.com/spack/spack
  Cloning into 'spack'...
  remote: Counting objects: 94561, done.
  remote: Compressing objects: 100% (121/121), done.
  remote: Total 94561 (delta 91), reused 121 (delta 48), pack-reused 94368
  Receiving objects: 100% (94561/94561), 32.44 MiB | 31.88 MiB/s, done.
  Resolving deltas: 100% (44914/44914), done.
  Checking connectivity... done.
  $ cd spack
  $ git checkout releases/v0.11.2
  Branch releases/v0.11.2 set up to track remote branch releases/v0.11.2 from origin.
  Switched to a new branch 'releases/v0.11.2'

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
  ==> 2177 packages.
  abinit                           libepoxy                               py-html5lib                     r-ncdf4
  abyss                            libevent                               py-httpbin                      r-network
  ack                              libevpath                              py-hypothesis                   r-networkd3abinit
  ...

The ``spack list`` command can also take a query string. Spack
automatically adds wildcards to both ends of the string. For example,
we can view all available python packages.

.. code-block:: console

  $ spack list py-
  ==> 356 packages.
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
  ==> Fetching file:///home/ubuntu/becker/buildcache/zlib/zlib-1.2.11.tar.gz
  curl: (37) Couldn't open file /home/ubuntu/becker/buildcache/zlib/zlib-1.2.11.tar.gz
  ==> Fetching from file:///home/ubuntu/becker/buildcache/zlib/zlib-1.2.11.tar.gz failed.
  ==> Fetching http://zlib.net/fossils/zlib-1.2.11.tar.gz
  ######################################################################## 100.0%
  ==> Staging archive: /home/ubuntu/test/spack/var/spack/stage/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb/zlib-1.2.11.tar.gz
  ==> Created stage in /home/ubuntu/test/spack/var/spack/stage/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> No patches needed for zlib
  ==> Building zlib [Package]
  ==> Executing phase: 'install'
  ==> Successfully installed zlib
    Fetch: 0.58s.  Build: 1.15s.  Total: 1.73s.
    [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb

Spack can install software either from source or from a binary
cache. Packages in the binary cache are signed with GPG for
security. For the tutorial we have prepared a binary cache so you
don't have to wait on slow compilation from source. To be able to
install from the binary cache, we will need to trust the GPG key that
the binary cache was prepared with.

.. code-block:: console

  $ spack gpg trust /opt/public.key
  gpg: keybox '/home/ubuntu/test/spack/opt/spack/gpg/pubring.kbx' created
  gpg: /home/ubuntu/test/spack/opt/spack/gpg/trustdb.gpg: trustdb created
  gpg: key 3B7C69B2: public key "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" imported
  gpg: Total number processed: 1
  gpg:               imported: 1

The AWS instances and Docker images we use for the tutorial already
have configuration files in place so that Spack knows where to look
for binary packages (and that's the only change we've made). You'll
learn more about configuring Spack later in the tutorial, but for now
you will be able to install the rest of the packages in the tutorial
from a binary cache by specifying ``spack install --use-cache
<package_name>``. This will install the binary cached version if it
exists and fall back on installing from source.

Spack's spec syntax is the interface by which we can request specific
configurations of the package. The ``%`` sigil is used to specify
compilers.

.. code-block:: console

  $ spack install --use-cache zlib %clang
  ...
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-4.7-libsigsegv-2.11-eaqxu5mka32jpjif32rttiwebimrr2kb.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-util-macros-1.19.1-milz7fmttmptcic2qdk5cnel7ll5sybr.spec.yaml
  ######################################################################## 100.0%
  ==> Installing zlib from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/zlib-1.2.11/linux-ubuntu16.04-x86_64-clang-3.8.0-2ubuntu4-zlib-1.2.11-4pt75q7qq6lygf3hgnona4lyc2uwedul.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:05:02 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed zlib from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/zlib-1.2.11-4pt75q7qq6lygf3hgnona4lyc2uwedul

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

  $ spack install --use-cache zlib@1.2.8
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-clang-3.8.0-2ubuntu4-zlib-1.2.11-4pt75q7qq6lygf3hgnona4lyc2uwedul.spec.yaml
  ######################################################################## 100.0%
  ==> Installing zlib from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8/linux-ubuntu16.04-x86_64-gcc-5.4.0-zlib-1.2.8-bkyl5bhuep6fmhuxzkmhqy25qefjcvzc.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:05:03 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed zlib from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8-bkyl5bhuep6fmhuxzkmhqy25qefjcvzc

  $ spack install --use-cache zlib %gcc@4.7
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-zlib-1.2.8-bkyl5bhuep6fmhuxzkmhqy25qefjcvzc.spec.yaml
  ######################################################################## 100.0%
  ==> Installing zlib from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-4.7/zlib-1.2.11/linux-ubuntu16.04-x86_64-gcc-4.7-zlib-1.2.11-bq2wtdxakpjytk2tjr7qu23i4py2fi2r.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:03:00 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed zlib from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-4.7/zlib-1.2.11-bq2wtdxakpjytk2tjr7qu23i4py2fi2r

The spec syntax also includes compiler flags. Spack accepts
``cppflags``, ``cflags``, ``cxxflags``, ``fflags``, ``ldflags``, and
``ldlibs`` parameters.  The values of these fields must be quoted on
the command line if they include spaces. These values are injected
into the compile line automatically by the Spack compiler wrappers.

.. code-block:: console

  $ spack install --use-cache zlib @1.2.8 cppflags=-O3
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-4.7-zlib-1.2.11-bq2wtdxakpjytk2tjr7qu23i4py2fi2r.spec.yaml
  ######################################################################## 100.0%
  ==> Installing zlib from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8/linux-ubuntu16.04-x86_64-gcc-5.4.0-zlib-1.2.8-64mns5mvdacqvlashkf7v6lqrxixhmxu.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:03:00 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed zlib from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8-64mns5mvdacqvlashkf7v6lqrxixhmxu

The ``spack find`` command is used to query installed packages. Note that
some packages appear identical with the default output. The ``-l`` flag
shows the hash of each package, and the ``-f`` flag shows any non-empty
compiler flags of those packages.

.. code-block:: console

  $ spack find
  ==> 5 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  zlib@1.2.11

  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  zlib@1.2.11

  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  zlib@1.2.8  zlib@1.2.8  zlib@1.2.11


  $ spack find -lf
  ==> 5 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  4pt75q7 zlib@1.2.11%clang


  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  bq2wtdx zlib@1.2.11%gcc


  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  bkyl5bh zlib@1.2.8%gcc

  64mns5m zlib@1.2.8%gcc cppflags="-O3"

  5nus6kn zlib@1.2.11%gcc

Spack generates a hash for each spec. This hash is a function of the full
provenance of the package, so any change to the spec affects the
hash. Spack uses this value to compare specs and to generate unique
installation directories for every combinatorial version. As we move into
more complicated packages with software dependencies, we can see that
Spack reuses existing packages to satisfy a dependency only when the
existing package's hash matches the desired spec.

.. code-block:: console

  $ spack install --use-cache openssl
  ==> zlib is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> Installing openssl
  ==> Searching for binary cache of openssl
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-zlib-1.2.8-64mns5mvdacqvlashkf7v6lqrxixhmxu.spec.yaml
  ######################################################################## 100.0%
  ==> Installing openssl from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2k/linux-ubuntu16.04-x86_64-gcc-5.4.0-openssl-1.0.2k-2woov64m3n4gjtnfp722qcyemzf2qtom.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:03:18 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed openssl from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2k-2woov64m3n4gjtnfp722qcyemzf2qtom

Dependencies can be explicitly requested using the ``^`` sigil. Note that
the spec syntax is recursive. Anything we could specify about the
top-level package, we can also specify about a dependency using ``^``.

.. code-block:: console

  $ spack install --use-cache openssl ^zlib @1.2.8 %clang
  ==> Installing zlib
  ==> Searching for binary cache of zlib
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-openssl-1.0.2k-2woov64m3n4gjtnfp722qcyemzf2qtom.spec.yaml
  ######################################################################## 100.0%
  ==> Installing zlib from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/zlib-1.2.8/linux-ubuntu16.04-x86_64-clang-3.8.0-2ubuntu4-zlib-1.2.8-i426yu3o6lyau5fv5ljwsajfkqxj5rl5.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:03:06 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed zlib from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/zlib-1.2.8-i426yu3o6lyau5fv5ljwsajfkqxj5rl5
  ==> Installing openssl
  ==> Searching for binary cache of openssl
  ==> Installing openssl from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/openssl-1.0.2k/linux-ubuntu16.04-x86_64-clang-3.8.0-2ubuntu4-openssl-1.0.2k-ufruk7kj2fz3oupuat2jbgc2y7hg37vy.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:03:23 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed openssl from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/openssl-1.0.2k-ufruk7kj2fz3oupuat2jbgc2y7hg37vy

Packages can also be referred to from the command line by their package
hash. Using the ``spack find -lf`` command earlier we saw that the hash
of our optimized installation of zlib (``cppflags="-O3"``) began with
``64mns5m``. We can now explicitly build with that package without typing
the entire spec, by using the ``/`` sigil to refer to it by hash. As with
other tools like git, you do not need to specify an *entire* hash on the
command line.  You can specify just enough digits to identify a hash
uniquely.  If a hash prefix is ambiguous (i.e., two or more installed
packages share the prefix) then spack will report an error.

.. code-block:: console

  $ spack install --use-cache openssl ^/64mn
  ==> zlib is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8-64mns5mvdacqvlashkf7v6lqrxixhmxu
  ==> Installing openssl
  ==> Searching for binary cache of openssl
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-clang-3.8.0-2ubuntu4-zlib-1.2.8-i426yu3o6lyau5fv5ljwsajfkqxj5rl5.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-clang-3.8.0-2ubuntu4-openssl-1.0.2k-ufruk7kj2fz3oupuat2jbgc2y7hg37vy.spec.yaml
  ######################################################################## 100.0%
  ==> Installing openssl from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2k/linux-ubuntu16.04-x86_64-gcc-5.4.0-openssl-1.0.2k-gyxmhgbam26d7y42omb7xrvkjjgmzwio.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:03:12 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed openssl from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2k-gyxmhgbam26d7y42omb7xrvkjjgmzwio

The ``spack find`` command can also take a ``-d`` flag, which can show
dependency information. Note that each package has a top-level entry,
even if it also appears as a dependency.

.. code-block:: console

  $ spack find -ldf
  ==> 9 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  ufruk7k    openssl@1.0.2k%clang
  i426yu3        ^zlib@1.2.8%clang

  i426yu3    zlib@1.2.8%clang

  4pt75q7    zlib@1.2.11%clang


  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  bq2wtdx    zlib@1.2.11%gcc


  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  gyxmhgb    openssl@1.0.2k%gcc
  64mns5m        ^zlib@1.2.8%gcc cppflags="-O3"

  2woov64    openssl@1.0.2k%gcc
  5nus6kn        ^zlib@1.2.11%gcc

  bkyl5bh    zlib@1.2.8%gcc

  64mns5m    zlib@1.2.8%gcc cppflags="-O3"

  5nus6kn    zlib@1.2.11%gcc


Let's move on to slightly more complicated packages. ``HDF5`` is a
good example of a more complicated package, with an MPI dependency. If
we install it "out of the box," it will build with ``openmpi``.

.. code-block:: console

  $ spack install --use-cache hdf5
  ==> Installing libsigsegv
  ==> Searching for binary cache of libsigsegv
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-openssl-1.0.2k-gyxmhgbam26d7y42omb7xrvkjjgmzwio.spec.yaml
  ######################################################################## 100.0%
  ==> Installing libsigsegv from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11/linux-ubuntu16.04-x86_64-gcc-5.4.0-libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:21:10 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed libsigsegv from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> Installing m4
  ==> Searching for binary cache of m4
  ==> Installing m4 from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18/linux-ubuntu16.04-x86_64-gcc-5.4.0-m4-1.4.18-r5envx3kqctwwflhd4qax4ahqtt6x43a.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:22:03 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed m4 from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-r5envx3kqctwwflhd4qax4ahqtt6x43a
  ==> Installing libtool
  ==> Searching for binary cache of libtool
  ==> Installing libtool from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/libtool-2.4.6/linux-ubuntu16.04-x86_64-gcc-5.4.0-libtool-2.4.6-o2pfwjf44353ajgr42xqtvzyvqsazkgu.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:29:09 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed libtool from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libtool-2.4.6-o2pfwjf44353ajgr42xqtvzyvqsazkgu
  ==> Installing pkg-config
  ==> Searching for binary cache of pkg-config
  ==> Installing pkg-config from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkg-config-0.29.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-pkg-config-0.29.2-ae2hwm7q57byfbxtymts55xppqwk7ecj.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:30:13 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed pkg-config from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkg-config-0.29.2-ae2hwm7q57byfbxtymts55xppqwk7ecj
  ==> Installing util-macros
  ==> Searching for binary cache of util-macros
  ==> Installing util-macros from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/util-macros-1.19.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-util-macros-1.19.1-milz7fmttmptcic2qdk5cnel7ll5sybr.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:30:12 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed util-macros from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/util-macros-1.19.1-milz7fmttmptcic2qdk5cnel7ll5sybr
  ==> Installing libpciaccess
  ==> Searching for binary cache of libpciaccess
  ==> Installing libpciaccess from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/libpciaccess-0.13.5/linux-ubuntu16.04-x86_64-gcc-5.4.0-libpciaccess-0.13.5-5urc6tcjae26fbbd2wyfohoszhgxtbmc.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:30:23 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed libpciaccess from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libpciaccess-0.13.5-5urc6tcjae26fbbd2wyfohoszhgxtbmc
  ==> Installing xz
  ==> Searching for binary cache of xz
  ==> Installing xz from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/xz-5.2.3/linux-ubuntu16.04-x86_64-gcc-5.4.0-xz-5.2.3-htnq7wqdrqtof6uxqicdj3f7oe3xz6pw.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:30:34 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed xz from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/xz-5.2.3-htnq7wqdrqtof6uxqicdj3f7oe3xz6pw
  ==> zlib is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> Installing libxml2
  ==> Searching for binary cache of libxml2
  ==> Installing libxml2 from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/libxml2-2.9.4/linux-ubuntu16.04-x86_64-gcc-5.4.0-libxml2-2.9.4-sxk64lvcxhqjflzesnf3ye4wakovwi45.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:30:23 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed libxml2 from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libxml2-2.9.4-sxk64lvcxhqjflzesnf3ye4wakovwi45
  ==> Installing hwloc
  ==> Searching for binary cache of hwloc
  ==> Installing hwloc from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hwloc-1.11.8/linux-ubuntu16.04-x86_64-gcc-5.4.0-hwloc-1.11.8-ivg4d2e6anxwin4zbld2g4qlrbuquoyg.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:30:32 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed hwloc from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hwloc-1.11.8-ivg4d2e6anxwin4zbld2g4qlrbuquoyg
  ==> Installing openmpi
  ==> Searching for binary cache of openmpi
  ==> Installing openmpi from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/openmpi-3.0.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-openmpi-3.0.0-yo5qkfvumpmgmvlbalqcadu46j5bd52f.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:43:34 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed openmpi from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openmpi-3.0.0-yo5qkfvumpmgmvlbalqcadu46j5bd52f
  ==> Installing hdf5
  ==> Searching for binary cache of hdf5
  ==> Installing hdf5 from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-hdf5-1.10.1-bovz45ms24pmfr7hlckf56bxegfc4rea.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:53:08 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed hdf5 from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1-bovz45ms24pmfr7hlckf56bxegfc4rea

Spack packages can also have variants. Boolean variants can be specified
using the ``+`` and ``~`` or ``-`` sigils. There are two sigils for
``False`` to avoid conflicts with shell parsing in different
situations. Variants (boolean or otherwise) can also be specified using
the same syntax as compiler flags.  Here we can install HDF5 without MPI
support.

.. code-block:: console

   $ spack install --use-cache hdf5~mpi
   ==> zlib is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
   ==> Installing hdf5
   ==> Searching for binary cache of hdf5
   ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
   ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-openmpi-3.0.0-yo5qkfvumpmgmvlbalqcadu46j5bd52f.spec.yaml
   ######################################################################## 100.0%
   ...
   ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-util-macros-1.19.1-milz7fmttmptcic2qdk5cnel7ll5sybr.spec.yaml
   ######################################################################## 100.0%
   ==> Installing hdf5 from binary cache
   ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-hdf5-1.10.1-pa6oqzfeqzkqkzqr2375fqyt3qggx3tr.spack
   ######################################################################## 100.0%
   gpg: Signature made Sat 11 Nov 2017 12:53:40 AM UTC using RSA key ID 3B7C69B2
   gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
   gpg: WARNING: This key is not certified with a trusted signature!
   gpg:          There is no indication that the signature belongs to the owner.
   Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
   ==> Relocating package from
     /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
   ==> Successfully installed hdf5 from binary cache
   [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1-pa6oqzfeqzkqkzqr2375fqyt3qggx3tr

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

  $ spack install --use-cache hdf5+hl+mpi ^mpich
  ==> Installing mpich
  ==> Searching for binary cache of mpich
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-hdf5-1.10.1-pa6oqzfeqzkqkzqr2375fqyt3qggx3tr.spec.yaml
  ######################################################################## 100.0%
  ==> Installing mpich from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpich-3.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-mpich-3.2-cymrnoowcc4vdyvdnf5ypvob4cmdadk5.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:45:26 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed mpich from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpich-3.2-cymrnoowcc4vdyvdnf5ypvob4cmdadk5
  ==> zlib is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> Installing hdf5
  ==> Searching for binary cache of hdf5
  ==> Installing hdf5 from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-hdf5-1.10.1-e4gz6f2l5ik3ijuk3alwsqplex4tbvin.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:49:45 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed hdf5 from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1-e4gz6f2l5ik3ijuk3alwsqplex4tbvin

We'll do a quick check in on what we have installed so far.

.. code-block:: console

  $ spack find -ldf
  ==> 23 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  ufruk7k    openssl@1.0.2k%clang
  i426yu3        ^zlib@1.2.8%clang

  i426yu3    zlib@1.2.8%clang

  4pt75q7    zlib@1.2.11%clang


  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  bq2wtdx    zlib@1.2.11%gcc


  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  pa6oqzf    hdf5@1.10.1%gcc
  5nus6kn        ^zlib@1.2.11%gcc

  bovz45m    hdf5@1.10.1%gcc
  yo5qkfv        ^openmpi@3.0.0%gcc
  ivg4d2e            ^hwloc@1.11.8%gcc
  5urc6tc                ^libpciaccess@0.13.5%gcc
  sxk64lv                ^libxml2@2.9.4%gcc
  htnq7wq                    ^xz@5.2.3%gcc
  5nus6kn                    ^zlib@1.2.11%gcc

  e4gz6f2    hdf5@1.10.1%gcc
  cymrnoo        ^mpich@3.2%gcc
  5nus6kn        ^zlib@1.2.11%gcc

  ivg4d2e    hwloc@1.11.8%gcc
  5urc6tc        ^libpciaccess@0.13.5%gcc
  sxk64lv        ^libxml2@2.9.4%gcc
  htnq7wq            ^xz@5.2.3%gcc
  5nus6kn            ^zlib@1.2.11%gcc

  5urc6tc    libpciaccess@0.13.5%gcc

  fypapcp    libsigsegv@2.11%gcc

  o2pfwjf    libtool@2.4.6%gcc

  sxk64lv    libxml2@2.9.4%gcc
  htnq7wq        ^xz@5.2.3%gcc
  5nus6kn        ^zlib@1.2.11%gcc

  r5envx3    m4@1.4.18%gcc
  fypapcp        ^libsigsegv@2.11%gcc

  cymrnoo    mpich@3.2%gcc

  yo5qkfv    openmpi@3.0.0%gcc
  ivg4d2e        ^hwloc@1.11.8%gcc
  5urc6tc            ^libpciaccess@0.13.5%gcc
  sxk64lv            ^libxml2@2.9.4%gcc
  htnq7wq                ^xz@5.2.3%gcc
  5nus6kn                ^zlib@1.2.11%gcc

  gyxmhgb    openssl@1.0.2k%gcc
  64mns5m        ^zlib@1.2.8%gcc cppflags="-O3"

  2woov64    openssl@1.0.2k%gcc
  5nus6kn        ^zlib@1.2.11%gcc

  ae2hwm7    pkg-config@0.29.2%gcc

  milz7fm    util-macros@1.19.1%gcc

  htnq7wq    xz@5.2.3%gcc

  bkyl5bh    zlib@1.2.8%gcc

  64mns5m    zlib@1.2.8%gcc cppflags="-O3"

  5nus6kn    zlib@1.2.11%gcc


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

You may also have noticed that there are some packages shown in the
``spack find -d`` output that we didn't install explicitly. These are
dependencies that were installed implicitly. A few packages installed
implicitly are not shown as dependencies in the ``spack find -d``
output. These are build dependencies. For example, ``libpciaccess`` is a
dependency of openmpi and requires ``m4`` to build. Spack will build ``m4`` as
part of the installation of ``openmpi``, but it does not become a part of
the DAG because it is not linked in at run time. Spack handles build
dependencies differently because of their different (less strict)
consistency requirements. It is entirely possible to have two packages
using different versions of a dependency to build, which obviously cannot
be done with linked dependencies.

``HDF5`` is more complicated than our basic example of zlib and
openssl, but it's still within the realm of software that an experienced
HPC user could reasonably expect to install given a bit of time. Now
let's look at an even more complicated package.

.. code-block:: console

  $ spack install --use-cache trilinos
  ==> Installing bzip2
  ==> Searching for binary cache of bzip2
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-hdf5-1.10.1-e4gz6f2l5ik3ijuk3alwsqplex4tbvin.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-mpich-3.2-cymrnoowcc4vdyvdnf5ypvob4cmdadk5.spec.yaml
  ######################################################################## 100.0%
  ==> Installing bzip2 from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/bzip2-1.0.6/linux-ubuntu16.04-x86_64-gcc-5.4.0-bzip2-1.0.6-ufczdvsqt6edesm36xiucyry7myhj7e7.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:39:37 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed bzip2 from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/bzip2-1.0.6-ufczdvsqt6edesm36xiucyry7myhj7e7
  ==> zlib is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> Installing boost
  ==> Searching for binary cache of boost
  ==> Installing boost from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/boost-1.65.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-boost-1.65.1-xxqnbqql5nup7rujer2ury3hsdgcumzb.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:43:14 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed boost from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/boost-1.65.1-xxqnbqql5nup7rujer2ury3hsdgcumzb
  ==> pkg-config is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkg-config-0.29.2-ae2hwm7q57byfbxtymts55xppqwk7ecj
  ==> Installing ncurses
  ==> Searching for binary cache of ncurses
  ==> Installing ncurses from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-ncurses-6.0-ukq4tccptm2rxd56d2bumqthnpcjzlez.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:06:38 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed ncurses from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.0-ukq4tccptm2rxd56d2bumqthnpcjzlez
  ==> openssl is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2k-2woov64m3n4gjtnfp722qcyemzf2qtom
  ==> Installing cmake
  ==> Searching for binary cache of cmake
  ==> Installing cmake from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/cmake-3.9.4/linux-ubuntu16.04-x86_64-gcc-5.4.0-cmake-3.9.4-a2lyofsoxutyy4ihvzopizpbjubtdoem.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 01:22:03 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed cmake from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/cmake-3.9.4-a2lyofsoxutyy4ihvzopizpbjubtdoem
  ==> Installing glm
  ==> Searching for binary cache of glm
  ==> Installing glm from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/glm-0.9.7.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-glm-0.9.7.1-jnw622jwcbsymzj2fsx22omjl7tmvaws.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:30:38 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed glm from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/glm-0.9.7.1-jnw622jwcbsymzj2fsx22omjl7tmvaws
  ==> libsigsegv is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> m4 is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-r5envx3kqctwwflhd4qax4ahqtt6x43a
  ==> libtool is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libtool-2.4.6-o2pfwjf44353ajgr42xqtvzyvqsazkgu
  ==> util-macros is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/util-macros-1.19.1-milz7fmttmptcic2qdk5cnel7ll5sybr
  ==> libpciaccess is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libpciaccess-0.13.5-5urc6tcjae26fbbd2wyfohoszhgxtbmc
  ==> xz is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/xz-5.2.3-htnq7wqdrqtof6uxqicdj3f7oe3xz6pw
  ==> libxml2 is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libxml2-2.9.4-sxk64lvcxhqjflzesnf3ye4wakovwi45
  ==> hwloc is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hwloc-1.11.8-ivg4d2e6anxwin4zbld2g4qlrbuquoyg
  ==> openmpi is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openmpi-3.0.0-yo5qkfvumpmgmvlbalqcadu46j5bd52f
  ==> Installing hdf5
  ==> Searching for binary cache of hdf5
  ==> Installing hdf5 from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-hdf5-1.10.1-d73xxpvfxgd2z2ypmuuwtxhoxmzdglez.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:39:36 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
  /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed hdf5 from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1-d73xxpvfxgd2z2ypmuuwtxhoxmzdglez
  ==> Installing openblas
  ==> Searching for binary cache of openblas
  ==> Installing openblas from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/openblas-0.2.20/linux-ubuntu16.04-x86_64-gcc-5.4.0-openblas-0.2.20-4dahl6ltbpojei4s3stbqbq5iuuqlaxo.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:43:22 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed openblas from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openblas-0.2.20-4dahl6ltbpojei4s3stbqbq5iuuqlaxo
  ==> Installing hypre
  ==> Searching for binary cache of hypre
  ==> Installing hypre from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hypre-2.12.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-hypre-2.12.1-z3rgfzqc4gu4u4qvveyo2dqqzl2j463z.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:30:17 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed hypre from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hypre-2.12.1-z3rgfzqc4gu4u4qvveyo2dqqzl2j463z
  ==> Installing matio
  ==> Searching for binary cache of matio
  ==> Installing matio from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/matio-1.5.9/linux-ubuntu16.04-x86_64-gcc-5.4.0-matio-1.5.9-4ajrcuhdf5uktotnrfzufufy5vbd6any.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:30:24 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed matio from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/matio-1.5.9-4ajrcuhdf5uktotnrfzufufy5vbd6any
  ==> Installing metis
  ==> Searching for binary cache of metis
  ==> Installing metis from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/metis-5.1.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-metis-5.1.0-m34qytcqsvsaduxyh3wevf3kj6pbzyw6.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:39:28 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
  /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed metis from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/metis-5.1.0-m34qytcqsvsaduxyh3wevf3kj6pbzyw6
  ==> Installing netlib-scalapack
  ==> Searching for binary cache of netlib-scalapack
  ==> Installing netlib-scalapack from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-scalapack-2.0.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-netlib-scalapack-2.0.2-xudg7xypr63nte6ifrdsmllilxbrfiar.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:30:28 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed netlib-scalapack from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-scalapack-2.0.2-xudg7xypr63nte6ifrdsmllilxbrfiar
  ==> Installing mumps
  ==> Searching for binary cache of mumps
  ==> Installing mumps from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/mumps-5.1.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-mumps-5.1.1-5a7hgodxoze47xqd32jcxhvzctex4ezx.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:30:15 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed mumps from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mumps-5.1.1-5a7hgodxoze47xqd32jcxhvzctex4ezx
  ==> Installing netcdf
  ==> Searching for binary cache of netcdf
  ==> Installing netcdf from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/netcdf-4.4.1.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-netcdf-4.4.1.1-gk2xxhbqijnrdwicawawcll4t3c7dvoj.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:43:37 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed netcdf from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netcdf-4.4.1.1-gk2xxhbqijnrdwicawawcll4t3c7dvoj
  ==> Installing parmetis
  ==> Searching for binary cache of parmetis
  ==> Installing parmetis from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/parmetis-4.0.3/linux-ubuntu16.04-x86_64-gcc-5.4.0-parmetis-4.0.3-o4qdo7aylhejov2e5ii7tagrnw6qrrlo.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:39:37 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
  /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed parmetis from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/parmetis-4.0.3-o4qdo7aylhejov2e5ii7tagrnw6qrrlo
  ==> Installing suite-sparse
  ==> Searching for binary cache of suite-sparse
  ==> Installing suite-sparse from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/suite-sparse-4.5.5/linux-ubuntu16.04-x86_64-gcc-5.4.0-suite-sparse-4.5.5-bg67crx4ltmxulnumuxjxqzrcobpmyzg.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:30:31 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed suite-sparse from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/suite-sparse-4.5.5-bg67crx4ltmxulnumuxjxqzrcobpmyzg
  ==> Installing superlu-dist
  ==> Searching for binary cache of superlu-dist
  ==> Installing superlu-dist from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/superlu-dist-5.2.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-superlu-dist-5.2.2-gggsamgizi2dwmwxglgzbxvg6hkamhol.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:43:35 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed superlu-dist from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/superlu-dist-5.2.2-gggsamgizi2dwmwxglgzbxvg6hkamhol
  ==> Installing trilinos
  ==> Searching for binary cache of trilinos
  ==> Installing trilinos from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-trilinos-12.12.1-istwe3b43b7etgtrhcuzjem3p5gonc6h.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 11:47:19 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed trilinos from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1-istwe3b43b7etgtrhcuzjem3p5gonc6h

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
  ==> bzip2 is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/bzip2-1.0.6-ufczdvsqt6edesm36xiucyry7myhj7e7
  ==> zlib is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> boost is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/boost-1.65.1-xxqnbqql5nup7rujer2ury3hsdgcumzb
  ==> pkg-config is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkg-config-0.29.2-ae2hwm7q57byfbxtymts55xppqwk7ecj
  ==> ncurses is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.0-ukq4tccptm2rxd56d2bumqthnpcjzlez
  ==> openssl is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2k-2woov64m3n4gjtnfp722qcyemzf2qtom
  ==> cmake is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/cmake-3.9.4-a2lyofsoxutyy4ihvzopizpbjubtdoem
  ==> glm is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/glm-0.9.7.1-jnw622jwcbsymzj2fsx22omjl7tmvaws
  ==> mpich is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpich-3.2-cymrnoowcc4vdyvdnf5ypvob4cmdadk5
  ==> hdf5 is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1-e4gz6f2l5ik3ijuk3alwsqplex4tbvin
  ==> openblas is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openblas-0.2.20-4dahl6ltbpojei4s3stbqbq5iuuqlaxo
  ==> Installing hypre
  ==> Searching for binary cache of hypre
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-netcdf-4.4.1.1-gk2xxhbqijnrdwicawawcll4t3c7dvoj.spec.yaml
  ######################################################################## 100.0%
  ...
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-bzip2-1.0.6-ufczdvsqt6edesm36xiucyry7myhj7e7.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-boost-1.65.1-xxqnbqql5nup7rujer2ury3hsdgcumzb.spec.yaml
  ######################################################################## 100.0%
  ==> Installing hypre from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/hypre-2.12.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-hypre-2.12.1-3psjg2ka2qa26jtgitlil4vglqr67anj.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:49:37 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed hypre from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hypre-2.12.1-3psjg2ka2qa26jtgitlil4vglqr67anj
  ==> Installing matio
  ==> Searching for binary cache of matio
  ==> Installing matio from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/matio-1.5.9/linux-ubuntu16.04-x86_64-gcc-5.4.0-matio-1.5.9-3ibrutc6cs7x6ybyt5ni5n6djtq5okm2.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:45:26 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed matio from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/matio-1.5.9-3ibrutc6cs7x6ybyt5ni5n6djtq5okm2
  ==> metis is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/metis-5.1.0-m34qytcqsvsaduxyh3wevf3kj6pbzyw6
  ==> Installing netlib-scalapack
  ==> Searching for binary cache of netlib-scalapack
  ==> Installing netlib-scalapack from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-scalapack-2.0.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-netlib-scalapack-2.0.2-km7tsbgoyyywonyejkjoojskhc5knz3z.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:49:49 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed netlib-scalapack from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netlib-scalapack-2.0.2-km7tsbgoyyywonyejkjoojskhc5knz3z
  ==> Installing mumps
  ==> Searching for binary cache of mumps
  ==> Installing mumps from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/mumps-5.1.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-mumps-5.1.1-phvk6yhkzqed6gjsbah6dnhlesdclild.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:45:28 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed mumps from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mumps-5.1.1-phvk6yhkzqed6gjsbah6dnhlesdclild
  ==> libsigsegv is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> m4 is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-r5envx3kqctwwflhd4qax4ahqtt6x43a
  ==> Installing netcdf
  ==> Searching for binary cache of netcdf
  ==> Installing netcdf from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/netcdf-4.4.1.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-netcdf-4.4.1.1-rmx4uppnhpv6kq7bh7r46zfqevgdkkgw.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:49:38 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed netcdf from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/netcdf-4.4.1.1-rmx4uppnhpv6kq7bh7r46zfqevgdkkgw
  ==> Installing parmetis
  ==> Searching for binary cache of parmetis
  ==> Installing parmetis from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/parmetis-4.0.3/linux-ubuntu16.04-x86_64-gcc-5.4.0-parmetis-4.0.3-qk77g6aiqr3f2hsykg54zzuhlxcpdcmv.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:45:14 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed parmetis from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/parmetis-4.0.3-qk77g6aiqr3f2hsykg54zzuhlxcpdcmv
  ==> suite-sparse is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/suite-sparse-4.5.5-bg67crx4ltmxulnumuxjxqzrcobpmyzg
  ==> Installing superlu-dist
  ==> Searching for binary cache of superlu-dist
  ==> Installing superlu-dist from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/superlu-dist-5.2.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-superlu-dist-5.2.2-65vot2le3ezooz7tj6eveovly725o44x.spack
  ######################################################################## 100.0%
  gpg: Signature made Sat 11 Nov 2017 12:45:14 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed superlu-dist from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/superlu-dist-5.2.2-65vot2le3ezooz7tj6eveovly725o44x
  ==> Installing trilinos
  ==> Searching for binary cache of trilinos
  ==> Installing trilinos from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-trilinos-12.12.1-xupifcp5d4f53cobm6g3xzao577uzezs.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 12:04:58 AM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed trilinos from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1-xupifcp5d4f53cobm6g3xzao577uzezs


We see that every package in the trilinos DAG that depends on MPI now
uses ``mpich``.

.. code-block:: console

  $ spack find -d trilinos
  ==> 2 installed packages.
  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
      trilinos@12.12.1
          ^boost@1.65.1
              ^bzip2@1.0.6
              ^zlib@1.2.11
          ^glm@0.9.7.1
          ^hdf5@1.10.1
              ^openmpi@3.0.0
                  ^hwloc@1.11.8
                      ^libpciaccess@0.13.5
                      ^libxml2@2.9.4
                          ^xz@5.2.3
          ^hypre@2.12.1
              ^openblas@0.2.20
          ^matio@1.5.9
          ^metis@5.1.0
          ^mumps@5.1.1
              ^netlib-scalapack@2.0.2
          ^netcdf@4.4.1.1
          ^parmetis@4.0.3
          ^suite-sparse@4.5.5
          ^superlu-dist@5.2.2

      trilinos@12.12.1
          ^boost@1.65.1
              ^bzip2@1.0.6
              ^zlib@1.2.11
          ^glm@0.9.7.1
          ^hdf5@1.10.1
              ^mpich@3.2
          ^hypre@2.12.1
              ^openblas@0.2.20
          ^matio@1.5.9
          ^metis@5.1.0
          ^mumps@5.1.1
              ^netlib-scalapack@2.0.2
          ^netcdf@4.4.1.1
          ^parmetis@4.0.3
          ^suite-sparse@4.5.5
          ^superlu-dist@5.2.2

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
  | | | | | | | | | | | | | |\
  o | | | | | | | | | | | | | |  superlu-dist
  |\ \ \ \ \ \ \ \ \ \ \ \ \ \ \
  | |_|/ / / / / / / / / / / / /
  |/| | | | | | | | | | | | | |
  | |\ \ \ \ \ \ \ \ \ \ \ \ \ \
  | | |_|/ / / / / / / / / / / /
  | |/| | | | | | | | | | | | |
  | | |\ \ \ \ \ \ \ \ \ \ \ \ \
  | | | |_|/ / / / / / / / / / /
  | | |/| | | | | | | | | | | |
  | | | | |_|_|/ / / / / / / /
  | | | |/| | | | | | | | | |
  | | | | o | | | | | | | | |  suite-sparse
  | | | |/| | | | | | | | | |
  | | |/|/ / / / / / / / / /
  o | | | | | | | | | | | |  parmetis
  |\| | | | | | | | | | | |
  |\ \ \ \ \ \ \ \ \ \ \ \ \
  | |_|_|/ / / / / / / / / /
  |/| | | | | | | | | | | |
  | | |_|_|_|_|_|_|_|/ / /
  | |/| | | | | | | | | |
  | | | | | | o | | | | |  mumps
  | | | |_|_|/| | | | | |
  | | |/| |_|/| | | | | |
  | | | |/| |/ / / / / /
  | | | | |/| | | | | |
  | | | | o | | | | | |  netlib-scalapack
  | | |_|/| | | | | | |
  | |/| |/| | | | | | |
  | | |/|/ / / / / / /
  o | | | | | | | | |  metis
  |/ / / / / / / / /
  | | | | | | | o |  glm
  | |_|_|_|_|_|/ /
  |/| | | | | | |
  o | | | | | | |  cmake
  |\ \ \ \ \ \ \ \
  o | | | | | | | |  openssl
  | | | | o | | | |  netcdf
  | |_|_|/| | | | |
  |/| | |/| | | | |
  | | |/| | | | | |
  | | | | |\ \ \ \ \
  | | | | | | |_|/ /
  | | | | | |/| | |
  | | | | | | o | |  matio
  | |_|_|_|_|/| | |
  |/| | | | |/ / /
  | | | | | | o |  hypre
  | | | |_|_|/| |
  | | |/| |_|/ /
  | | | |/| | |
  | | | | | o |  hdf5
  | |_|_|_|/| |
  |/| | |_|/ /
  | | |/| | |
  | | o | | |  openmpi
  | | o | | |  hwloc
  | | |\ \ \ \
  | | | |\ \ \ \
  | | | o | | | |  libxml2
  | |_|/| | | | |
  |/| |/| | | | |
  | | | | | | | o  boost
  | |_|_|_|_|_|/|
  |/| | | | | | |
  o | | | | | | |  zlib
   / / / / / / /
   | | o | | | |  xz
   | |  / / / /
   | | o | | |  libpciaccess
   | |/| | | |
   | | |\ \ \ \
   | | o | | | |  util-macros
   | |  / / / /
   o | | | | |  ncurses
   |/ / / / /
   o | | | |  pkg-config
    / / / /
    | o | |  openblas
    |  / /
    o | |  libtool
    |/ /
    o |  m4
    o |  libsigsegv
     /
     o  bzip2

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
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
      openssl@1.0.2k
          ^zlib@1.2.8

  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
      openssl@1.0.2k
          ^zlib@1.2.8

      openssl@1.0.2k
          ^zlib@1.2.11

  $ spack find zlib
  ==> 6 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  zlib@1.2.8  zlib@1.2.11

  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  zlib@1.2.11

  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  zlib@1.2.8  zlib@1.2.8  zlib@1.2.11

We can uninstall packages by spec using the same syntax as install.

.. code-block:: console

  $ spack uninstall zlib %gcc@4.7
  ==> The following packages will be uninstalled:

  -- linux-ubuntu16.04-x86_64 / gcc@4.7 ---------------------------
  bq2wtdx zlib@1.2.11%gcc+optimize+pic+shared

  ==> Do you want to proceed? [y/N] y
  ==> Successfully uninstalled zlib@1.2.11%gcc@4.7+optimize+pic+shared arch=linux-ubuntu16.04-x86_64 /bq2wtdx

  $ spack find -lf zlib
  ==> 5 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  i426yu3 zlib@1.2.8%clang

  4pt75q7 zlib@1.2.11%clang


  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  bkyl5bh zlib@1.2.8%gcc

  64mns5m zlib@1.2.8%gcc cppflags="-O3"

  5nus6kn zlib@1.2.11%gcc

We can also uninstall packages by referring only to their hash.

We can use either ``-f`` (force) or ``-R`` (remove dependents as well) to
remove packages that are required by another installed package.

.. code-block:: console

  $ spack uninstall zlib/i426
  ==> Error: Will not uninstall zlib@1.2.8%clang@3.8.0-2ubuntu4/i426yu3

  The following packages depend on it:
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  ufruk7k openssl@1.0.2k%clang


  ==> Error: Use \`spack uninstall --dependents\` to uninstall these dependencies as well.

  $ spack uninstall -R zlib/i426
  ==> The following packages will be uninstalled:

  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
  ufruk7k openssl@1.0.2k%clang

  i426yu3 zlib@1.2.8%clang+optimize+pic+shared

  ==> Do you want to proceed? [y/N] y
  ==> Successfully uninstalled openssl@1.0.2k%clang@3.8.0-2ubuntu4 arch=linux-ubuntu16.04-x86_64 /ufruk7k
  ==> Successfully uninstalled zlib@1.2.8%clang@3.8.0-2ubuntu4+optimize+pic+shared arch=linux-ubuntu16.04-x86_64 /i426yu3

Spack will not uninstall packages that are not sufficiently
specified. The ``-a`` (all) flag can be used to uninstall multiple
packages at once.

.. code-block:: console

  $ spack uninstall trilinos
  ==> Error: trilinos matches multiple packages:

  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  istwe3b trilinos@12.12.1%gcc~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~dtk+epetra+epetraext+exodus+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2+instantiate~instantiate_cmplx~intrepid~intrepid2+metis+ml+muelu+mumps~nox~openmp~pnetcdf~python~rol+sacado~shards+shared~stk+suite-sparse~superlu+superlu-dist+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2

  xupifcp trilinos@12.12.1%gcc~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~dtk+epetra+epetraext+exodus+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2+instantiate~instantiate_cmplx~intrepid~intrepid2+metis+ml+muelu+mumps~nox~openmp~pnetcdf~python~rol+sacado~shards+shared~stk+suite-sparse~superlu+superlu-dist+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2


  ==> Error: You can either:
      a) use a more specific spec, or
      b) use `spack uninstall --all` to uninstall ALL matching specs.


  $ spack uninstall /istw
  ==> The following packages will be uninstalled:

  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  istwe3b trilinos@12.12.1%gcc~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~dtk+epetra+epetraext+exodus+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2+instantiate~instantiate_cmplx~intrepid~intrepid2+metis+ml+muelu+mumps~nox~openmp~pnetcdf~python~rol+sacado~shards+shared~stk+suite-sparse~superlu+superlu-dist+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2

  ==> Do you want to proceed? [y/N] y
  ==> Successfully uninstalled trilinos@12.12.1%gcc@5.4.0~alloptpkgs+amesos+amesos2+anasazi+aztec+belos+boost build_type=RelWithDebInfo ~dtk+epetra+epetraext+exodus+fortran~fortrilinos+gtest+hdf5+hypre+ifpack+ifpack2+instantiate~instantiate_cmplx~intrepid~intrepid2+metis+ml+muelu+mumps~nox~openmp~pnetcdf~python~rol+sacado~shards+shared~stk+suite-sparse~superlu+superlu-dist+teuchos+tpetra~x11~xsdkflags~zlib+zoltan+zoltan2 arch=linux-ubuntu16.04-x86_64 /istwe3b

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
  ==> 9 installed packages.
  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  hdf5@1.10.1  hypre@2.12.1  matio@1.5.9  mumps@5.1.1  netcdf@4.4.1.1  netlib-scalapack@2.0.2  parmetis@4.0.3  superlu-dist@5.2.2  trilinos@12.12.1


  $ spack find cppflags=-O3
  ==> 1 installed packages.
  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
  zlib@1.2.8

The ``find`` command can also show which packages were installed
explicitly (rather than pulled in as a dependency) using the ``-e``
flag. The ``-E`` flag shows implicit installs only. The ``find`` command can
also show the path to which a spack package was installed using the ``-p``
command.

.. code-block:: console

  $ spack find -pe
  ==> 10 installed packages.
  -- linux-ubuntu16.04-x86_64 / clang@3.8.0-2ubuntu4 --------------
      zlib@1.2.11  /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/clang-3.8.0-2ubuntu4/zlib-1.2.11-4pt75q7qq6lygf3hgnona4lyc2uwedul

  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
      hdf5@1.10.1       /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1-pa6oqzfeqzkqkzqr2375fqyt3qggx3tr
      hdf5@1.10.1       /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1-bovz45ms24pmfr7hlckf56bxegfc4rea
      hdf5@1.10.1       /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/hdf5-1.10.1-e4gz6f2l5ik3ijuk3alwsqplex4tbvin
      openssl@1.0.2k    /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2k-gyxmhgbam26d7y42omb7xrvkjjgmzwio
      openssl@1.0.2k    /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/openssl-1.0.2k-2woov64m3n4gjtnfp722qcyemzf2qtom
      trilinos@12.12.1  /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/trilinos-12.12.1-xupifcp5d4f53cobm6g3xzao577uzezs
      zlib@1.2.8        /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8-bkyl5bhuep6fmhuxzkmhqy25qefjcvzc
      zlib@1.2.8        /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.8-64mns5mvdacqvlashkf7v6lqrxixhmxu
      zlib@1.2.11       /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb

---------------------
Customizing Compilers
---------------------


Spack manages a list of available compilers on the system, detected
automatically from from the user's ``PATH`` variable. The ``spack
compilers`` command is an alias for the command ``spack compiler list``.

.. code-block:: console

  $ spack compilers
  ==> Available compilers
  -- clang ubuntu16.04-x86_64 -------------------------------------
  clang@3.8.0-2ubuntu4  clang@3.7.1-2ubuntu2

  -- gcc ubuntu16.04-x86_64 ---------------------------------------
  gcc@5.4.0  gcc@4.7

The compilers are maintained in a YAML file. Later in the tutorial you
will learn how to configure compilers by hand for special cases. Spack
also has tools to add compilers, and compilers built with Spack can be
added to the configuration.

.. code-block:: console

  $ spack install --use-cache gcc
  ==> libsigsegv is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libsigsegv-2.11-fypapcprssrj3nstp6njprskeyynsgaz
  ==> m4 is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/m4-1.4.18-r5envx3kqctwwflhd4qax4ahqtt6x43a
  ==> pkg-config is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/pkg-config-0.29.2-ae2hwm7q57byfbxtymts55xppqwk7ecj
  ==> ncurses is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/ncurses-6.0-ukq4tccptm2rxd56d2bumqthnpcjzlez
  ==> Installing readline
  ==> Searching for binary cache of readline
  ==> Finding buildcaches in /home/ubuntu/becker/buildcache/build_cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-matio-1.5.9-3ibrutc6cs7x6ybyt5ni5n6djtq5okm2.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-trilinos-12.12.1-xupifcp5d4f53cobm6g3xzao577uzezs.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-parmetis-4.0.3-qk77g6aiqr3f2hsykg54zzuhlxcpdcmv.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-superlu-dist-5.2.2-65vot2le3ezooz7tj6eveovly725o44x.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-hypre-2.12.1-3psjg2ka2qa26jtgitlil4vglqr67anj.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-mumps-5.1.1-phvk6yhkzqed6gjsbah6dnhlesdclild.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-netcdf-4.4.1.1-rmx4uppnhpv6kq7bh7r46zfqevgdkkgw.spec.yaml
  ######################################################################## 100.0%
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64-gcc-5.4.0-netlib-scalapack-2.0.2-km7tsbgoyyywonyejkjoojskhc5knz3z.spec.yaml
  ######################################################################## 100.0%
  ==> Installing readline from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/readline-7.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-readline-7.0-gizxpch53zv5ufa62a2tb5lalcqgxbuc.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 10:26:53 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed readline from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/readline-7.0-gizxpch53zv5ufa62a2tb5lalcqgxbuc
  ==> Installing gdbm
  ==> Searching for binary cache of gdbm
  ==> Installing gdbm from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/gdbm-1.13/linux-ubuntu16.04-x86_64-gcc-5.4.0-gdbm-1.13-vdhoris6wdzzb2ykax2hz7qzgizk5h3t.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 10:26:51 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed gdbm from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gdbm-1.13-vdhoris6wdzzb2ykax2hz7qzgizk5h3t
  ==> Installing perl
  ==> Searching for binary cache of perl
  ==> Installing perl from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/perl-5.24.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-perl-5.24.1-mfzwy6y5mlbqpqvti4etpe3cgkmxkpi2.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 10:27:19 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed perl from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/perl-5.24.1-mfzwy6y5mlbqpqvti4etpe3cgkmxkpi2
  ==> Installing autoconf
  ==> Searching for binary cache of autoconf
  ==> Installing autoconf from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/autoconf-2.69/linux-ubuntu16.04-x86_64-gcc-5.4.0-autoconf-2.69-bvabhjiklhi7c5742ixzs7hubhid3ax2.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 10:27:22 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed autoconf from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/autoconf-2.69-bvabhjiklhi7c5742ixzs7hubhid3ax2
  ==> Installing automake
  ==> Searching for binary cache of automake
  ==> Installing automake from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/automake-1.15.1/linux-ubuntu16.04-x86_64-gcc-5.4.0-automake-1.15.1-kaiefe4j2lsq6b32ncrclmbeoa5z25a5.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 10:27:21 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed automake from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/automake-1.15.1-kaiefe4j2lsq6b32ncrclmbeoa5z25a5
  ==> libtool is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/libtool-2.4.6-o2pfwjf44353ajgr42xqtvzyvqsazkgu
  ==> Installing gmp
  ==> Searching for binary cache of gmp
  ==> Installing gmp from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/gmp-6.1.2/linux-ubuntu16.04-x86_64-gcc-5.4.0-gmp-6.1.2-qc4qcfz4monpllc3nqupdo7vwinf73sw.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 10:12:29 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed gmp from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gmp-6.1.2-qc4qcfz4monpllc3nqupdo7vwinf73sw
  ==> Installing isl
  ==> Searching for binary cache of isl
  ==> Installing isl from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/isl-0.18/linux-ubuntu16.04-x86_64-gcc-5.4.0-isl-0.18-vttqoutnsmjpm3ogb52rninksc7hq5ax.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 10:12:28 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed isl from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/isl-0.18-vttqoutnsmjpm3ogb52rninksc7hq5ax
  ==> Installing mpfr
  ==> Searching for binary cache of mpfr
  ==> Installing mpfr from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpfr-3.1.5/linux-ubuntu16.04-x86_64-gcc-5.4.0-mpfr-3.1.5-mdi6irzvxcbemt7yredzr36dvo6ty4sl.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 10:12:30 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed mpfr from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpfr-3.1.5-mdi6irzvxcbemt7yredzr36dvo6ty4sl
  ==> Installing mpc
  ==> Searching for binary cache of mpc
  ==> Installing mpc from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpc-1.0.3/linux-ubuntu16.04-x86_64-gcc-5.4.0-mpc-1.0.3-tumbpshu5hjxwextoudk5hmic6nspb3z.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 10:12:29 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed mpc from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/mpc-1.0.3-tumbpshu5hjxwextoudk5hmic6nspb3z
  ==> zlib is already installed in /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/zlib-1.2.11-5nus6knzumx4ik2yl44jxtgtsl7d54xb
  ==> Installing gcc
  ==> Searching for binary cache of gcc
  ==> Installing gcc from binary cache
  ==> Fetching file:///home/ubuntu/becker/buildcache/build_cache/linux-ubuntu16.04-x86_64/gcc-5.4.0/gcc-7.2.0/linux-ubuntu16.04-x86_64-gcc-5.4.0-gcc-7.2.0-k3vy57euyeuyvpotwf4wezfmpo3mrtrj.spack
  ######################################################################## 100.0%
  gpg: Signature made Sun 12 Nov 2017 10:16:31 PM UTC using RSA key ID 3B7C69B2
  gpg: Good signature from "sc-tutorial (GPG created for Spack) <becker33@llnl.gov>" [unknown]
  gpg: WARNING: This key is not certified with a trusted signature!
  gpg:          There is no indication that the signature belongs to the owner.
  Primary key fingerprint: 95C7 1787 7AC0 0FFD AA8F  D6E9 9CFA 4A45 3B7C 69B2
  ==> Relocating package from
    /home/ubuntu/becker/spack/opt/spack to /home/ubuntu/test/spack/opt/spack.
  ==> Successfully installed gcc from binary cache
  [+] /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gcc-7.2.0-k3vy57euyeuyvpotwf4wezfmpo3mrtrj

  $ spack find -p gcc
  ==> 1 installed packages.
  -- linux-ubuntu16.04-x86_64 / gcc@5.4.0 -------------------------
      gcc@7.2.0  /home/ubuntu/test/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gcc-7.2.0-k3vy57euyeuyvpotwf4wezfmpo3mrtrj

We can add gcc to Spack as an available compiler using the ``spack
compiler add`` command. This will allow future packages to build with
gcc@7.2.0.

.. code-block:: console

  $ spack compiler add /home/ubuntu/becker/spack/opt/spack/linux-ubuntu16.04-x86_64/gcc-5.4.0/gcc-7.2.0-k3vy57euyeuyvpotwf4wezfmpo3mrtrj
  ==> Added 1 new compiler to /home/ubuntu/.spack/linux/compilers.yaml
      gcc@7.2.0
  ==> Compilers are defined in the following files:
      /home/ubuntu/.spack/linux/compilers.yaml

We can also remove compilers from our configuration using ``spack compiler remove <compiler_spec>``

.. code-block:: console

  $ spack compiler remove gcc@7.2.0
  ==> Removed compiler gcc@7.2.0
