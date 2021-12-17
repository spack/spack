.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _developer-workflow:

=====================
Developer Workflow
=====================

A Spack developer workflow environment is an independent (i.e., not managed
by Spack) environment specifying potentially constrained packages that the
team actively develops. The environment can be used to create and maintain
a build cache -- source and or binary -- of the root and dependency packages
used by the team.


-----------------
Getting Started
-----------------

You will need to set up an active Spack instance. If you haven't done
that yet, enter the following on the command line from wherever you want
your Spack instance to reside:

.. code-block:: console

    $ git clone https://github.com/spack/spack.git
    $ . spack/share/spack/setup-env.sh

.. note::

   The root directory of the Spack clone will be referred to here as
   ``$SPACK_ROOT``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Activating the Development Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have set up your Spack instance, you can activate the
development environment. Assuming ``$DEV_ENV`` contains the path
to the directory containing the development environment file, you
can activate the environment with:

.. code-block:: console

    $ cd $DEV_ENV
    $ spacktivate .

^^^^^^^^^^^^^^^^^^^^
Install the Software
^^^^^^^^^^^^^^^^^^^^

Now that the environment is active, you can install the software from
source or, if available, binary cache (as described below) and begin
development. 

The softwware will need to be installed *before* you creating the
binary cache. This is done using the following command:

.. code-block:: console

    $ spack install

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Creating a Local Build Cache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now let's cover creation and use of a local build cache.
Assuming the project doesn't already have one set up and the goal
is to share it on the local file system, you can create one. First
you'll need to:

* activate the development environment; and
* install the software

using the processes described above.

Now you can create a local build cache on the file system by:

* create or re-using a GPG signing key with user id
  ``$USER_ID`` and email ``$EMAIL``;
* creating a Spack mirror in the shared directory (``$MIRROR_DIR``);
* create the source build cache; and
* create the binary build cache.

The commands for creating a GPG signing key are:

.. code-block:: console

    $ spack gpg create $USER_ID $EMAIL
    $ mkdir $HOME/private_gpg_backup
    $ cp $SPACK_ROOT/opt/spack/gpg/*.gpg $HOME/private_gpg_backup
    $ cp $SPACK_ROOT/opt/spack/gpg/pubring.* $MIRROR_DIR
    $ chgrp $GROUP $MIRROR_DIR/pubring.*

Note ``$MIRROR_DIR`` is assumed to belong to and be accessible by all
members of the ``$GROUP`` group.

.. note::

   An existing signing key can be used.  (TODO: Add this to the process.)

Now create the Spack mirror for all installed packages from the active
development environment. You can add the ``-D`` option to the ``spack``
command if you also want dependencies of the development environment
to be cached.

.. code-block:: console

    $ spack mirror create -d $MIRROR_DIR --all
    $ chmod -R g+rws $MIRROR_DIR

This creates a source cache mirror, which can form the basis for the
binary cache mirror.

Now you can create the binary build cache leveraging the results from
the source cache. Adding the ``--only=package`` option to
``spack buildcache`` will **exclude dependencies** from the build
cache.

.. code-block:: console

    $ spack mirror add $MY_DEV_ENV $MIRROR_DIR
    $ spack buildcache keys --install --trust
    $ mkdir -p $MIRROR_DIR/build_cache
    $ spack buildcache create --allow-root --force -d $MIRROR_DIR --all
    $ chmod -R g+rws $MIRROR_DIR/build_cache

You can add/remove packages from the environment and re-create it
with the command above to modify the build cache.

---------------------------
Using the Local Build Cache
---------------------------

Team members will need to run the following command from their own
Spack instances to use the local build cache:

.. code-block:: console

    $ spack mirror add $MY_DEV_ENV $MIRROR_DIR
    $ spack buildcache keys --install --trust --force

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Set up your Development Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have the mirror added and a copy of the development
environment -- assumed below to be in ``$DEV_ENV`` directory --
enter the following commands:

.. code-block:: console

    $ cd $DEV_ENV
    $ spacktivate .
    $ spack install

to install the software.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Developing Software in the Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With the environment activate, you can begin development on one
or more packages within the environment. You'll need to tell Spack to:

* check out a **specific version** of each package for development;
* re-concretize the development environment; and
* rebuild the affected software.

Suppose you only want to work on one package, ``$PACKAGE``, for ``$VERSION``.
You would enter the following on the command line:

.. code-block:: console

    $ spack develop $PACKAGE@$VERSION
    $ spack concretize -f
    $ spack install

If you want to develop on multiple packages at the same time you
will call ``spack develop`` for each package before re-concretizing
the environment. This will result in the software being expanded
under your ``$DEV_ENV`` directory.

You can now make changes to the software.

When you're ready to rebuild the modified software, you simply need
to re-install it:

.. code-block:: console

    $ spack install

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Additional Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spack provides documentation and tutorials on the capabilities described
here. For more information:

* `Build Caches Documentation
  <https://spack.readthedocs.io/en/latest/binary_caches.html>`_
* `Developer Workflows Tutorial
  <https://spack-tutorial.readthedocs.io/en/latest/tutorial_developer_workflows.html>`_
* `Environments Documentation
  <https://spack.readthedocs.io/en/latest/environments.html>`_
* `Environments Tutorial
  <https://spack-tutorial.readthedocs.io/en/latest/tutorial_environments.html>`_
* `Mirrors Documentation
  <https://spack.readthedocs.io/en/latest/mirrors.html>`_
* `Mirror Tutorial
  <https://spack-tutorial.readthedocs.io/en/latest/tutorial_binary_cache.html>`_
* `Package Repositories Documentation
  <https://spack.readthedocs.io/en/latest/repositories.html>`_
