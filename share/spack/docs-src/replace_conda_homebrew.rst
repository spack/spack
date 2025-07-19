.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _spack-environments-basic-usage:

==================
Spack Environments
==================

Spack is an incredibly powerful package manager, designed for supercomputers where users have diverse installation needs.
But Spack can also be used to handle simple single-user installations on your laptop.
Most macOS users are already familiar with package managers like Homebrew and Conda, where all installed packages are symlinked to a single central location like ``/usr/local``.
In this section, we will show you how to emulate the behavior of Homebrew/Conda using :ref:`Spack environments <environments>`!

--------------------------
Creating a New Environment
--------------------------

First, let's create a new environment.
We'll assume that Spack is already set up correctly, and that you've already sourced the setup script for your shell.
To create, and activate, a new environment, simply run:

.. code-block:: console

   $ spack env create myenv

Here, *myenv* can be anything you want to name your environment.
Next, we can add a list of packages we would like to install into our environment.
Let's say we want a newer version of Bash than the one that comes with macOS, and we want a few Python libraries.
We can run:

.. code-block:: console

   $ spack -e myenv add bash@5 python py-numpy py-scipy py-matplotlib

Each package can be listed on a separate line, or combined into a single line like we did above.
Notice that we're explicitly asking for Bash 5 here.
You can use any spec you would normally use on the command line with other Spack commands.
If you run the following command:

.. code-block:: console

   $ spack -e myenv config edit

you'll see how your ``spack.yaml`` looks like:

.. code-block:: yaml

   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs:
     - bash@5
     - python
     - py-numpy
     - py-scipy
     - py-matplotlib
     view: true
     concretizer:
       unify: true

-------------------------
Configuring View Location
-------------------------

Spack symlinks all installations to ``${SPACK_ROOT}/var/spack/environments/myenv/.spack-env/view``, which is the default when ``view: true``.
You can actually change this to any directory you want by editing the ``spack.yaml`` manifest file, or by using the following command:

.. code-block:: console

   $ spack -e myenv env view enable <path>

In order to access files in these locations, you need to update ``PATH`` and other environment variables to point to them.
Activating the Spack environment does this automatically, once the software is installed:

.. code-block:: console

   $ spack env activate -p myenv

For now, let's deactivate the environment, and proceed with installing the software:

.. code-block:: console

   $ spack env deactivate


-----------------------
Installing the Software
-----------------------

Once the manifest file is properly defined, you may want to update the ``builtin`` package repository using this command:

.. code-block:: console

   $ spack repo update

Then you can proceed concretizing the environment:

.. code-block:: console

   $ spack -e myenv concretize

This will tell you which packages, if any, are already installed, and alert you to any conflicting specs.

To actually install these packages and symlink them to your ``view:`` directory, simply run:

.. code-block:: console

   $ spack -e myenv install
   $ spack env activate myenv

Now, when you type ``which python3``, it should find the one you just installed.

.. admonition:: Add the new shell to the list of valid login shells
   :class: tip
   :collapsible:

   In order to change the default shell to our newer Bash installation, we first need to add it to this list of acceptable shells.
   Run:

   .. code-block:: console

      $ sudo vim /etc/shells

   and add the absolute path to your bash executable. Then run:

   .. code-block:: console

      $ chsh -s /path/to/bash

   Now, when you log out and log back in, ``echo $SHELL`` should point to the newer version of Bash.


-----------------------
Keeping Up With Updates
-----------------------

Let's say you upgraded to a new version of macOS, or a new version of Python was released, and you want to rebuild your entire software stack.
To do this, simply run the following commands:

.. code-block:: console

   $ spack env activate myenv
   $ spack concretize --fresh --force
   $ spack install

The ``--fresh`` flag tells Spack to use the latest version of every package, where possible, instead of trying to reuse installed packages as much as possible.

The ``--force`` flag in addition tells Spack to overwrite its previous concretization decisions, allowing you to choose a new version of Python.
If any of the new packages like Bash are already installed, ``spack install`` won't re-install them, it will keep the symlinks in place.

------------------------
Cleaning Up Old Packages
------------------------

If we want to clean up old, out-of-date packages from our environment after an upgrade, here's how to upgrade our entire software stack and tidy up the old versions:

.. code-block:: console

   $ spack env activate myenv
   $ spack concretize --fresh --force
   $ spack install
   $ spack gc --except-any-environment

The final step, ``spack gc --except-any-environment``, runs Spack's garbage collector and removes any packages that are no longer needed by any managed Spack environment—which will clean up those old versions that got replaced during the upgrade.

------------------------
Removing the Environment
------------------------

If you need to remove ``myenv`` completely, the procedure is simple.
Just run:

.. code-block:: console

   $ spack env activate myenv
   $ spack uninstall --all
   $ spack env deactivate myenv
   $ spack env rm myenv

This will uninstall all packages in your environment, remove the symlinks, and finally remove the environment.
