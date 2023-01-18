.. Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _binary_caches:

============
Build Caches
============

Some sites may encourage users to set up their own test environments
before carrying out central installations, or some users may prefer to set
up these environments on their own motivation. To reduce the load of
recompiling otherwise identical package specs in different installations,
installed packages can be put into build cache tarballs, pushed to
your Spack mirror and then downloaded and installed by others.

Whenever a mirror provides prebuilt packages, Spack will take these packages
into account during concretization and installation, making ``spack install``
signficantly faster.


.. note::

    We use the terms "build cache" and "mirror" often interchangeably. Mirrors
    are used during installation both for sources and prebuilt packages. Build
    caches refer to mirrors that provide prebuilt packages.


----------------------
Creating a build cache
----------------------

Build caches are created via:

.. code-block:: console

    $ spack buildcache create <path/url/mirror name> <spec>

This command takes the locally installed spec and its dependencies, and
creates tarballs of their install prefixes. It also generates metadata files,
signed with GPG. These tarballs and metadata files are then pushed to the
provided binary cache, which can be a local directory or a remote URL.

Here is an example where a build cache is created in a local directory named
"spack-cache", to which we push the "ninja" spec:

.. code-block:: console

    $ spack buildcache create --allow-root ./spack-cache ninja
    ==> Pushing binary packages to file:///home/spackuser/spack/spack-cache/build_cache

Not that ``ninja`` must be installed locally for this to work.

We're using the ``--allow-root`` flag to tell Spack that is OK when any of
the binaries we're pushing contain references to the local Spack install
directory.

Once you have a build cache, you can add it as a mirror, discussed next.

---------------------------------------
Finding or installing build cache files
---------------------------------------

To find build caches or install build caches, a Spack mirror must be configured
with:

.. code-block:: console

    $ spack mirror add <name> <url or path>


Both web URLs and local paths on the filesystem can be specified. In the previous
example, you might add the directory "spack-cache" and call it ``mymirror``:


.. code-block:: console

    $ spack mirror add mymirror ./spack-cache


You can see that the mirror is added with ``spack mirror list`` as follows:

.. code-block:: console


    $ spack mirror list
    mymirror           file:///home/spackuser/spack/spack-cache
    spack-public       https://spack-llnl-mirror.s3-us-west-2.amazonaws.com/


At this point, you've create a buildcache, but spack hasn't indexed it, so if
you run ``spack buildcache list`` you won't see any results. You need to index
this new build cache as follows:

.. code-block:: console

    $ spack buildcache update-index ./spack-cache

Now you can use list:

.. code-block:: console

    $  spack buildcache list
    ==> 1 cached build.
    -- linux-ubuntu20.04-skylake / gcc@9.3.0 ------------------------
    ninja@1.10.2

With ``mymirror`` configured and an index available, Spack will automatically
use it during concretization and installation. That means that you can expect
``spack install ninja`` to fetch prebuilt packages from the mirror. Let's
verify by re-installing ninja:

.. code-block:: console

    $ spack uninstall ninja
    $ spack install ninja
    ==> Installing ninja-1.11.1-yxferyhmrjkosgta5ei6b4lqf6bxbscz
    ==> Fetching file:///home/spackuser/spack/spack-cache/build_cache/linux-ubuntu20.04-skylake-gcc-9.3.0-ninja-1.10.2-yxferyhmrjkosgta5ei6b4lqf6bxbscz.spec.json.sig
    gpg: Signature made Do 12 Jan 2023 16:01:04 CET
    gpg:                using RSA key 61B82B2B2350E171BD17A1744E3A689061D57BF6
    gpg: Good signature from "example (GPG created for Spack) <example@example.com>" [ultimate]
    ==> Fetching file:///home/spackuser/spack/spack-cache/build_cache/linux-ubuntu20.04-skylake/gcc-9.3.0/ninja-1.10.2/linux-ubuntu20.04-skylake-gcc-9.3.0-ninja-1.10.2-yxferyhmrjkosgta5ei6b4lqf6bxbscz.spack
    ==> Extracting ninja-1.10.2-yxferyhmrjkosgta5ei6b4lqf6bxbscz from binary cache
    ==> ninja: Successfully installed ninja-1.11.1-yxferyhmrjkosgta5ei6b4lqf6bxbscz
    Search: 0.00s.  Fetch: 0.17s.  Install: 0.12s.  Total: 0.29s
    [+] /home/harmen/spack/opt/spack/linux-ubuntu20.04-skylake/gcc-9.3.0/ninja-1.11.1-yxferyhmrjkosgta5ei6b4lqf6bxbscz


