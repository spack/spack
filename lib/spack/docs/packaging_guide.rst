Packaging Guide
=====================

This guide is intended for developers or administrators who want to
*package* their software so that Spack can install it.  We assume that
you have at least some familiarty with Python, and that you've read
the :ref:`basic usage guide <basic_usage>`, especially the part
about :ref:`specs <sec-specs>`.

There are two key parts of Spack:

   #. **specs**: a language for describing builds of software, and
   #. **packages**: Python modules that build software according to a
      spec.

The package allows the developer to encapsulate build logic for
different versions, compilers, and platforms in one place.

Packages in Spack are written in pure Python, so you can do anything
in Spack that you can do in Python.  Python was chosen as the
implementation language for two reasons.  First, Python is getting to
be ubiquitous in the HPC community due to its use in numerical codes.
Second, it's a modern language and has many powerful features to help
make package writing easy.

Finally, we've gone to great lengths to make it *easy* to create
packages.  The ``spack create`` command lets you generate a
boilerplate package template from a tarball URL, and ideally you'll
only need to run this once and slightly modify the boilerplate to get
your package working.

This section of the guide goes through the parts of a package, and
then tells you how to make your own.  If you're impatient, jump ahead
to :ref:`spack-create`.

Directory Structure
---------------------------

A Spack installation directory is structured like a standard UNIX
install prefix (``bin``, ``lib``, ``include``, ``share``, etc.).  Most
of the code for Spack lives in ``$SPACK_ROOT/lib/spack``, and this is
also the top-level include directory for Python code.  When Spack
runs, it adds this directory to its ``PYTHONPATH``.

Spack packages live in the ``spack.packages`` Python package, which
means that they need to go in ``$prefix/lib/spack/spack/packages``.
If you list that directory, you'll see all the existing packages:

.. command-output::  cd $SPACK_ROOT/lib/spack/spack/packages;  ls *.py
   :shell:
   :ellipsis: 5

``__init__.py`` contains some utility functions used by Spack to load
packages when they're needed for an installation.  All the other files
in the ``packages`` directory are actual Spack packages used to
install software.

Parts of a package
---------------------------

It's probably easiest to learn about packages by looking at an
example.  Let's take a look at ``libelf.py``:

.. literalinclude:: ../spack/packages/libelf.py
   :linenos:

Package Names
~~~~~~~~~~~~~~~~~~

This package lives in a file called ``libelf.py``, and it contains a
class called ``Libelf``.  The ``Libelf`` class extends Spack's
``Package`` class (and this is what makes it a Spack package).  The
*file name* is what users need to provide in their package
specs. e.g., if you type any of these:

.. code-block:: sh

   spack install libelf
   spack install libelf@0.8.13

Spack sees the package name in the spec and looks for a file called
``libelf.py`` in its ``packages`` directory.  Likewise, if you say
``spack install docbook-xml``, then Spack looks for a file called
``docbook-xml.py``.

We use the filename for the package name to give packagers more
freedom in naming their packages. Package names can contain letters,
numbers, dashes, and underscores, and there are no other restrictions.
You can name a package ``3proxy`` or ``_foo`` and Spack won't care --
it just needs to see that name in the package spec.  Experienced
Python programmers will notice that package names are actually Python
module names, and but they're not necessarily valid Python
identifiers.  i.e., you can't actually ``import 3proxy`` in Python.
You'll get a syntax error because the identifier doesn't start with a
letter or underscore.  For more details on why this is still ok, see
the :ref:`developer guide<developer_guide>`.

.. literalinclude:: ../spack/packages/libelf.py
   :linenos:
   :lines: 3

The *class name* is formed by converting words separated by `-` or
``_`` in the file name to camel case.  If the name starts with a
number, we prefix the class name with ``Num_``. Here are some
examples:

=================  =================
 Module Name         Class Name
=================  =================
 ``foo_bar``         ``FooBar``
 ``docbook-xml``     ``DocbookXml``
 ``FooBar``          ``Foobar``
 ``3proxy``          ``Num_3proxy``
=================  =================

The class name is needed by Spack to properly import a package, but
not for much else.  In general, you won't have to remember this naming
convention because ``spack create`` will generate a boilerplate class
for you, and you can just fill in the blanks.


Metadata
~~~~~~~~~~~~~~~~~~~~

