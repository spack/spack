Basic usage
=====================

Nearly everything you do wtih spack will involve the ``spack``
command.  Like many well-known tools (``git``, ``cvs``, ``svn``,
``yum``, ``port``, ``apt-get``, etc.), ``spack`` is generally called
with a *subcommand* indicating the action you want to perform.

Getting Help
-----------------------


``spack help``
~~~~~~~~~~~~~~~~~~~~~~

The first subcommand you should know is ``spack help``.  Run with no
arguments, it will give a list of all spack options and subcommands:

.. command-output:: spack help

If you want help on the usage of a particular subcommand, you can pass
it as an argument to ``spack help``:

.. command-output:: spack help install

Alternately, you can use ``spack -h`` in place of ``spack help``, or
``spack <subcommand> -h`` to get help on a particular subcommand.


Viewing available packages
------------------------------

The first thing you will likely want to do with spack is find out what
software is available to install.  There are two main commands for
this: ``spack list`` and ``spack info``.


``spack list``
~~~~~~~~~~~~~~~~

The ``spack list`` command does what you might expect. it prints out a
list of all the available packages you can install.  Use it like
this:

.. command-output:: spack list

The packages are listed by name in alphabetical order.  If you just
want to see *installed* packages, you should use ``spack list -i``


``spack info``
~~~~~~~~~~~~~~~~

To get information on a particular package from the full list, you can
run ``spack info <package name>``.  e.g., for ``mpich``:

.. command-output:: spack info mpich

This gives basic information about the package, such as where it can
be downloaded, what other packages it depends on, virtual package
information, and a text description, if one is available.  We'll give
more details on dependencies and virtual dependencies later in this
guide.


Installing and uninstalling
------------------------------

``spack install``
~~~~~~~~~~~~~~~~~~~~~

You can install any package from ``spack list``, using ``spack
install``.  In the simplest case, if you just want the latest version
and you don't care about any configuration, you can just run ``spack
install <package>``:

.. code-block:: sh

   spack install mpileaks

This will fetch the tarball for ``mpileaks``, expand it, verify that
it was donwloaded without errors, build the package, and install it in
its own directory in ``$SPACK_HOME/opt``.  If the requested packages
depends on other packages in order to build, then they will also be
fetched and installed.

Spack also allows you to ask for *specific* configurations of a
package.  For example, if you want to install something with a
specific version, you can add ``@`` after the package name, followed
by the version you want:

.. code-block:: sh

   spack install mpich@3.0.4

You can install as many versions of the same pacakge as you want, and
they will not interfere with each other.  Spack installs each package
into its own unique prefix.  If you or another user links a library
against soething you install using Spack, it will continue to work
until you explicitly uninstall it.

The version isn't all that you can customize on a spack command line.
Spack can install many configurations, with different versions,
compilers, compiler versions, compile-time options (variants), and
even architectures (e.g., on a machine that requires cross-compiling).
Spack is also unique in that it lets you customize the *dependencies*
you build a package with.  That is, you could have two configurations
of the same version of a package: one built with boost 1.39.0, and the
other version built with version 1.43.0.

Spack calls the descriptor used to refer to a particular package
configuration a **spec**.  In the command lines above, both
``mpileaks`` and ``mpileaks@3.0.4`` are specs.  Specs and their syntax
are covered in more detail in :ref:`sec-specs`.




``spack uninstall``
~~~~~~~~~~~~~~~~~~~~~

To uninstall a package, just type ``spack uninstall <package>``.  This
will completely remove the directory in which the package was installed.

.. code-block:: sh

   spack uninstall mpich

If there are other installed packages depend on the package you're
uninstalling, spack will issue a warning to this effect.  In general,
you should remove the other packages *before* removing the package
they depend on, or you risk breaking packages on your system.  If you
still want to remove the package without regard for its dependencies,
you can run ``spack uninstall -f <package>`` to override Spack's
warning.

If you have more than one version of the same package installed, spack
may not be able to figure out which on eyou want uninstalled.  For
example, if you have both ``mpich@3.0.2`` and ``mpich@3.1`` installed,
and you type ``spack uninstall mpich``, then Spack will not know which
one you're referring to, and it will ask you to be more specific by
providing a version to differentiate, For example, ``spack uninstall
mpich@3.1`` is unambiguous.


.. _sec-specs:

Specs
-------------------------

Dependencies
-------------------------

Virtual dependencies
-------------------------

Versions, compilers, and architectures
----------------------------------------

``spack versions``
~~~~~~~~~~~~~~~~~~~~~~~~

``spack compilers``
~~~~~~~~~~~~~~~~~~~~~~~~

Architectures
~~~~~~~~~~~~~~~~~~~~~~~~

Spack's specs allow insatllations for multiple architectures to coexist
within the same prefix.  It is also intended to support multiple
architecutres for cross-compilation.


Package lifecycle
------------------------------

The ``spack install`` command performs a number of tasks before it
finally installs each package.  It downloads an archive, expands it in
a temporary directory, and only then performs the installation.  Spack
has several commands that allow finer-grained control over each of
these stages of the build process.


``spack fetch``
~~~~~~~~~~~~~~~~~

This is the first step of ``spack install``.  It takes a spec and
determines the correct download URL to use for the requested package
version.  It then downloads the archive, checks it against an MD5
checksum, and stores it in a staging directory if the check was
successful.  The staging directory will be located under
``$SPACK_HOME/var/spack``.

If run after the archive has already been downloaded, ``spack fetch``
is idempotent and will not download the archive again.

``spack stage``
~~~~~~~~~~~~~~~~~

This is the second step in installation after ``spack fetch``.  It
expands the downloaded archive in its temporary directory, where it
will be built by ``spack install``.  If the archive has already been
expanded, then this command does nothing.

``spack clean``
~~~~~~~~~~~~~~~~~

This command has several variations, each undoing one of the
installation tasks.  They are:

``spack clean``
  Runs ``make clean`` in the expanded archive directory.  This is useful
  if an attempted  build failed, and something needs to be changed to get
  a package to build.  If a particular package does not have a ``make clean``
  target, this will do nothing.

``spack clean -w`` or ``spack clean --work``
  This deletes the entire build directory and re-expands it from the downloaded
  archive. This is useful if a package does not support a proper ``make clean``
  target.

``spack clean -d`` or ``spack clean --dist``
  This deletes the build directory *and* the downloaded archive.  If
  ``fetch``, ``stage``, or ``install`` are run again after this, the
  process will start from scratch, and the archive archive will be
  downloaded again.  Useful if somehow a bad archive is downloaded
  accidentally and needs to be cleaned out of the staging area.




``spack purge``
~~~~~~~~~~~~~~~~~
