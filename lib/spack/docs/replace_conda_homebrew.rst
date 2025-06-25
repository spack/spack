.. Copyright Spack Project Developers. See COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

=====================================
Spack for Homebrew/Conda Users
=====================================

Spack is an incredibly powerful package manager, designed for supercomputers where users have diverse installation needs.
But Spack can also be used to handle simple single-user installations on your laptop.
Most macOS users are already familiar with package managers like Homebrew and Conda, where all installed packages are symlinked to a single central location like ``/usr/local``.
In this section, we will show you how to emulate the behavior of Homebrew/Conda using :ref:`environments`!

-----
Setup
-----

First, let's create a new environment.
We'll assume that Spack is already set up correctly, and that you've already sourced the setup script for your shell.
To create a new environment, simply run:

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

Next, we want to manually configure a couple of things:

.. code-block:: console

   $ spack -e myenv config edit

.. code-block:: yaml

   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs: [bash@5, python, py-numpy, py-scipy, py-matplotlib]
     view: true

You can see the packages we added earlier in the ``specs:`` section.
If you ever want to add more packages, you can either use ``spack add`` or manually edit this file.

We also need to change the ``concretizer:unify`` option.
By default, Spack concretizes each spec *separately*, allowing multiple versions of the same package to coexist.
Since we want a single consistent environment, we want to concretize all of the specs *together*.

Here is what your ``spack.yaml`` looks like with this new setting:

.. code-block:: yaml

   # This is a Spack Environment file.
   #
   # It describes a set of packages to be installed, along with
   # configuration settings.
   spack:
     # add package specs to the `specs` list
     specs: [bash@5, python, py-numpy, py-scipy, py-matplotlib]
     view: true
     concretizer:
       unify: true

^^^^^^^^^^^^^^^^
Symlink location
^^^^^^^^^^^^^^^^

Spack symlinks all installations to ``/Users/me/spack/var/spack/environments/myenv/.spack-env/view``, which is the default when ``view: true``.
You can actually change this to any directory you want.
For example, Homebrew uses ``/usr/local``, while Conda uses ``/Users/me/anaconda``.
In order to access files in these locations, you need to update ``PATH`` and other environment variables to point to them.
Activating the Spack environment does this automatically, but you can also manually set them in your ``.bashrc``.

.. warning::

   There are several reasons why you shouldn't use ``/usr/local``:

   1. If you are on macOS 10.11+ (El Capitan and newer), Apple makes it hard
      for you. You may notice permissions issues on ``/usr/local`` due to their
      `System Integrity Protection <https://support.apple.com/en-us/HT204899>`_.
      By default, users don't have permissions to install anything in ``/usr/local``,
      and you can't even change this using ``sudo chown`` or ``sudo chmod``.
   2. Other package managers like Homebrew will try to install things to the
      same directory. If you plan on using Homebrew in conjunction with Spack,
      don't symlink things to ``/usr/local``.
   3. If you are on a shared workstation, or don't have sudo privileges, you
      can't do this.

   If you still want to do this anyway, there are several ways around SIP.
   You could disable SIP by booting into recovery mode and running
   ``csrutil disable``, but this is not recommended, as it can open up your OS
   to security vulnerabilities. Another technique is to run ``spack concretize``
   and ``spack install`` using ``sudo``. This is also not recommended.

   The safest way I've found is to create your installation directories using
   sudo, then change ownership back to the user like so:

   .. code-block:: bash

      for directory in .spack bin contrib include lib man share
      do
          sudo mkdir -p /usr/local/$directory
          sudo chown $(id -un):$(id -gn) /usr/local/$directory
      done

Depending on the packages you install in your environment, the exact list of directories you need to create may vary.
You may also find some packages like Java libraries that install a single file to the installation prefix instead of in a subdirectory.
In this case, the action is the same, just replace ``mkdir -p`` with ``touch`` in the for-loop above.

   But again, it's safer just to use the default symlink location.


------------
Installation
------------

To actually concretize the environment, run:

.. code-block:: console

   $ spack -e myenv concretize

This will tell you which packages, if any, are already installed, and alert you to any conflicting specs.

To actually install these packages and symlink them to your ``view:`` directory, simply run:

.. code-block:: console

   $ spack -e myenv install
   $ spack env activate myenv

Now, when you type ``which python3``, it should find the one you just installed.

In order to change the default shell to our newer Bash installation, we first need to add it to this list of acceptable shells.
Run:

.. code-block:: console

   $ sudo vim /etc/shells

and add the absolute path to your bash executable. Then run:

.. code-block:: console

   $ chsh -s /path/to/bash

Now, when you log out and log back in, ``echo $SHELL`` should point to the newer version of Bash.

-----------------------------
Updating Package Repositories
-----------------------------

Before we upgrade our installed packages, we can update our Spack package repositories that come from git repos (like Spack's default community package repository) with:

.. code-block:: console

    $ spack repo update

----------------------------
Upgrading Installed Packages
----------------------------

Let's say we upgraded to a new version of macOS, or a new version of Python was released, and we want to rebuild our entire software stack.
To do this, we'll run the following commands:

.. code-block:: console

   $ spack env activate myenv
   $ spack concretize --fresh --force
   $ spack install

The ``--fresh`` flag tells Spack to use the latest version of every package where it can, instead of trying to reuse what we've already got installed.

The ``--force`` flag in addition tells Spack to overwrite its previous concretization decisions, allowing us to choose a new version of Python.
If some of the new packages (like Bash) are already installed, ``spack install`` will skip re-installing them and reuse the existing installation.

.. note::
   We can save a lot of time rebuilding our environment if we instead run
   ``spack concretize --force --fresh-roots`` which will still upgrade all of
   our explicitly installed "root" packages in the enviornment, but will
   attempt to reuse existing libraries and lower level packages when possible.

------------------------------------
Upgrading & Cleaning Up Old Packages
------------------------------------

If we want to mimic what Homebrew does and clean up old, out-of-date packages from our environment after an upgrade, here's how to upgrade our entire software stack and tidy up the old versions:

.. code-block:: console

   $ spack env activate myenv
   $ spack concretize --force --fresh
   $ spack install
   $ spack gc --except-any-environment

The final step, ``spack gc --except-any-environment``, runs Spack's garbage collector and removes any packages that are no longer needed by any managed Spack environment—which will clean up those old versions that got replaced during the upgrade.

--------------
Uninstallation
--------------

If you decide that Spack isn't right for you, uninstallation is simple.
Just run:

.. code-block:: console

   $ spack env activate myenv
   $ spack uninstall --all

This will uninstall all packages in your environment and remove the symlinks.
