Getting Started
====================

Download
--------------------

Getting spack is easy.  You can clone it from the `github repository
<https://github.com/scalability-llnl/spack>`_ using this command:

.. code-block:: sh

   $ git clone https://github.com/scalability-llnl/spack.git

This will create a directory called ``spack``.  We'll assume that the
full path to this directory is in some environment called
``SPACK_HOME``.  Add ``$SPACK_HOME/bin`` to your path and you're ready
to go:

.. code-block:: sh

   $ export PATH=spack/bin:$PATH
   $ spack install libelf

In general, most of your interactions with Spack will be through the
``spack`` command.


Install
--------------------

You don't need to install Spack; it's ready to run as soon as you
clone it from git.

You may want to run it out of a prefix other than the git repository
you cloned.  The ``spack bootstrap`` command provides this
functionality.  To install spack in a new directory, simply type:

.. code-block:: sh

    $ spack bootstrap /my/favorite/prefix

This will install a new spack script in /my/favorite/prefix/bin, which
you can use just like you would the regular spack script.  Each copy
of spack installs packages into its own ``$PREFIX/opt`` directory.
