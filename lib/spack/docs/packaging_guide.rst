.. _packaging-guide:

Packaging Guide
=====================

This guide is intended for developers or administrators who want to
*package* their software so that Spack can install it.  We assume that
you have at least some familiarty with Python, and that you've read
the :ref:`basic usage guide <basic-usage>`, especially the part
about :ref:`specs <sec-specs>`.

There are two key parts of Spack:

   #. **Specs**: expressions for describing builds of software, and
   #. **Packages**: Python modules that build software according to a
      spec.

Package files allow a developer to encapsulate build logic for
different versions, compilers, and platforms in one place.  Specs
allow a user to describe a *particular* build in a way that a package
author can understand.

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

Package Files
---------------------------

It's probably easiest to learn about packages by looking at an
example.  Let's take a look at the ``libelf`` package:

.. literalinclude:: ../../../var/spack/packages/libelf/package.py
   :lines: 25-
   :linenos:

Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Spack installation directory is structured like a standard UNIX
install prefix (``bin``, ``lib``, ``include``, ``var``, ``opt``,
etc.).  Most of the code for Spack lives in ``$SPACK_ROOT/lib/spack``.
Packages themselves live in ``$SPACK_ROOT/var/spack/packages``.

If you ``cd`` to that directory, you will see directories for each
package:

.. command-output::  cd $SPACK_ROOT/var/spack/packages;  ls
   :shell:
   :ellipsis: 10

Each of these directories contains a file called ``package.py``.  This
file is where all the python code for a package goes.  For example,
the ``libelf`` package looks like this::

   $SPACK_ROOT/var/spack/packages/
       libelf/
           package.py

Alongside the ``package.py`` file, a package may contain extra files (like
patches) that it needs to build.


Package Names
~~~~~~~~~~~~~~~~~~

Packages are named after the directory containing ``package.py``.  So,
``libelf``'s ``package.py`` lives in a directory called ``libelf``.
The ``package.py`` file contains a class called ``Libelf``, which
extends Spack's ``Package`` class.  This is what makes it a Spack
package.  The **directory name** is what users need to provide on the
command line. e.g., if you type any of these:

.. code-block:: sh

   $ spack install libelf
   $ spack install libelf@0.8.13

Spack sees the package name in the spec and looks for
``libelf/package.py`` in ``var/spack/packages``.  Likewise, if you say
``spack install docbook-xml``, then Spack looks for
``docbook-xml/package.py``.

We use the directory name to packagers more freedom when naming their
packages. Package names can contain letters, numbers, dashes, and
underscores.  You can name a package ``3proxy`` or ``_foo`` and Spack
won't care -- it just needs to see that name in the package spec.
These aren't valid Python module names, but we allow them in Spack and
import ``package.py`` file dynamically.

Package class names
~~~~~~~~~~~~~~~~~~~~~~~

The **class name** (``Libelf`` in our example) is formed by converting
words separated by `-` or ``_`` in the file name to camel case.  If
the name starts with a number, we prefix the class name with
``_``. Here are some examples:

=================  =================
 Module Name         Class Name
=================  =================
 ``foo_bar``         ``FooBar``
 ``docbook-xml``     ``DocbookXml``
 ``FooBar``          ``Foobar``
 ``3proxy``          ``_3proxy``
=================  =================

The class name is needed by Spack to properly import a package, but
not for much else.  In general, you won't have to remember this naming
convention because ``spack create`` will generate a boilerplate class
for you, and you can just fill in the blanks.

.. _metadata:

Metadata
~~~~~~~~~~~~~~~~~~~~