It worked! You've just completed a full example of creating a build cache with
a spec of interest, adding it as a mirror, updating its index, listing the contents,
and finally, installing from it.

By default Spack falls back to building from sources when the mirror is not available
or when the package is simply not already available. To force Spack to only install
prebuilt packages, you can use

.. code-block:: console

   $ spack install --use-buildcache only <package>

For example, to combine all of the commands above to add the E4S build cache
and then install from it exclusively, you would do:

.. code-block:: console

    $ spack mirror add E4S https://cache.e4s.io
    $ spack buildcache keys --install --trust
    $ spack install --use-buildache only <package>

We use ``--install`` and ``--trust`` to say that we are installing keys to our
keyring, and trusting all downloaded keys.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^
List of popular build caches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `Extreme-scale Scientific Software Stack (E4S) <https://e4s-project.github.io/>`_: `build cache <https://oaciss.uoregon.edu/e4s/inventory.html>`_


----------
Relocation
----------

Initial build and later installation do not necessarily happen at the same
location. Spack provides a relocation capability and corrects for RPATHs and
non-relocatable scripts. However, many packages compile paths into binary
artifacts directly. In such cases, the build instructions of this package would
need to be adjusted for better re-locatability.

.. _cmd-spack-buildcache:

--------------------
``spack buildcache``
--------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache create``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create tarball of installed Spack package and all dependencies.
Tarballs are checksummed and signed if gpg2 is available.
Places them in a directory ``build_cache`` that can be copied to a mirror.
Commands like ``spack buildcache install`` will search Spack mirrors for build_cache to get the list of build caches.

==============  ========================================================================================================================
Arguments       Description
==============  ========================================================================================================================
``<specs>``     list of partial specs or hashes with a leading ``/`` to match from installed packages and used for creating build caches
``-d <path>``   directory in which ``build_cache`` directory is created, defaults to ``.``
``-f``          overwrite ``.spack`` file in ``build_cache`` directory if it exists
``-k <key>``    the key to sign package with. In the case where multiple keys exist, the package will be unsigned unless ``-k`` is used.
``-r``          make paths in binaries relative before creating tarball
``-y``          answer yes to all create unsigned ``build_cache`` questions
==============  ========================================================================================================================

^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache list``
^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieves all specs for build caches available on a Spack mirror.

==============  =====================================================================================
Arguments       Description
==============  =====================================================================================
``<specs>``     list of partial package specs to be matched against specs downloaded for build caches
==============  =====================================================================================

E.g. ``spack buildcache list gcc`` with print only commands to install ``gcc`` package(s)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache install``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieves all specs for build caches available on a Spack mirror and installs build caches
with specs matching the specs input.

==============  ==============================================================================================
Arguments       Description
==============  ==============================================================================================
``<specs>``     list of partial package specs or hashes with a leading ``/`` to be installed from build caches
``-f``          remove install directory if it exists before unpacking tarball
``-y``          answer yes to all to don't verify package with gpg questions
==============  ==============================================================================================

^^^^^^^^^^^^^^^^^^^^^^^^^
``spack buildcache keys``
^^^^^^^^^^^^^^^^^^^^^^^^^

List public keys available on Spack mirror.

=========  ==============================================
Arguments  Description
=========  ==============================================
``-i``     trust the keys downloaded with prompt for each
``-y``     answer yes to all trust all keys downloaded
=========  ==============================================