Just under the class name is a description of the ``libelf`` package.
In Python, this is called a *docstring*, and it's a multi-line,
triple-quoted (``"""``) string that comes just after the definition of
a class.  Spack uses the docstring to generate the description of the
package that is shown when you run ``spack info``.  If you don't provide
a description, Spack will just print "None" for the description.

In addition the package description, there are a few fields you'll
need to fill out.  They are as follows:

``homepage``
    This is the URL where you can learn about the package and get
    information.  It is displayed to users when they run ``spack info``.

``url``
    This is the URL where you can download a distribution tarball of
    the pacakge's source code.

``versions``
    This is a `dictionary
    <http://docs.python.org/2/tutorial/datastructures.html#dictionaries>`_
    mapping versions to MD5 hashes.  Spack uses the hashes to checksum
    archives when it downloads a particular version.

The homepage and URL are required fields, and ``versions`` is not
required but it's recommended.  Spack will warn usrs if they try to
install a spec (e.g., ``libelf@0.8.10`` for which there is not a
checksum available.  They can force it to download the new version and
install, but it's better to provide checksums so users don't have to
install from an unchecked archive.


Install function
~~~~~~~~~~~~~~~~~~~~~~~

The last element of the ``libelf`` package is its ``install()``
function.  This is where the real work of installation happens, and
it's the main part of the package you'll need to customize for each
piece of software.

When a user runs ``spack install``, Spack fetches an archive for the
correct version of the software, expands the archive, and sets the
current working directory to the root directory of the expanded
archive.  It then instantiates a package object and calls its
``install()`` method.

Install takes a ``spec`` object and a ``prefix`` path:

.. literalinclude:: ../spack/packages/libelf.py
   :start-after: 0.8.12

We'll talk about ``spec`` objects and the types of methods you can
call on them later.  The ``prefix`` is the path to the directory where
the package should install the software after it is built.

Inside of the ``install()`` function, things should look pretty
familiar.  ``libelf`` uses autotools, so the package first calls
``configure``, passing the prefix and some other package-specific
arguments.  It then calls ``make`` and ``make install``.

``configure`` and ``make`` look very similar to commands you'd type in
a shell, but they're actually Python functions.  Spack provides these
wrapper functions to allow you to call commands more naturally when
you write packages.  This allows spack to provide some special
features, as well.  For example, in Spack, ``make`` is parallel by
default. Spack figures out the number of cores on your machine and
passes and appropriate value for ``-j<numjobs>`` to the ``make``
command.  In a package file, you can supply a keyword argument,
``parallel=False``, to disable parallel make.  We do it here to avoid
some race conditions in ``libelf``\'s ``install`` target.  The first
call to ``make()``, which does not have a keyword argument, will still
build in parallel.

We'll go into more detail about shell command functions in later
sections.


.. _spack-create:

Creating Packages Automatically
----------------------------------

``spack create``
~~~~~~~~~~~~~~~~~~~~~

The ``spack create`` command takes the drudgery out of making
packages.  It generates boilerplate code that conforms to Spack's idea
of a package should be, so that you can focus on getting your pacakge
working.

All you need is the URL to a tarball you want to package:

.. code-block:: sh

   $ spack create http://www.cmake.org/files/v2.8/cmake-2.8.12.1.tar.gz

When you run this, Spack will look at the tarball URL, and it will try
to figure out the of the package to be created. It also tries to
figure out what version strings for that package look like.  Once that
is done, it tries to find *additional* versions by spidering the
package's webpage.  Spack then prompts you to tell it how many
versions you want to download and checksum.

.. code-block:: sh

   ==> Creating template for package cmake
   ==> Found 18 versions of cmake.
     2.8.12.1  http://www.cmake.org/files/v2.8/cmake-2.8.12.1.tar.gz
     2.8.12    http://www.cmake.org/files/v2.8/cmake-2.8.12.tar.gz
     2.8.11.2  http://www.cmake.org/files/v2.8/cmake-2.8.11.2.tar.gz
     2.8.11.1  http://www.cmake.org/files/v2.8/cmake-2.8.11.1.tar.gz
     2.8.11    http://www.cmake.org/files/v2.8/cmake-2.8.11.tar.gz
     2.8.10.2  http://www.cmake.org/files/v2.8/cmake-2.8.10.2.tar.gz
     2.8.10.1  http://www.cmake.org/files/v2.8/cmake-2.8.10.1.tar.gz
     2.8.10    http://www.cmake.org/files/v2.8/cmake-2.8.10.tar.gz
     2.8.9     http://www.cmake.org/files/v2.8/cmake-2.8.9.tar.gz
     ...
     2.8.0     http://www.cmake.org/files/v2.8/cmake-2.8.0.tar.gz

   Include how many checksums in the package file? (default is 5, q to abort)

Spack will automatically download the number of tarballs you specify
(starting with the most recent) and checksum each of them.

Note that you don't need to do everything up front.  If your package
is large, you can always choose to download just one tarball for now,
then run :ref:`spack checksum <spack-checksum>` later if you end up wanting more.  Let's
say, for now, that you opted to download 3 tarballs:

.. code-block:: sh

   Include how many checksums in the package file? (default is 5, q to abort) 3
   ==> Downloading...
   ==> Fetching http://www.cmake.org/files/v2.8/cmake-2.8.12.1.tar.gz
   ######################################################################    98.6%
   ==> Fetching http://www.cmake.org/files/v2.8/cmake-2.8.12.tar.gz
   #####################################################################     96.7%
   ==> Fetching http://www.cmake.org/files/v2.8/cmake-2.8.11.2.tar.gz
   ####################################################################      95.2%

Now Spack generates some boilerplate and open the package file in
your favorite ``$EDITOR``:

.. code-block:: python
   :linenos:

   # FIXME:
   # This is a template package file for Spack.  We've conveniently
   # put "FIXME" labels next to all the things you'll want to change.
   #
   # Once you've edited all the FIXME's, delete this whole message,
   # save this file, and test out your package like this:
   #
   #     spack install cmake
   #
   # You can always get back here to change things with:
   #
   #     spack edit cmake
   #
   # See the spack documentation for more information on building
   # packages.
   #
   from spack import *

   class Cmake(Package):
       """FIXME: put a proper description of your package here."""
       # FIXME: add a proper url for your package's homepage here.
       homepage = "http://www.example.com"
       url      = "http://www.cmake.org/files/v2.8/cmake-2.8.12.1.tar.gz"

       versions = { '2.8.12.1' : '9d38cd4e2c94c3cea97d0e2924814acc',
                    '2.8.12'   : '105bc6d21cc2e9b6aff901e43c53afea',
                    '2.8.11.2' : '6f5d7b8e7534a5d9e1a7664ba63cf882', }

       def install(self, spec, prefix):
           # FIXME: Modify the configure line to suit your build system here.
           configure("--prefix=%s" % prefix)

           # FIXME: Add logic to build and install here
           make()
           make("install")

The tedious stuff (creating the class, checksumming archives) has been
done for you.

All the things you still need to change are marked with ``FIXME``
labels.  The first ``FIXME`` refers to the commented instructions at
the top of the file.  You can delete these after reading them.  The
rest of them are as follows:

   #. Add a description in your package's docstring.
   #. Change the homepage to a useful URL (not ``example.com``).
   #. Get the ``install()`` method working.


``spack edit``
~~~~~~~~~~~~~~~~~~~~

Once you've created a package, you can go back and edit it using
``spack edit``.  For example, this:

.. code-block:: sh

   spack edit libelf

will open ``$SPACK_ROOT/lib/spack/spack/packages/libelf.py`` in
``$EDITOR``.  If you try to edit a package that doesn't exist, Spack
will recommend using ``spack create``:

.. code-block:: sh

   $ spack edit foo
   ==> Error: No package 'foo'.  Use spack create, or supply -f/--force to edit a new file.

And, finally, if you *really* want to skip all the automatic stuff
that ``spack create`` does for you, then you can run ``spack edit
-f/--force``:

   $ spack edit -f foo

Which will generate a *very* minimal package structure for you to fill
in:

.. code-block:: python
   :linenos:

   from spack import *

   class Foo(Package):
       """Description"""

       homepage = "http://www.example.com"
       url      = "http://www.example.com/foo-1.0.tar.gz"

       versions = { '1.0' : '0123456789abcdef0123456789abcdef' }

       def install(self, spec, prefix):
           configure("--prefix=%s" % prefix)
           make()
           make("install")

We recommend using this only when you have to, as it's generally more
work than using ``spack create``.


.. _spack-checksum:

``spack checksum``
~~~~~~~~~~~~~~~~~~~~~~

If you've already created a package and you want to add more version
checksums to it, this is automated with ``spack checksum``.  Here's an
example for ``libelf``:

.. code-block:: sh

   $ spack checksum libelf
   ==> Found 16 versions of libelf.
     0.8.13    http://www.mr511.de/software/libelf-0.8.13.tar.gz
     0.8.12    http://www.mr511.de/software/libelf-0.8.12.tar.gz
     0.8.11    http://www.mr511.de/software/libelf-0.8.11.tar.gz
     0.8.10    http://www.mr511.de/software/libelf-0.8.10.tar.gz
     0.8.9     http://www.mr511.de/software/libelf-0.8.9.tar.gz
     0.8.8     http://www.mr511.de/software/libelf-0.8.8.tar.gz
     0.8.7     http://www.mr511.de/software/libelf-0.8.7.tar.gz
     0.8.6     http://www.mr511.de/software/libelf-0.8.6.tar.gz
     0.8.5     http://www.mr511.de/software/libelf-0.8.5.tar.gz
     ...
     0.5.2     http://www.mr511.de/software/libelf-0.5.2.tar.gz

   How many would you like to checksum? (default is 5, q to abort)

This does the same thing that ``spack create`` did, it just allows you
to go back and create more checksums for an existing package.  It
fetches the tarballs you ask for and prints out a dict ready to copy
and paste into your package file:

.. code-block:: sh

   ==> Checksummed new versions of libelf:
     {
         '0.8.13' : '4136d7b4c04df68b686570afa26988ac',
         '0.8.12' : 'e21f8273d9f5f6d43a59878dc274fec7',
         '0.8.11' : 'e931910b6d100f6caa32239849947fbf',
         '0.8.10' : '9db4d36c283d9790d8fa7df1f4d7b4d9',
     }

You should be able to add these checksums directly to the versions
field in your package.

Note that for ``spack checksum`` to work, Spack needs to be able to
``import`` your pacakge in Python.  That means it can't have any
syntax errors, or the ``import`` will fail.  Use this once you've got
your package in working order.


Dependencies
------------------------------


Virtual dependencies
-----------------------------


Install environment
-----------------------------



Package lifecycle
------------------------------

The ``spack install`` command performs a number of tasks before it
finally installs each package.  It downloads an archive, expands it in
a temporary directory, and then performs the installation.  Spack has
several commands that allow finer-grained control over each stage of
the build process.


``spack fetch``
~~~~~~~~~~~~~~~~~

The first step of ``spack install``.  Takes a spec and determines the
correct download URL to use for the requested package version, then
downloads the archive, checks it against an MD5 checksum, and stores
it in a staging directory if the check was successful.  The staging
directory will be located under ``$SPACK_HOME/var/spack``.

When run after the archive has already been downloaded, ``spack
fetch`` is idempotent and will not download the archive again.

``spack stage``
~~~~~~~~~~~~~~~~~

The second step in ``spack install`` after ``spack fetch``.  Expands
the downloaded archive in its temporary directory, where it will be
built by ``spack install``.  Similar to ``fetch``, if the archive has
already been expanded,  ``stage`` is idempotent.

``spack clean``
~~~~~~~~~~~~~~~~~

There are several variations of ``spack clean``.  With no arguments,
``spack clean`` runs ``make clean`` in the expanded archive directory.
This is useful if an attempted build failed, and something needs to be
changed to get a package to build.  If a particular package does not
have a ``make clean`` target, this will do nothing.

``spack clean -w / --work``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Deletes the entire build directory and re-expands it from the downloaded
archive. This is useful if a package does not support a proper ``make clean``
target.

``spack clean -d / --dist``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Deletes the build directory *and* the downloaded archive.  If
``fetch``, ``stage``, or ``install`` are run again after this, the
process will start from scratch, and the archive archive will be
downloaded again.  Useful if somehow a bad archive is downloaded
accidentally and needs to be cleaned out of the staging area.

``spack purge``
~~~~~~~~~~~~~~~~~

Cleans up *everything* in the build directory.  You can use this to
recover disk space if temporary files from interrupted or failed
installs accumulate in the staging area.


Dirty Installs
~~~~~~~~~~~~~~~~~~~

By default, ``spack install`` will delete the staging area once a
pacakge has been successfully built and installed, *or* if an error
occurs during the build.  Use ``spack install --dirty`` or ``spack
install -d`` to leave the build directory intact.  This allows you to
inspect the build directory and potentially fix the build.  You can
use ``purge`` or ``clean`` later to get rid of the unwanted temporary
files.






``spack graph``
~~~~~~~~~~~~~~~~~~~~
