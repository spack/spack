..
   Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Discover how to set up and manage mirrors in Spack to provide a local repository of tarballs for offline package fetching.

.. index::
   single: mirror; configuring
   single: mirrors.yaml; reference
   :name: mirrors

Mirrors (mirrors.yaml)
======================

Some sites may not have access to the internet for fetching packages.
These sites will need a local repository of tarballs from which they can get their files.
Spack has support for this with *mirrors*.
A mirror is a URL that points to a directory, either on the local filesystem or on some server, containing tarballs for all of Spack's packages.

Here's an example of a mirror's directory structure:

.. code-block:: none

   mirror/
       _source-cache/
           archive/
               2e/
                   2e197bcb6fd44dbf82652e04968b307c73545e01d5c5df04a1f28eef1a081fe4.tar.gz
               63/
                   63074c85be23615383579176d891e9464244d4dcb44ca9a4bdadd7bd9d84a0d8.tar.gz
               a6/
                   a667318a44e3f749721cc630f2cb5541b0f542e934c188280b7075fd6f8e2ee1.tar.gz
           git/
               my-git-hosting.example.com/
                   my-project.git/
                       8d24b17801d9d78a45892e42a7169eb6f1d4c26d.tar.gz

Mirror entries are stored *content-addressed*: archives live under ``_source-cache/archive/`` in directories named after the first two characters of their checksum, and each archive is named after its full checksum.
Archives of version control checkouts (e.g. git repositories at a specific commit) are stored under a directory named after the fetch method, repository URL, and revision.

.. note::

   Archives are **not** named the way they were in the package's fetch URL.
   They have the form ``<checksum>.<extension>``, where ``<checksum>`` is the digest specified in the package recipe for that version (e.g. its ``sha256``), and ``<extension>`` is whatever format the package's fetch URL contains.

   In order to make mirror creation reasonably fast, we copy the tarball in its original format to the mirror directory, but we do not standardize on a particular compression algorithm, because this would potentially require expanding and recompressing each archive.

.. _cmd-spack-mirror:

``spack mirror``
----------------

Mirrors are managed with the ``spack mirror`` command.
The help for ``spack mirror`` looks like this:

.. command-output:: spack help mirror

The ``create`` command actually builds a mirror by fetching all of its packages from the internet and checksumming them.

The other three commands are for managing mirror configuration.
They control the URL(s) from which Spack downloads its packages.

.. _cmd-spack-mirror-create:

``spack mirror create``
-----------------------

You can create a mirror using the ``spack mirror create`` command, assuming you're on a machine where you can access the internet.

The command will iterate through all of Spack's packages and download the safe ones into a directory structure like the one above.
Here is what it looks like:

.. code-block:: console

   $ spack mirror create libelf libdwarf
   ==> Created new mirror in spack-mirror-2014-06-24
   ==> Trying to fetch from http://www.mr511.de/software/libelf-0.8.13.tar.gz
   ##########################################################                81.6%
   ==> Checksum passed for libelf@0.8.13
   ==> Added libelf@0.8.13
   ==> Trying to fetch from http://www.mr511.de/software/libelf-0.8.12.tar.gz
   ######################################################################    98.6%
   ==> Checksum passed for libelf@0.8.12
   ==> Added libelf@0.8.12
   ==> Trying to fetch from http://www.prevanders.net/libdwarf-20130207.tar.gz
   ######################################################################    97.3%
   ==> Checksum passed for libdwarf@20130207
   ==> Added libdwarf@20130207
   ==> Trying to fetch from http://www.prevanders.net/libdwarf-20130126.tar.gz
   ########################################################                  78.9%
   ==> Checksum passed for libdwarf@20130126
   ==> Added libdwarf@20130126
   ==> Trying to fetch from http://www.prevanders.net/libdwarf-20130729.tar.gz
   #############################################################             84.7%
   ==> Added libdwarf@20130729
   ==> Added spack-mirror-2014-06-24/_source-cache/archive/4c/4cc5e2f7b7bd6abf71d7c9c8eee6656b13c81ff8f507b3f1732fd8a00752b971.tar.gz to mirror
   ==> Added python@2.7.8.
   ==> Successfully updated mirror in spack-mirror-2015-02-24.
     Archive stats:
       0    already present
       5    added
       0    failed to fetch.

