.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. meta::
   :description lang=en:
      Learn how to use Spack environments to manage reproducible software stacks on a local machine.

Spack Environments
==================

Spack is a powerful package manager designed for the complex software needs of supercomputers.
These same robust features for managing versions and dependencies also make it an excellent tool for local development on a laptop or workstation.

If you are used to tools like Conda, Homebrew or pip for managing local command-line tools and development projects, you will find Spack environments to be a powerful and flexible alternative.
Spack environments allow you to create self-contained, reproducible software collections, a concept similar to Conda environments and Python's virtual environments.

Unlike other package managers, Spack environments do not contain copies of the software themselves.
Instead, they reference installations in the Spack store, which is a central location where Spack keeps all installed packages.
This means that multiple environments can share the same package installations, saving disk space and reducing duplication.

In this section, we will walk through creating a simple environment to manage a personal software stack.

Creating and Activating an Environment
--------------------------------------

First, let's create and activate a new environment.
This places you "inside" the environment, so all subsequent Spack commands apply to it by default.

.. code-block:: console

   $ spack env create myenv
   ==> Created environment myenv in /path/to/spack/var/spack/environments/myenv
   $ spack env activate myenv

Here, *myenv* is the name of our new environment.

You can verify you are in the environment using:

.. code-block:: console

   $ spack env status
   ==> In environment myenv

Adding Specs to the Environment
-------------------------------

Now that our environment is active, we can add the packages we want to install.
Let's say we want a newer version of curl and a few Python libraries.

.. code-block:: spec

   $ spack add curl@8 python py-numpy py-scipy py-matplotlib

You can add packages one at a time or all at once.
Notice that we didn't need to specify the environment name, as Spack knows we are working inside ``myenv``.
These packages are now added to the environment's manifest file, ``spack.yaml``.

You can view the manifest at any time by running:

.. code-block:: console

   $ spack config edit

This will open your ``spack.yaml``, which should look like this:

.. code-block:: yaml
   :caption: Example ``spack.yaml`` for our environment

   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs:
     - curl@8
     - python
     - py-numpy
     - py-scipy
     - py-matplotlib
     view: true
     concretizer:
       unify: true

The ``view: true`` setting tells Spack to create a single directory where all executables, libraries, etc., are symlinked together, similar to a traditional Unix prefix.
By default, this view is located inside the environment directory.

Installing the Software
-----------------------

With our specs defined, the next step is to have Spack solve the dependency graph.
This is called "concretization."

.. code-block:: console

   $ spack concretize
   ==> Concretized ...
    ...

Spack will find a consistent set of versions and dependencies for the packages you requested.
Once this is done, you can install everything with a single command:

.. code-block:: console

   $ spack install

Spack will now download, build, and install all the necessary packages.
After the installation is complete, the environment's view is automatically updated.
Because the environment is active, your ``PATH`` and other variables are already configured.

You can verify the installation:

.. code-block:: console

   $ which python3
   /path/to/spack/var/spack/environments/myenv/.spack-env/view/bin/python3

When you are finished working in the environment, you can deactivate it:

.. code-block:: console

   $ spack env deactivate

Keeping Up With Updates
-----------------------

Over time, you may want to update the packages in your environment to their latest versions.
Spack makes this easy.

First, update Spack's package repository to make the latest package versions available:

.. code-block:: console

   $ spack repo update

Then, activate the environment, re-concretize and reinstall.

.. code-block:: console

   $ spack env activate myenv
   $ spack concretize --fresh-roots --force
   $ spack install

The ``--fresh-roots`` flag tells the concretizer to prefer the latest available package versions you've added explicitly to the environment, while allowing existing dependencies to remain unchanged if possible.
Alternatively, you can use the ``--fresh`` flag to prefer the latest versions of all packages including dependencies, but that might lead to longer install times and more changes.
The ``--force`` flag allows it to overwrite the previously solved dependencies.
The ``install`` command is smart and will only build packages that are not already installed for the new configuration.

Cleaning Up Old Packages
------------------------

After an update, you may have old, unused packages taking up space.
You can safely remove any package that is no longer part of an environment's dependency tree.

.. code-block:: console

   $ spack gc --except-any-environment

This runs Spack's garbage collector, which will find and uninstall any package versions that are no longer referenced by *any* of your environments.

Removing the Environment
------------------------

If you no longer need an environment, you can completely remove it.

First, ensure the environment is not active:

.. code-block:: console

    $ spack env deactivate

Then, remove the environment.

.. code-block:: console

   $ spack env rm myenv

This removes the environment's directory and its view, but the packages that were installed for it remain in the Spack store.
To actually remove the installations from the Spack store and free up disk space, you can run the garbage collector again.

.. code-block:: console

   $ spack gc --except-any-environment

This command will safely uninstall any packages that are no longer referenced by any of your remaining environments.

Next steps
----------

Spack has many other features for managing software environments.
See :doc:`environments` for more advanced usage.
