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

^^^^^^^^^^^^^^^^^^^^^^^
Installing the Software
^^^^^^^^^^^^^^^^^^^^^^^

Now that the environment is active, you can install the software from
source or, if available, binary cache (as described below) and begin
development. 

The software will need to be installed *before* creating the binary
cache. This is done using the following command:

.. code-block:: console

    $ spack install

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Creating a Local Build Cache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now let's cover creation and use of a local build cache.
Assuming the project doesn't already have one set up and the goal
is to share it on the local file system, you can create one. First
you'll need to:

#. activate the development environment; and
#. install the software

using the processes described above.

Now you can create a local build cache on the file system by:

* re-using or creating a GPG signing key with user id
  ``$USER_ID`` and email ``$EMAIL``;
* creating a Spack mirror in the shared directory (``$MIRROR_DIR``);
* create the source build cache; and
* create the binary build cache.

Establishing the GPG Signing Key
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can re-use or create a GPG signing key

If you already have a key you want to use, you can provide it to
the ``spack buildcache create`` command. Review your signing keys
with the ``spack gpg list`` command. For example,

.. code-block:: console

    $ spack gpg list --signing
    /home/user/spack/opt/spack/gpg/pubring.gpg
    -------------------------------------------------
    pub   4096R/AC30B582 2021-04-01
    uid                  user (GPG created for Spack) <user1@llnl.gov>

    pub   4096R/561130C0 2021-12-01
    uid                  user1 (GPG created for Spack) <user1@llnl.gov>

In this case there are two signing keys, one with the ``$USER_ID`` of
``user`` and the other ``user1``.

If you don't have a signing key, you can create one using the commands:

.. code-block:: console

    $ spack gpg create $USER_ID $EMAIL
    $ mkdir $HOME/private_gpg_backup
    $ cp $SPACK_ROOT/opt/spack/gpg/*.gpg $HOME/private_gpg_backup
    $ cp $SPACK_ROOT/opt/spack/gpg/pubring.* $MIRROR_DIR
    $ chgrp $GROUP $MIRROR_DIR/pubring.*

Note ``$MIRROR_DIR`` is assumed to belong to and be accessible by all
members of the ``$GROUP`` group.

Creating the Spack mirror
~~~~~~~~~~~~~~~~~~~~~~~~~

Create the Spack mirror for all installed packages from the active
development environment. 

.. code-block:: console

    $ spack mirror create -d $MIRROR_DIR --all
    $ chmod -R g+rws $MIRROR_DIR

This creates a source cache mirror, which can form the basis for the
binary cache mirror.

.. note::

   You can add the ``-D`` option to the ``spack`` command if you also
   want dependencies of the development environment to be cached.


Creating the Binary Build Cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create the binary build cache leveraging the results from the source
cache. Start by adding the mirror to Spack's list and creating a
``build_cache`` subdirectory within the mirror:

.. code-block:: console

    $ spack mirror add $MY_DEV_ENV $MIRROR_DIR
    $ mkdir -p $MIRROR_DIR/build_cache

If you are re-using a signing key, you can provide its ``$USER_ID``
using the ``-k`` option during creation:

.. code-block:: console

    $ spack buildcache create --allow-root --force \
      -k $USER_ID -d $MIRROR_DIR --all

Otherwise, you can skip the option:

.. code-block:: console

    $ spack buildcache keys --install --trust
    $ spack buildcache create --allow-root --force -d $MIRROR_DIR --all

.. note::

   Adding the ``--only=package`` option to ``spack buildcache``
   will **exclude dependencies** from the build cache.

Once the build cache is created, make sure the team's group has
access permissions:

.. code-block:: console

    $ chmod -R g+rws $MIRROR_DIR/build_cache

.. note::

   You can add and remove packages from the environment but will have
   to re-create the buildcache with the command above to modify the
   cache.


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