Just under the class name is a description of the ``libelf`` package.
In Python, this is called a *docstring*: a multi-line, triple-quoted
(``"""``) string that comes just after the definition of a class.
Spack uses the docstring to generate the description of the package
that is shown when you run ``spack info``.  If you don't provide a
description, Spack will just print "None" for the description.

In addition to the package description, there are a few fields you'll
need to fill out.  They are as follows:

``homepage`` (required)
  This is the URL where you can learn about the package and get
  information.  It is displayed to users when they run ``spack info``.

``url`` (required)
  This is the URL where you can download a distribution tarball of
  the pacakge's source code.

``versions`` (optional)
  This is a `dictionary
  <http://docs.python.org/2/tutorial/datastructures.html#dictionaries>`_
  mapping versions to MD5 hashes.  Spack uses the hashes to checksum
  archives when it downloads a particular version.

``parallel`` (optional) Whether make should be parallel by default.
  By default, this is ``True``, and package authors need to call
  ``make(parallel=False)`` to override.  If you set this to ``False``
  at the package level then each call to ``make`` will be sequential
  by default, and users will have to call ``make(parallel=True)`` to
  override it.

``versions`` is optional but strongly recommended.  Spack will warn
usrs if they try to install a version (e.g., ``libelf@0.8.10`` for
which there is not a checksum available.  They can force it to
download the new version and install, but it's better to provide
checksums so users don't have to install from an unchecked archive.


Install method
~~~~~~~~~~~~~~~~~~~~~~~

The last element of the ``libelf`` package is its ``install()``
method.  This is where the real work of installation happens, and
it's the main part of the package you'll need to customize for each
piece of software.

.. literalinclude::  ../../../var/spack/packages/libelf/package.py
   :start-after: 0.8.12
   :linenos:

``install`` takes a ``spec``: a description of how the package should
be built, and a ``prefix``: the path to the directory where the
software should be installed.

:ref:`Writing the install method <install-method>` is documented in
detail later, but in general, the ``install()`` method should look
familiar.  ``libelf`` uses autotools, so the package first calls
``configure``, passing the prefix and some other package-specific
arguments.  It then calls ``make`` and ``make install``.

Spack provides wrapper functions for ``configure`` and ``make`` so
that you can call them in a similar way to how you'd call a shell
comamnd.  In reality, these are Python functions.  Spack provides
these functions to make writing packages more natural. See the section
on :ref:`shell wrappers <shell-wrappers>`.

.. _spack-create:

Creating Packages
----------------------------------

``spack create``
~~~~~~~~~~~~~~~~~~~~~

The ``spack create`` command takes the tedium out of making packages.
It generates boilerplate code for you, so that you can focus on
getting your package build working.

All you need is the URL to a tarball you want to package:

.. code-block:: sh

   $ spack create http://www.cmake.org/files/v2.8/cmake-2.8.12.1.tar.gz

When you run this, Spack will look at the tarball URL, and it will try
to figure out the name of the package to be created. It will also try
to figure out what version strings for that package look like.  Once
that is done, it tries to find *additional* versions by spidering the
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
then run :ref:`spack checksum <spack-checksum>` later if you end up
wanting more.  Let's say you chose to download 3 tarballs:

.. code-block:: sh

   Include how many checksums in the package file? (default is 5, q to abort) 3
   ==> Downloading...
   ==> Fetching http://www.cmake.org/files/v2.8/cmake-2.8.12.1.tar.gz
   ######################################################################    98.6%
   ==> Fetching http://www.cmake.org/files/v2.8/cmake-2.8.12.tar.gz
   #####################################################################     96.7%
   ==> Fetching http://www.cmake.org/files/v2.8/cmake-2.8.11.2.tar.gz
   ####################################################################      95.2%

Now Spack generates boilerplate code and opens the new
``package.py`` file in your favorite ``$EDITOR``:

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

       version('2.8.12.1', '9d38cd4e2c94c3cea97d0e2924814acc')
       version('2.8.12',   '105bc6d21cc2e9b6aff901e43c53afea')
       version('2.8.11.2', '6f5d7b8e7534a5d9e1a7664ba63cf882')

       def install(self, spec, prefix):
           # FIXME: Modify the configure line to suit your build system here.
           configure("--prefix=" + prefix)

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

will open ``$SPACK_ROOT/var/spack/packages/libelf/package.py`` in
``$EDITOR``.  If you try to edit a package that doesn't exist, Spack
will recommend using ``spack create``:

.. code-block:: sh

   $ spack edit foo
   ==> Error: No package 'foo'.  Use spack create, or supply -f/--force to edit a new file.

And, finally, if you *really* want to skip all the automatic stuff
that ``spack create`` does for you, then you can run ``spack edit
-f/--force``:

   $ spack edit -f foo

Which will generate a minimal package structure for you to fill in:

.. code-block:: python
   :linenos:

   from spack import *

   class Foo(Package):
       """Description"""

       homepage = "http://www.example.com"
       url      = "http://www.example.com/foo-1.0.tar.gz"

       version('1.0', '0123456789abcdef0123456789abcdef')

       def install(self, spec, prefix):
           configure("--prefix=" + prefix)
           make()
           make("install")

This is useful when, e.g., Spack cannot figure out the name and
version of your package from the archive URL.


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
       version('0.8.13', '4136d7b4c04df68b686570afa26988ac')
       version('0.8.12', 'e21f8273d9f5f6d43a59878dc274fec7')
       version('0.8.11', 'e931910b6d100f6caa32239849947fbf')
       version('0.8.10', '9db4d36c283d9790d8fa7df1f4d7b4d9')

You should be able to add these checksums directly to the versions
field in your package.

Note that for ``spack checksum`` to work, Spack needs to be able to
``import`` your pacakge in Python.  That means it can't have any
syntax errors, or the ``import`` will fail.  Use this once you've got
your package in working order.


Optional Package Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to ``homepage``, ``url``, and ``versions``, there are some
other useful attributes you can add to your package file.

``list_url``
^^^^^^^^^^^^^^^^^^

When spack tries to find available versions of packages (e.g. in
``spack checksum``), by default it looks in the parent directory of
the tarball in the package's ``url``.  For example, for libelf, the
url is:

.. literalinclude::  ../../../var/spack/packages/libelf/package.py
   :start-after: homepage
   :end-before: versions

Spack will try to fetch the URL ``http://www.mr511.de/software/``,
scrape the page, and use any links that look like the tarball URL to
find other available versions.  For many packages, the tarball's
parent directory may be unlistable, or it may not contain any links to
source code archives.  For these, you can specify a separate
``list_url`` indicating the page to search for tarballs.  For example,
``libdwarf`` has the homepage as the ``list_url``:

.. literalinclude::  ../../../var/spack/packages/libdwarf/package.py
   :start-after: Libdwarf
   :end-before: versions

``list_depth``
^^^^^^^^^^^^^^^^^^^^

Some packages may not have a listing of available verisons on a single
page.  For these, you can specify a ``list_depth`` indicating that
Spack should follow links from the ``list_url`` up to a particular
depth.  Spack will follow links and search each page reachable from
the ``list_url`` for tarball links.  For example, ``mpich`` archives
are stored in a directory tree of versions, so the package looks like
this:

.. literalinclude::  ../../../var/spack/packages/mpich/package.py
   :start-after: homepage
   :end-before: versions


.. _dependencies:

Dependencies
------------------------------

We've now covered how to build a simple package, but what if one
package relies on another package to build?  How do you express that
in a package file?  And how do you refer to the other package in the
build script for your own package?

Spack makes this relatively easy.  Let's take a look at the
``libdwarf`` package to see how it's done:

.. literalinclude:: ../../../var/spack/packages/libdwarf/package.py
   :linenos:
   :start-after: dwarf_dirs
   :end-before: def clean
   :emphasize-lines: 10
   :append: ...

``depends_on``
~~~~~~~~~~~~~~~~~~~~~

The ``depends_on('libelf')`` call on line 10 tells Spack that it needs
to build and install the ``libelf`` package before it builds
``libdwarf``.  This means that in your ``install()`` method, you are
guaranteed that ``libelf`` has been built and installed successfully,
so you can rely on it for your libdwarf build.

Dependency specs
~~~~~~~~~~~~~~~~~~~~~~

``depends_on`` doesn't just take the name of another package.  It
actually takes a full spec.  This means that you can restrict the
versions or other configuration options of ``libelf`` that
``libdwarf`` will build with.  Here's an example.  Suppose that in the
``libdwarf`` package you wrote:

.. code-block:: python

   depends_on("libelf@0.8:")

Now ``libdwarf`` will only ever build with ``libelf`` version ``0.8``
or higher.  If some versions of ``libelf`` are installed but they are
all older than this, then Spack will build a new version of ``libelf``
that satisfies the spec's version constraint, and it will build
``libdwarf`` with that one.  You could just as easily provide a
version range (e.g., ``0.8.2:0.8.4``) or a variant constraint
(e.g.. ``+debug``) to control how dependencies should be built.

Note that both users and package authors can use the same spec syntax
to refer to different package configurations.  Users use the spec
syntax on the command line to find installed packages or to install
packages with particular constraints, and package authors can use it
to describe relationships between packages.

.. _virtual-dependencies:

Virtual dependencies
-----------------------------

In some cases, more than one package can satisfy another package's
dependency.  One way this can happen is if a pacakge depends on a
particular *interface*, but there are multiple *implementations* of
the interface, and the package could be built with either.  A *very*
common interface in HPC is the `Message Passing Interface (MPI)
<http://www.mcs.anl.gov/research/projects/mpi/>`_, which is used in
many large-scale parallel applications.

MPI has several different implementations (e.g., `MPICH
<http://www.mpich.org>`_, `OpenMPI <http://www.open-mpi.org>`_, and
`MVAPICH <http://mvapich.cse.ohio-state.edu>`_) and scientific
applicaitons can be built with any one of these.  Complicating
matters, MPI does not have a standardized ABI, so a package built with
one implementation cannot be relinked with another implementation.
Many pacakage managers handle interfaces like this by requiring many
similar pacakge files, e.g., ``foo``, ``foo-mvapich``, ``foo-mpich``,
but Spack avoids this explosion of package files by providing support
for *virtual dependencies*.


``provides``
~~~~~~~~~~~~~~~~~~~~~

In Spack, ``mpi`` is a *virtual package*.  A package can depend on it
just like any other package, by supplying a ``depends_on`` call in the
package definition.  In ``mpileaks``, this looks like so:

.. literalinclude::  ../../../var/spack/packages/mpileaks/package.py
   :start-after: url
   :end-before: install

Here, ``callpath`` is an actual pacakge, but there is no package file
for ``mpi``, so we say it is a *virtual* package.  The syntax of
``depends_on``, however, is the same for both..  If we look inside the
package file of an MPI implementation, say MPICH, we'll see something
like this:

.. code-block:: python

   class Mpich(Package):
       provides('mpi')
       ...

The ``provides("mpi")`` call tells Spack that the ``mpich`` package
can be substituted whenever a package says it depends on ``mpi``.

Just as you can pass a spec to ``depends_on``, you can pass a spec to
``provides`` to add constraints.  This allows Spack to support the
notion of *versioned interfaces*.  The MPI standard has gone through
many revisions, each with new functions added.  Some packages may
require a recent implementation that supports MPI-3 fuctions, but some
MPI versions may only provide up to MPI-2.  You can indicate this by
adding a version constraint to the spec passed to ``provides``:

.. code-block:: python

   provides("mpi@:2")

Suppose that the above restriction is in the ``mpich2`` package.  This
says that ``mpich2`` provides MPI support *up to* version 2, but if a
package ``depends_on("mpi@3")``, then Spack will *not* build with ``mpich2``
for the MPI implementation.

``provides when``
~~~~~~~~~~~~~~~~~~~~~~~~~~

The same package may provide different versions of an interface
depending on *its* version.  Above, we simplified the ``provides``
call in ``mpich`` to make the explanation easier.  In reality, this is
how ``mpich`` declares the virtual packages it provides:

.. code-block:: python

   provides('mpi@:3', when='@3:')
   provides('mpi@:1', when='@1:')

The ``when`` argument to ``provides`` (a `keyword argument
<http://docs.python.org/2/tutorial/controlflow.html#keyword-arguments>`_
for those not familiar with Python) allows you to specify optional
constraints on the *calling* package.  The calling package will only
provide the declared virtual spec when *it* matches the constraints in
the when clause.  Here, when ``mpich`` is at version 3 or higher, it
provides MPI up to version 3.  When ``mpich`` is at version 1 or higher,
it provides the MPI virtual pacakge at version 1.

The ``when`` qualifier will ensure that Spack selects a suitably high
version of ``mpich`` to match another package that ``depends_on`` a
particular version of MPI.  It will also prevent a user from building
with too low a version of ``mpich``.  For example, suppose the package
``foo`` declares that it ``depends_on('mpi@2')``, and a user invokes
``spack install`` like this:

.. code-block:: sh

   $ spack install foo ^mpich@1.0

Spack will fail with a constraint violation, because the version of
MPICH requested is too low for the ``mpi`` requirement in ``foo``.


.. _abstract-and-concrete:

Abstract & concrete specs
------------------------------------------

Now that we've seen how spec constraints can be specified :ref:`on the
command line <sec-specs>` and within package definitions, we can talk
about how Spack puts all of this information together.  When you run
this:

.. code-block:: sh

   spack install mpileaks ^callpath@1.0+debug ^libelf@0.8.11

Spack parses the command line and builds a spec from the description.
The spec says that ``mpileaks`` should be built with the ``callpath``
library at 1.0 and with the debug option enabled, and with ``libelf``
version 0.8.11.  Spack will also look at the ``depends_on`` calls in
all of these packages, and it will build a spec from that.  The specs
from the command line and the specs built from package descriptions
are then combined, and the constraints are checked against each other
to make sure they're satisfiable.

What we have after this is done is called an *abstract spec*.  An
abstract spec is partially specified.  In other words, it could
describe more than one build of a package.  Spack does this to make
things easier on the user: they should only have to specify as much of
the package spec as they care about.  Here's an example partial spec
DAG, based on the constraints above::

   mpileaks
       ^callpath@1.0+debug
           ^dyninst
               ^libdwarf
                   ^libelf@0.8.11
           ^mpi

This diagram shows a spec DAG output as a tree, where successive
levels of indentation represent a depends-on relationship.  In the
above DAG, we can see some packages annotated with their constraints,
and some packages with no annotations at all.  When there are no
annotations, it means the user doesn't care what configuration of that
package is built, just so long as it works.

Concretization
~~~~~~~~~~~~~~~~~~~

An abstract spec is useful for the user, but you can't install an
abstract spec.  Spack has to take the abstract spec and "fill in" the
remaining unspecified parts in order to install.  This process is
called **concretization**.  Concretization happens in between the time
the user runs ``spack install`` and the time the ``install()`` method
is called.  The concretized version of the spec above might look like
this::

   mpileaks@2.3%gcc@4.7.3=macosx_10.8_x86_64
       ^callpath@1.0%gcc@4.7.3+debug=macosx_10.8_x86_64
           ^dyninst@8.1.2%gcc@4.7.3=macosx_10.8_x86_64
               ^libdwarf@20130729%gcc@4.7.3=macosx_10.8_x86_64
                   ^libelf@0.8.11%gcc@4.7.3=macosx_10.8_x86_64
           ^mpich@3.0.4%gcc@4.7.3=macosx_10.8_x86_64

Here, all versions, compilers, and platforms are filled in, and there
is a single version (no version ranges) for each package.  All
decisions about configuration have been made, and only after this
point will Spack call the ``install()`` method for your package.

Concretization in Spack is based on certain selection policies that
tell Spack how to select, e.g., a version, when one is not specified
explicitly.  Concretization policies are discussed in more detail in
:ref:`site-configuration`.  Sites using Spack can customize them to
match the preferences of their own users.


``spack spec``
~~~~~~~~~~~~~~~~~~~~

For an arbitrary spec, you can see the result of concretization by
running ``spack spec``.  For example:

.. code-block:: sh

   $ spack spec dyninst@8.0.1
   dyninst@8.0.1
       ^libdwarf
           ^libelf

   dyninst@8.0.1%gcc@4.7.3=macosx_10.8_x86_64
       ^libdwarf@20130729%gcc@4.7.3=macosx_10.8_x86_64
           ^libelf@0.8.13%gcc@4.7.3=macosx_10.8_x86_64


.. _install-environment:

Install environment
--------------------------

In general, you should not have to do much differently in your install
method than you would when installing a pacakge on the command line.
Spack tries to set environment variables and modify compiler calls so
that it *appears* to the build system that you're building with a
standard system install of everything.  Obviously that's not going to
cover *all* build systems, but it should make it easy to port packages
that use standard build systems to Spack.

There are a couple of things that Spack does that help with this:


Compiler interceptors
~~~~~~~~~~~~~~~~~~~~~~~~~

Spack intercepts the compiler calls that your build makes.  If your
build invokes ``cc``, then Spack intercepts the ``cc`` call with its
own wrapper script, and it inserts ``-I``, ``-L``, and ``-Wl,-rpath``
options for all dependencies before invoking the actual compiler.

An example of this would be the ``libdwarf`` build, which has one
dependency: ``libelf``.  Every call to ``cc`` in the ``libdwarf``
build will have ``-I$LIBELF_PREFIX/include``,
``-L$LIBELF_PREFIX/lib``, and ``-Wl,-rpath=$LIBELF_PREFIX/lib``
inserted on the command line.  This is done transparently to the
project's build system, which will just think it's using a system
where ``libelf`` is readily available.  Because of this, you **do
not** have to insert extra ``-I``, ``-L``, etc. on the command line.

An exmaple of this is the ``libdwarf`` package.  You'll notice that it
never mentions ``libelf`` outside of the ``depends_on('libelf')``
call, but it still manages to find its dependency library and build.
This is due to Spack's compiler interceptors.



Environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~

Spack sets a number of standard environment variables so that build
systems use its compiler wrappers for their builds.  The standard
enviroment variables are:

  =======================  =============================
    Variable                Purpose
  =======================  =============================
    ``CC``                  C compiler
    ``CXX``                 C++ compiler
    ``F77``                 Fortran 77 compiler
    ``FC``                  Fortran 90 and above compiler
    ``CMAKE_PREFIX_PATH``   Path to dependency prefixes for CMake
  =======================  =============================

All of these are standard variables respected by most build systems,
so if your project uses something like ``autotools`` or ``CMake``,
then it should pick them up automatically when you run ``configure``
or ``cmake`` in your ``install()`` function.  Many traditional builds
using GNU Make and BSD make also respect these variables, so they may
work with these systems, as well.

If your build systm does *not* pick these variables up from the
environment automatically, then you can simply pass them on the
command line or use a patch as part of your build process to get the
correct compilers into the project's build system.


Forked process
~~~~~~~~~~~~~~~~~~~~~

To give packages free reign over how they install things, how they
modify the environemnt, and how they use Spack's internal APIs, we
fork a new process each time we invoke ``install()``.  This allows
packages to have their own completely sandboxed build environment,
without impacting other jobs that the main Spack process runs.

.. _patching:

Patches
------------------------------------------

Depending on the host architecture, package version, known bugs, or
other issues, you may need to patch your software to get it to build
correctly.  Like many other package systems, spack allows you to store
patches alongside your package files and apply them to source code
after it's downloaded.

``patch``
~~~~~~~~~~~~~~~~~~~~~

You can specify patches in your package file with the ``patch()``
function.  ``patch`` looks like this:

.. code-block:: python

   class Mvapich2(Package):
       ...
       patch('ad_lustre_rwcontig_open_source.patch', when='@1.9:')

The first argument can be either a URL or a filename.  It specifies a
patch file that should be applied to your source.  If the patch you
supply is a filename, then the patch needs to live within the spack
source tree.  For example, the patch above lives in a directory
structure like this::

   $SPACK_ROOT/var/spack/packages/
       mvapich2/
           package.py
           ad_lustre_rwcontig_open_source.patch

If you supply a URL instead of a filename, the patch will be fetched
from the URL and then applied to your source code.

.. warning::

   It is generally better to use a filename rather than a URL for your
   patch.  Patches fetched from URLs are not currently checksummed,
   and adding checksums for them is tedious for the package builder.
   File patches go into the spack repository, which gives you git's
   integrity guarantees.  URL patches may be removed in a future spack
   version.

``patch`` can take two options keyword arguments.  They are:

``when``
  If supplied, this is a spec that tells spack when to apply
  the patch.  If the installed package spec matches this spec, the
  patch will be applied.  In our example above, the patch is applied
  when mvapich is at version ``1.9`` or higher.

``level``
  This tells spack how to run the ``patch`` command.  By default,
  the level is 1 and spack runs ``patch -p1``.  If level is 2,
  spack will run ``patch -p2``, and so on.

A lot of people are confused by level, so here's a primer.  If you
look in your patch file, you may see something like this:

.. code-block:: diff

   --- a/src/mpi/romio/adio/ad_lustre/ad_lustre_rwcontig.c 2013-12-10 12:05:44.806417000 -0800
   +++ b/src/mpi/romio/adio/ad_lustre/ad_lustre_rwcontig.c 2013-12-10 11:53:03.295622000 -0800
   @@ -8,7 +8,7 @@
     *   Copyright (C) 2008 Sun Microsystems, Lustre group
     */

   -#define _XOPEN_SOURCE 600
   +//#define _XOPEN_SOURCE 600
    #include <stdlib.h>
    #include <malloc.h>
    #include "ad_lustre.h"

The first two lines show paths with synthetic ``a/`` and ``b/``
prefixes.  These are placeholders for the two ``mvapich2`` source
directories that ``diff`` compared when it created the patch file.
This is git's default behavior when creating patch files, but other
programs may behave differently.

``-p1`` strips off the first level of the prefix in both paths,
allowing the patch to be applied from the root of an expanded mvapich2
archive.  If you set level to ``2``, it would strip off ``src``, and
so on.

It's generally easier to just structure your patch file so that it
applies cleanly with ``-p1``, but if you're using a URL to a patch you
didn't create yourself, ``level`` can be handy.


.. _install-method:

Implementing the ``install`` method
------------------------------------------

Now that the metadata is out of the way, we can move on to the
``install()`` method.  When a user runs ``spack install``, Spack
fetches an archive for the correct version of the software, expands
the archive, and sets the current working directory to the root
directory of the expanded archive.  It then instantiates a package
object and calls the ``install()`` method.

The ``install()`` signature looks like this:

.. code-block:: python

   class Foo(Package):
       def install(self, spec, prefix):
           ...

The parameters are as follows:

``self``
    For those not used to Python instance methods, this is the
    package itself.  In this case it's an instance of ``Foo``, which
    extends ``Package``.  For API docs on Package objects, see
    :py:class:`Package <spack.package.Package>`.

``spec``
    This is the concrete spec object created by Spack from an
    abstract spec supplied by the user.  It describes what should be
    installed.  It will be of type :py:class:`Spec <spack.spec.Spec>`.

``prefix``
    This is the path that your install method should copy build
    targets into.  It acts like a string, but it's actually its own
    special type, :py:class:`Prefix <spack.util.prefix.Prefix>`.

``spec`` and ``prefix`` are passed to ``install`` for convenience.
``spec`` is also available as an attribute on the package
(``self.spec``), and ``prefix`` is actually an attribute of ``spec``
(``spec.prefix``).

As mentioned in :ref:`install-environment`, you will usually not need
to refer to dependencies explicitly in your package file, as the
compiler wrappers take care of most of the heavy lifting here.  There
will be times, though, when you need to refer to the install locations
of dependencies, or when you need to do something different depending
on the version, compiler, dependencies, etc. that your package is
built with.  These parameters give you access to this type of
information.

.. _prefix-objects:

Prefix objects
----------------------

Spack passes the ``prefix`` parameter to the install method so that
you can pass it to ``configure``, ``cmake``, or some other installer,
e.g.:

.. code-block:: python

   configure('--prefix=' + prefix)


For the most part, prefix objects behave exactly like strings.  For
packages that do not have their own install target, or for those that
implement it poorly (like ``libdwarf``), you may need to manually copy
things into particular directories under the prefix.  For this, you
can refer to standard subdirectories without having to construct paths
yourself, e.g.:

.. code-block:: python

   def install(self, spec, prefix):
       mkdirp(prefix.bin)
       install('foo-tool', prefix.bin)

       mkdirp(prefix.include)
       install('foo.h', prefix.include)

       mkdirp(prefix.lib)
       install('libfoo.a', prefix.lib)


Most of the standard UNIX directory names are attributes on the
``prefix`` object.  See :py:class:`spack.prefix.Prefix` for a full
list.


.. _spec-objects:

Spec objects
-------------------------

When ``install`` is called, most parts of the build process are set up
for you.  The correct version's tarball has been downloaded and
expanded.  Environment variables like ``CC`` and ``CXX`` are set to
point to the correct compiler and version.  An install prefix has
already been selected and passed in as ``prefix``.  In most cases this
is all you need to get ``configure``, ``cmake``, or another install
working correctly.

There will be times when you need to know more about the build
configuration.  For example, some software requires that you pass
special parameters to ``configure``, like
``--with-libelf=/path/to/libelf`` or ``--with-mpich``.  You might also
need to supply special compiler flags depending on the compiler.  All
of this information is available in the spec.

Testing spec constraints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can test whether your spec is configured a certain way by using
the ``satisfies`` method.  For example, if you want to check whether
the package's version is in a particular range, you can use specs to
do that, e.g.:

.. code-block:: python

   if spec.satisfies('@1.2:1.4'):
       configure_args.append("CXXFLAGS='-DWITH_FEATURE'")
   configure('--prefix=' + prefix, *configure_args)

This works for compilers, too:

.. code-block:: python

   if spec.satisfies('%gcc'):
       configure_args.append('CXXFLAGS="-g3 -O3"')
   if spec.satisfies('%intel'):
       configure_args.append('CXXFLAGS="-xSSE2 -fast"')

Or for combinations of spec constraints:

.. code-block:: python

   if spec.satisfies('@1.2%intel'):
       tty.error("Version 1.2 breaks when using Intel compiler!")

You can also do similar satisfaction tests for dependencies:

.. code-block:: python

   if spec.satisfies('^dyninst@8.0'):
       configure_args.append('CXXFLAGS=-DSPECIAL_DYNINST_FEATURE')

This could allow you to easily work around a bug in a particular
dependency version.

You can use ``satisfies()`` to test for particular dependencies,
e.g. ``foo.satisfies('^openmpi@1.2')`` or ``foo.satisfies('^mpich')``,
or you can use Python's builtin ``in`` operator:

.. code-block:: python

   if 'libelf' in spec:
       print "this package depends on libelf"

This is useful for virtual dependencies, as you can easily see what
implementation was selected for this build:

.. code-block:: python

   if 'openmpi' in spec:
       configure_args.append('--with-openmpi')
   elif 'mpich' in spec:
       configure_args.append('--with-mpich')
   elif 'mvapich' in spec:
       configure_args.append('--with-mvapich')

It's also a bit more concise than satisfies.  The difference between
the two functions is that ``satisfies()`` tests whether spec
constraints overlap at all, while ``in`` tests whether a spec or any
of its dependencies satisfy the provided spec.


Accessing Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

You may need to get at some file or binary that's in the prefix of one
of your dependencies.  You can do that by subscripting the spec:

.. code-block:: python

   my_mpi = spec['mpich']

The value in the brackets needs to be some package name, and spec
needs to depend on that package, or the operation will fail.  For
example, the above code will fail if the ``spec`` doesn't depend on
``mpich``.  The value returned and assigned to ``my_mpi``, is itself
just another ``Spec`` object, so you can do all the same things you
would do with the package's own spec:

.. code-block:: python

   mpicc = new_path(my_mpi.prefix.bin, 'mpicc')

.. _multimethods:

Multimethods and ``@when``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Spack allows you to make multiple versions of instance functions in
packages, based on whether the package's spec satisfies particular
criteria.

The ``@when`` annotation lets packages declare multiple versions of
methods like install() that depend on the package's spec.  For
example:

.. code-block:: python

   class SomePackage(Package):
       ...

       def install(self, prefix):
           # Do default install

       @when('=chaos_5_x86_64_ib')
       def install(self, prefix):
           # This will be executed instead of the default install if
           # the package's sys_type() is chaos_5_x86_64_ib.

       @when('=bgqos_0")
       def install(self, prefix):
           # This will be executed if the package's sys_type is bgqos_0

In the above code there are three versions of install(), two of which
are specialized for particular platforms.  The version that is called
depends on the architecture of the package spec.

Note that this works for methods other than install, as well.  So,
if you only have part of the install that is platform specific, you
could do something more like this:

.. code-block:: python

   class SomePackage(Package):
      ...
       # virtual dependence on MPI.
       # could resolve to mpich, mpich2, OpenMPI
       depends_on('mpi')

       def setup(self):
           # do nothing in the default case
           pass

       @when('^openmpi')
       def setup(self):
           # do something special when this is built with OpenMPI for
           # its MPI implementations.

       def install(self, prefix):
           # Do common install stuff
           self.setup()
           # Do more common install stuff

You can write multiple ``@when`` specs that satisfy the package's spec,
for example:

.. code-block:: python

   class SomePackage(Package):
       ...
       depends_on('mpi')

       def setup_mpi(self):
           # the default, called when no @when specs match
           pass

       @when('^mpi@3:')
       def setup_mpi(self):
           # this will be called when mpi is version 3 or higher
           pass

       @when('^mpi@2:')
       def setup_mpi(self):
           # this will be called when mpi is version 2 or higher
           pass

       @when('^mpi@1:')
       def setup_mpi(self):
           # this will be called when mpi is version 1 or higher
           pass

In situations like this, the first matching spec, in declaration order
will be called.  As before, if no ``@when`` spec matches, the default
method (the one without the ``@when`` decorator) will be called.

.. warning::

   The default version of decorated methods must **always** come
   first.  Otherwise it will override all of the platform-specific
   versions.  There's not much we can do to get around this because of
   the way decorators work.



.. _shell-wrappers:

Shell command wrappers
-------------------------

Recall the install method from ``libelf``:

.. code-block:: python

   def install(self, spec, prefix):
       configure("--prefix=" + prefix,
                 "--enable-shared",
                 "--disable-dependency-tracking",
                 "--disable-debug")
       make()

       # The mkdir commands in libelf's install can fail in parallel
       make("install", parallel=False)

Normally in Python, you'd have to write something like this in order
to execute shell commands:

.. code-block:: python

   import subprocess
   subprocess.check_call('configure', '--prefix=' + prefix)

We've tried to make this a bit easier by providing callable wrapper
objects for some shell commands.  By default, ``configure``,
``cmake``, and ``make`` wrappers are are provided, so you can call
them more naturally in your package files.

If you need other commands, you can use ``which`` to get them:

.. code-block:: python

   sed = which('sed')
   sed('s/foo/bar/', filename)

The ``which`` function will search the ``PATH`` for the application.

Callable wrappers also allow spack to provide some special features.
For example, in Spack, ``make`` is parallel by default, and Spack
figures out the number of cores on your machine and passes an
appropriate value for ``-j<numjobs>`` when it calls ``make`` (see the
``parallel`` package attribute under :ref:`metadata <metadata>`).  In
a package file, you can supply a keyword argument, ``parallel=False``,
to the ``make`` wrapper to disable parallel make.  In the ``libelf``
package, this allows us to avoid race conditions in the library's
build system.

.. _pacakge-lifecycle:

The package build process
---------------------------------

When you are building packages, you will likely not get things
completely right the first time.

The ``spack install`` command performs a number of tasks before it
finally installs each package.  It downloads an archive, expands it in
a temporary directory, and only then gives control to the package's
``install()`` method.  If the build doesn't go as planned, you may
want to clean up the temporary directory, or if the package isn't
downloading properly, you might want to run *only* the ``fetch`` stage
of the build.

A typical package development cycle might look like this:

.. code-block:: sh

   $ spack edit mypackage
   $ spack install mypackage
   ... build breaks! ...
   $ spack clean mypackage
   $ spack edit mypackage
   $ spack install mypackage
   ... repeat clean/install until install works ...

Below are some commands that will allow you some finer-grained
controll over the install process.

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

``spack patch``
~~~~~~~~~~~~~~~~~

After staging, Spack applies patches to downloaded packages, if any
have been specified in the package file.  This command will run the
install process through the fetch, stage, and patch phases.  Spack
keeps track of whether patches have already been applied and skips
this step if they have been.  If Spack discovers that patches didn't
apply cleanly on some previous run, then it will restage the entire
package before patching.


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
