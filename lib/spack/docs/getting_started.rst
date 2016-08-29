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

Clean Environment
~~~~~~~~~~~~~~~~~~

Many packages' installs can be broken by changing environment
variables.  For example, a packge might pick up the wrong build-time
dependencies (most of them not specified) depending on the setting of
``PATH``.  ``GCC`` seems to be particularly vulnerable to these issues.

Therefore, it is recommended that Spack users run with a *clean
environment*, especially for ``PATH``.  Only software that comes with
the system, or that you know you wish to use with Spack, should be
included.  This procedure will avoid many strange build errors that no
one knows how to fix.


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

Bootstrapping
--------------

Although Spack itself does not needinstallation, it is 

Install Environment Modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to use Spack's generated environment modules, you must have
installed the *Environment Modules* package.  On many Linux
distributions, this can be installed from the vendor's repository.
For example: ```yum install environment-modules``
(Fedora/RHEL/CentOS).  If your Linux distribution does not have
Environment Modules, you can get it with Spack:

1. Consider using system tcl.  If so, add to ``packages.yaml``::

    packages:
        tcl:
            paths:
                tcl@8.5: /usr
            version: [8.5]
            buildable: False
2. Install with::

    spack install environment-modules

3. Activate with::

    TMP=`tempfile`
    echo >$TMP
    MODULE_HOME=`spack location -i environment-modules`
    MODULE_VERSION=`ls -1 $MODULE_HOME/Modules | head -1`
    ${MODULE_HOME}/Modules/${MODULE_VERSION}/bin/add.modules <$TMP
    cp .bashrc $TMP
    echo "MODULE_VERSION=${MODULE_VERSION}" > .bashrc
    cat $TMP >>.bashrc

This adds to your ``.bashrc`` (or similar) files, enabling Environment
Modules when you log in.  Re-load your .bashrc (or log out and in
again), and then test that the ``module`` command is found with:

    module avail





git
binutils