Once this is done, you can tar up the ``spack-mirror-2014-06-24`` directory and copy it over to the machine you want it hosted on.

Custom package sets
^^^^^^^^^^^^^^^^^^^

Normally, ``spack mirror create`` downloads all the archives it has checksums for.
If you want to only create a mirror for a subset of packages, you can do that by supplying a list of package specs on the command line after ``spack mirror create``.
For example, this command:

.. code-block:: console

   $ spack mirror create libelf@0.8.12: boost@1.44:

Will create a mirror for libelf versions greater than or equal to 0.8.12 and boost versions greater than or equal to 1.44.

Mirror files
^^^^^^^^^^^^

If you have a *very* large number of packages you want to mirror, you can supply a file with specs in it, one per line:

.. code-block:: console

   $ cat specs.txt
   libdwarf
   libelf@0.8.12:
   boost@1.44:
   boost@1.39.0
   ...
   $ spack mirror create --file specs.txt
   ...

This is useful if there is a specific suite of software managed by your site.

Mirror environment
^^^^^^^^^^^^^^^^^^

To create a mirror of all packages required by a concrete environment, activate the environment and run ``spack mirror create -a``.
This is especially useful to create a mirror of an environment that was concretized on another machine.

Optionally specify ``-j <n_workers>`` to control the number of workers used to create a full mirror.
If not specified, the optimal number of workers is determined dynamically.
For a full mirror, the number of workers used is the minimum of 16 workers, available CPU cores, and number of packages to mirror.
For individual packages, 1 worker is used.

.. code-block:: console

   [remote] $ spack env create myenv
   [remote] $ spack env activate myenv
   [remote] $ spack add ...
   [remote] $ spack concretize
   
   $ sftp remote:/spack/var/environment/myenv/spack.lock
   $ spack env create myenv spack.lock
   $ spack env activate myenv
   $ spack mirror create -a
  


.. _cmd-spack-mirror-add:

``spack mirror add``
--------------------

Once you have a mirror, you need to let Spack know about it.
This is relatively simple.
First, figure out the URL for the mirror.
If it's a directory, you can use a file URL like this one:

.. code-block:: none

   file://$HOME/spack-mirror-2014-06-24

That points to the directory on the local filesystem.
If it were on a web server, you could use a URL like this one:

https://example.com/some/web-hosted/directory/spack-mirror-2014-06-24

Spack will use the URL as the root for all of the packages it fetches.
You can tell your Spack installation to use that mirror like this:

.. code-block:: console

   $ spack mirror add local_filesystem file://$HOME/spack-mirror-2014-06-24

Each mirror has a name so that you can refer to it again later.

.. _cmd-spack-mirror-list:

``spack mirror list``
---------------------

To see all the mirrors Spack knows about, run ``spack mirror list``:

.. code-block:: console

   $ spack mirror list
   local_filesystem    file:///home/username/spack-mirror-2014-06-24

.. _cmd-spack-mirror-remove:

``spack mirror remove``
-----------------------

To remove a mirror by name, run:

.. code-block:: console

   $ spack mirror remove local_filesystem
   $ spack mirror list
   ==> No mirrors configured.

Mirror precedence
-----------------

Adding a mirror really adds a line in ``~/.spack/mirrors.yaml``:

.. code-block:: yaml

   mirrors:
     local_filesystem: file:///home/username/spack-mirror-2014-06-24
     remote_server: https://example.com/some/web-hosted/directory/spack-mirror-2014-06-24

If you want to change the order in which mirrors are searched for packages, you can edit this file and reorder the sections.
Spack will search the topmost mirror first and the bottom-most mirror last.

.. _caching:

Local Default Cache
-------------------

Spack caches resources that are downloaded as part of installations.
The cache is a valid Spack mirror: it uses the same directory structure and naming scheme as other Spack mirrors (so it can be copied anywhere and referenced with a URL like other mirrors).
The mirror is maintained locally (within the Spack installation directory) at :file:`var/spack/cache/`.
It is always enabled (and is always searched first when attempting to retrieve files for an installation) but can be cleared with ``spack clean --misc-cache``; the cache directory can also be deleted manually without issue.

Caching includes retrieved tarball archives and source control repositories, but only resources with an associated digest or commit ID (e.g. a revision number for SVN) will be cached.
