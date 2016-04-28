Getting Started
====================

Download
--------------------

Getting spack is easy.  You can clone it from the `github repository
<https://github.com/llnl/spack>`_ using this command:

.. code-block:: sh

   $ git clone https://github.com/llnl/spack.git

This will create a directory called ``spack``.  We'll assume that the
full path to this directory is in the ``SPACK_ROOT`` environment
variable.  Add ``$SPACK_ROOT/bin`` to your path and you're ready to
go:

.. code-block:: sh

   $ export PATH=$SPACK_ROOT/bin:$PATH
   $ spack install libelf

For a richer experience, use Spack's `shell support
<http://software.llnl.gov/spack/basic_usage.html#environment-modules>`_:

.. code-block:: sh

   # For bash users
   $ . $SPACK_ROOT/share/spack/setup-env.sh

   # For tcsh or csh users (note you must set SPACK_ROOT)
   $ setenv SPACK_ROOT /path/to/spack
   $ source $SPACK_ROOT/share/spack/setup-env.csh

This automatically adds Spack to your ``PATH``.

Installation
--------------------

You don't need to install Spack; it's ready to run as soon as you
clone it from git.

You may want to run it out of a prefix other than the git repository
you cloned.  The ``spack bootstrap`` command provides this
functionality.  To install spack in a new directory, simply type:

.. code-block:: sh

    $ spack bootstrap /my/favorite/prefix

This will install a new spack script in ``/my/favorite/prefix/bin``,
which you can use just like you would the regular spack script.  Each
copy of spack installs packages into its own ``$PREFIX/opt``
directory.
