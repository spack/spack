.. _packaging-guide:

Packaging Guide
=====================

This guide is intended for developers or administrators who want to
package software so that Spack can install it.  It assumes that you
have at least some familiarty with Python, and that you've read the
:ref:`basic usage guide <basic-usage>`, especially the part about
:ref:`specs <sec-specs>`.

There are two key parts of Spack:

   #. **Specs**: expressions for describing builds of software, and
   #. **Packages**: Python modules that describe how to build
      software according to a spec.

Specs allow a user to describe a *particular* build in a way that a
package author can understand.  Packages allow a developer to
encapsulate the logic build logic for different versions, compilers,
options, platforms, and dependency combinations in one place.

Packages in Spack are written in pure Python, so you can do anything
in Spack that you can do in Python.  Python was chosen as the
implementation language for two reasons.  First, Python is becoming
ubiquitous in the HPC community due to its use in numerical codes.
Second, it's a modern language and has many powerful features to help
make package writing easy.

Creating & Editing Packages
----------------------------------

.. _spack-create:

``spack create``
~~~~~~~~~~~~~~~~~~~~~

The ``spack create`` command generates boilerplate package template
from a URL pointing to a tarball or other software archive.  In most
cases, you'll only need to run this once, then slightly modify the
boilerplate to get your package working.

All you need is the URL to a tarball (other archive formats are ok
too) you want to package:

.. code-block:: sh

   $ spack create http://www.cmake.org/files/v2.8/cmake-2.8.12.1.tar.gz

When you run this, Spack looks at the tarball URL and tries to figure
out the name of the package to be created. It also tries to determine
out what version strings look like for this package. Using this
information, it tries to find *additional* versions by spidering the
package's webpage.  If it finds multiple versions, Spack prompts you
to tell it how many versions you want to download and checksum.

.. code-block:: sh

   $ spack create http://www.cmake.org/files/v2.8/cmake-2.8.12.1.tar.gz
   ==> This looks like a URL for cmake version 2.8.12.1.
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
wanting more.  Let's say you choose to download 3 tarballs:

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

       # FIXME: Add dependencies if this package requires them.
       # depends_on("foo")

       def install(self, spec, prefix):
           # FIXME: Modify the configure line to suit your build system here.
           configure("--prefix=" + prefix)

           # FIXME: Add logic to build and install here
           make()
           make("install")

The tedious stuff (creating the class, checksumming archives) has been
done for you.

.. note::

   If ``spack create`` fails to download or to detect the package
   version, you can use ``spack edit -f`` to generate simpler
   boilerplate.  See the next section for more on this.

In the generated package, the download ``url`` attribute is already
set.  All the things you still need to change are marked with
``FIXME`` labels.  The first ``FIXME`` refers to the commented
instructions at the top of the file.  You can delete these
instructions after reading them.  The rest of them are as follows:

   #. Add a description.

      Immediately inside the package class is a *docstring* in
      triple-quotes (``"""``).  It's used to generate the description
      shown when users run ``spack info``.

   #. Change the ``homepage`` to a useful URL.

      The ``homepage`` is displayed when users run ``spack info`` so
      that they can learn about packages.

   #. Add ``depends_on()`` calls for the package's dependencies.

      ``depends_on`` tells Spack that other packages need to be built
      and installed before this one.  See `dependencies_`.

   #. Get the ``install()`` method working.

      The ``install()`` method implements the logic to build a
      package.  The code should look familiar; it is designed to look
      like a shell script. Specifics will differ depending on the package,
      and :ref:`implementing the install method <install-method>` is
      covered in detail later.

Before going into details, we'll cover a few more basics.

.. _spack-edit:

``spack edit``
~~~~~~~~~~~~~~~~~~~~

One of the easiest ways to learn to write packages is to look at
existing ones.  You can edit a package file by name with the ``spack
edit`` command:

.. code-block:: sh

   spack edit cmake

So, if you used ``spack create`` to create a package, then saved and
closed the resulting file, you can get back to it with ``spack edit``.
The ``cmake`` package actually lives in
``$SPACK_ROOT/var/spack/packages/cmake/package.py``, but this provides
a much simpler shortcut and saves you the trouble of typing the full
path.


``spack edit -f``
~~~~~~~~~~~~~~~~~~~~
If you try to edit a package that doesn't exist, Spack will recommend
using ``spack create``:

.. code-block:: sh

   $ spack edit foo
   ==> Error: No package 'foo'.  Use spack create, or supply -f/--force to edit a new file.

As the output advises, You can use ``spack edit -f/--force`` to force
the creation of a new, *very* simple boilerplate package:

.. code-block:: sh

   $ spack edit -f foo

Unlike ``spack create``, which tries to infer names and versions, and
which actually downloads the tarball and checksums it for you, ``spack
edit -f`` will substitute dummy values for you to fill in yourself:

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

This is useful when ``spack create`` cannot figure out the name and
version of your package from the archive URL.


Naming & Directory Structure
--------------------------------------

This section describes how packages need to be named, and where they
live in Spack's directory structure.  In general, `spack-create`_ and
`spack-edit`_ handle creating package files for you, so you can skip
most of the details here.

``var/spack/packages``
~~~~~~~~~~~~~~~~~~~~~~~

A Spack installation directory is structured like a standard UNIX
install prefix (``bin``, ``lib``, ``include``, ``var``, ``opt``,
etc.).  Most of the code for Spack lives in ``$SPACK_ROOT/lib/spack``.
Packages themselves live in ``$SPACK_ROOT/var/spack/packages``.

If you ``cd`` to that directory, you will see directories for each
package:

.. command-output::  cd $SPACK_ROOT/var/spack/packages;  ls -CF
   :shell:

Each directory contains a file called ``package.py``, which is where
all the python code for the package goes.  For example, the ``libelf``
package lives in::

   $SPACK_ROOT/var/spack/packages/libelf/package.py

Alongside the ``package.py`` file, a package may contain extra
directories or files (like patches) that it needs to build.


Package Names
~~~~~~~~~~~~~~~~~~

Packages are named after the directory containing ``package.py``.  So,
``libelf``'s ``package.py`` lives in a directory called ``libelf``.
The ``package.py`` file contains a class called ``Libelf``, which
extends Spack's ``Package`` class.  This is what makes it a Spack
package:

``var/spack/packages/libelf/package.py``

.. code-block:: python
   :linenos:

   from spack import *

   class Libelf(Package):
       """ ... description ... """
       homepage = ...
       url = ...
       version(...)
       depends_on(...)

       def install():
           ...

The **directory name** (``libelf``) is what users need to provide on
the command line. e.g., if you type any of these:

.. code-block:: sh

   $ spack install libelf
   $ spack install libelf@0.8.13

Spack sees the package name in the spec and looks for
``libelf/package.py`` in ``var/spack/packages``.  Likewise, if you say
``spack install docbook-xml``, then Spack looks for
``docbook-xml/package.py``.

Spack uses the directory name as the package name in order to give
packagers more freedom in naming their packages.  Package names can
contain letters, numbers, dashes, and underscores.  Using a Python
identifier (e.g., a class name or a module name) would make it
difficult to support these options.  So, you can name a package
``3proxy`` or ``_foo`` and Spack won't care.  It just needs to see
that name in the package spec.

Package class names
~~~~~~~~~~~~~~~~~~~~~~~

Spack loads ``package.py`` files dynamically, and it needs to find a
special class name in the file for the load to succeed.  The **class
name** (``Libelf`` in our example) is formed by converting words
separated by `-` or ``_`` in the file name to camel case.  If the name
starts with a number, we prefix the class name with ``_``. Here are
some examples:

=================  =================
 Module Name         Class Name
=================  =================
 ``foo_bar``         ``FooBar``
 ``docbook-xml``     ``DocbookXml``
 ``FooBar``          ``Foobar``
 ``3proxy``          ``_3proxy``
=================  =================

In general, you won't have to remember this naming convention because
`spack-create`_ and `spack-edit`_ will generate boilerplate for you,
and you can just fill in the blanks.


Adding new versions
------------------------

The most straightforward way to add new versions to your package is to
add a line like this in the package class:

.. code-block:: python
   :linenos:

   class Foo(Package):
       url = 'http://example.com/foo-1.0.tar.gz'
       version('8.2.1', '4136d7b4c04df68b686570afa26988ac')
       ...

Version URLs
~~~~~~~~~~~~~~~~~

By default, each version's URL is extrapolated from the ``url`` field
in the package.  For example, Spack is smart enough to download
version ``8.2.1.`` of the ``Foo`` package above from
``http://example.com/foo-8.2.1.tar.gz``.

If spack *cannot* extrapolate the URL from the ``url`` field, or if
the package doesn't have a ``url`` field, you can add a URL explicitly
for a particular version:

.. code-block:: python

   version('8.2.1', '4136d7b4c04df68b686570afa26988ac',
           url='http://example.com/foo-8.2.1-special-version.tar.gz')

For the URL above, you might have to add an explicit URL because the
version can't simply be substituted in the original ``url`` to
construct the new one for ``8.2.1``.

Wehn you supply a custom URL for a version, Spack uses that URL
*verbatim* when fetching the version, and will *not* perform
extrapolation.

Checksums
~~~~~~~~~~~~~~~~~

Spack uses a checksum to ensure that the downloaded package version is
not corrupted or compromised.  This is especially important when
fetching from insecure sources, like unencrypted http.  By default, a
package will *not* be installed if it doesn't pass a checksum test
(though users can overried this with ``spack install --no-checksum``).

Spack can currently support checksums using the MD5, SHA-1, SHA-224,
SHA-256, SHA-384, and SHA-512 algorithms.

``spack md5``
^^^^^^^^^^^^^^^^^^^^^^

If you have a single file to checksum, you can use the ``spack md5``
command to do it.  Here's how you might download an archive and get a
checksum for it:

.. code-block:: sh

   $ curl -O http://exmaple.com/foo-8.2.1.tar.gz'
   $ spack md5 foo-8.2.1.tar.gz
   4136d7b4c04df68b686570afa26988ac  foo-8.2.1.tar.gz

Doing this for lots of files, or whenever a new package version is
released, is tedious.  See ``spack checksum`` below for an automated
version of this process.

.. _spack-checksum:

``spack checksum``
^^^^^^^^^^^^^^^^^^^^^^

If you want to add new versions to a package you've already created,
this is automated with the ``spack checksum`` command.  Here's an
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

This does the same thing that ``spack create`` does, but it allows you
to go back and add new vesrions easily as you need them (e.g., as
they're released).  It fetches the tarballs you ask for and prints out
a list of ``version`` commands ready to copy/paste into your package
file:

.. code-block:: sh

   ==> Checksummed new versions of libelf:
       version('0.8.13', '4136d7b4c04df68b686570afa26988ac')
       version('0.8.12', 'e21f8273d9f5f6d43a59878dc274fec7')
       version('0.8.11', 'e931910b6d100f6caa32239849947fbf')
       version('0.8.10', '9db4d36c283d9790d8fa7df1f4d7b4d9')

By default, Spack will search for new tarball downloads by scraping
the parent directory of the tarball you gave it.  So, if your tarball
is at ``http://example.com/downloads/foo-1.0.tar.gz``, Spack will look
in ``http://example.com/downloads/`` for links to additional versions.
If you need to search another path for download links, see the
reference documentation on `attribute_list_url`_ and
`attributee_list_depth`_.

.. note::

  * This command assumes that Spack can extrapolate new URLs from an
    existing URL in the package, and that Spack can find similar URLs
    on a webpage.  If that's not possible, you'll need to manually add
    ``version`` calls yourself.

  * For ``spack checksum`` to work, Spack needs to be able to
    ``import`` your pacakge in Python.  That means it can't have any
    syntax errors, or the ``import`` will fail.  Use this once you've
    got your package in working order.


.. _vcs-fetch:

Fetching from VCS Repositories
--------------------------------------

For some packages, source code is hosted in a Version Control System
(VCS) repository rather than as a tarball.  Packages can be set up to
fetch from a repository instead of a tarball. Currently, Spack
supports fetching with `Git <git-fetch_>`_, `Mercurial (hg)
<hg-fetch_>`_, and `Subversion (SVN) <svn-fetch_>`_.

To fetch a package from a source repository, you add a ``version()``
call to your package with parameters indicating the repository URL and
any branch, tag, or revision to fetch.  See below for the paramters
you'll need for each VCS system.

Repositories and versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The package author is responsible for coming up with a sensible name
for each version.  For example, if you're fetching from a tag like
``v1.0``, you might call that ``1.0``.  If you're fetching a nameless
git commit or an older subversion revision, you might give the commit
an intuitive name, like ``dev`` for a development version, or
``some-fancy-new-feature`` if you want to be more specific.

In general, it's recommended to fetch tags or particular
commits/revisions, NOT branches or the repository mainline, as
branches move forward over time and you aren't guaranteed to get the
same thing every time you fetch a particular version.  Life isn't
simple, though, so this is not strictly enforced.

In some future release, Spack may support extrapolating repository
versions as it does for tarball URLs, but currently this is not
supported.

.. _git-fetch:

Git
~~~~~~~~~~~~~~~~~~~~

Git fetching is enabled with the following parameters to ``version``:

  * ``git``: URL of the git repository.
  * ``tag``: name of a tag to fetch.
  * ``branch``: name of a branch to fetch.
  * ``commit``: SHA hash (or prefix) of a commit to fetch.

Only one of ``tag``, ``branch``, or ``commit`` can be used at a time.

Default branch
  To fetch a repository's default branch:

  .. code-block:: python

     class Example(Package):
         ...
         version('dev', git='https://github.com/example-project/example.git')

  This is not recommended, as the contents of the default branch
  change over time.

Tags
  To fetch from a particular tag, use the ``tag`` parameter along with
  ``git``:

  .. code-block:: python

     version('1.0.1', git='https://github.com/example-project/example.git',
             tag='v1.0.1')

Branches
  To fetch a particular branch, use ``branch`` instead:

  .. code-block:: python

     version('experimental', git='https://github.com/example-project/example.git',
             branch='experimental')

  This is not recommended, as the contents of branches change over
  time.

Commits
  Finally, to fetch a particular commit, use ``commit``:

  .. code-block:: python

     version('2014-10-08', git='https://github.com/example-project/example.git',
             commit='9d38cd4e2c94c3cea97d0e2924814acc')

  This doesn't have to be a full hash; You can abbreviate it as you'd
  expect with git:

  .. code-block:: python

     version('2014-10-08', git='https://github.com/example-project/example.git',
             commit='9d38cd')

  It may be useful to provide a saner version for commits like this,
  e.g. you might use the date as the version, as done above.  Or you
  could just use the abbreviated commit hash.  It's up to the package
  author to decide what makes the most sense.

Installing
^^^^^^^^^^^^^^

You can fetch and install any of the versions above as you'd expect,
by using ``@<version>`` in a spec:

.. code-block:: sh

   spack install example@2014-10-08

Git and other VCS versions will show up in the list of versions when
a user runs ``spack info <package name>``.


.. _hg-fetch:

Mercurial
~~~~~~~~~~~~~~~~~~~~~~~~~

Fetching with mercurial works much like `git <git-fetch>`_, but you
use the ``hg`` parameter.

Default
  Add the ``hg`` parameter with no ``revision``:

  .. code-block:: python

     version('hg-head', hg='https://jay.grs.rwth-aachen.de/hg/example')

  Note that this is not recommended; try to fetch a particular
  revision instead.

Revisions
  Add ``hg`` and ``revision``parameters:

  .. code-block:: python

     version('1.0', hg='https://jay.grs.rwth-aachen.de/hg/example',
             revision='v1.0')

  Unlike ``git``, which has special parameters for different types of
  revisions, you can use ``revision`` for branches, tags, and commits
  when you fetch with Mercurial.

As wtih git, you can fetch these versions using the ``spack install
example@<version>`` command-line syntax.

.. _svn-fetch:

Subversion
~~~~~~~~~~~~~~~~~~~~~~~~~~

To fetch with subversion, use the ``svn`` and ``revision`` parameters:

Head
  Simply add an ``svn`` parameter to ``version``:

  .. code-block:: python

     version('svn-head', svn='https://outreach.scidac.gov/svn/libmonitor/trunk')

  This is not recommended, as the head will move forward over time.

Revisions
  To fetch a particular revision, add a ``revision`` to the
  version call:

  .. code-block:: python

     version('svn-head', svn='https://outreach.scidac.gov/svn/libmonitor/trunk',
             revision=128)

Subversion branches are handled as part of the directory structure, so
you can check out a branch or tag by changing the ``url``.

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
     :linenos:

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

  Lines 1-2 show paths with synthetic ``a/`` and ``b/`` prefixes.  These
  are placeholders for the two ``mvapich2`` source directories that
  ``diff`` compared when it created the patch file.  This is git's
  default behavior when creating patch files, but other programs may
  behave differently.

  ``-p1`` strips off the first level of the prefix in both paths,
  allowing the patch to be applied from the root of an expanded mvapich2
  archive.  If you set level to ``2``, it would strip off ``src``, and
  so on.

  It's generally easier to just structure your patch file so that it
  applies cleanly with ``-p1``, but if you're using a patch you didn't
  create yourself, ``level`` can be handy.


Finding Package Downloads
----------------------------

We've already seen the ``homepage`` and ``url`` package attributes:

.. code-block:: python
   :linenos:

   from spack import *

   class Mpich(Package):
      """MPICH is a high performance and widely portable implementation of
         the Message Passing Interface (MPI) standard."""
      homepage = "http://www.mpich.org"
      url      = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"

These are class-level attributes used by Spack to show users
information about the package, and to determine where to download its
source code.

Spack uses the tarball URL to extrapolate where to find other tarballs
of the same package (e.g. in `spack checksum <spack-checksum_>`_, but
this does not always work.  This section covers ways you can tell
Spack to find tarballs elsewhere.

.. _attribute_list_url:

``list_url``
~~~~~~~~~~~~~~~~~~~~~

When spack tries to find available versions of packages (e.g. with
`spack checksum <spack-checksum_>`_), it spiders the parent directory
of the tarball in the ``url`` attribute.  For example, for libelf, the
url is:

.. code-block:: python

   url = "http://www.mr511.de/software/libelf-0.8.13.tar.gz"

Spack spiders ``http://www.mr511.de/software/`` to find similar
tarball links and ultimately to make a list of available versions of
``libelf``.

For many packages, the tarball's parent directory may be unlistable,
or it may not contain any links to source code archives.  In fact,
many times additional package downloads aren't even available in the
same directory as the download URL.

For these, you can specify a separate ``list_url`` indicating the page
to search for tarballs.  For example, ``libdwarf`` has the homepage as
the ``list_url``, because that is where links to old versions are:

.. code-block:: python
   :linenos:

   class Libdwarf(Package):
       homepage = "http://www.prevanders.net/dwarf.html"
       url      = "http://www.prevanders.net/libdwarf-20130729.tar.gz"
       list_url = homepage

.. _attribute_list_depth:

``list_depth``
~~~~~~~~~~~~~~~~~~~~~

``libdwarf`` and many other packages have a listing of available
verisons on a single webpage, but not all do.  For example, ``mpich``
has a tarball URL that looks like this:

    url = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"

But its downloads are in many different subdirectories of
``http://www.mpich.org/static/downloads/``.  So, we need to add a
``list_url`` *and* a ``list_depth`` attribute:

.. code-block:: python
   :linenos:

   class Mpich(Package):
       homepage   = "http://www.mpich.org"
       url        = "http://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
       list_url   = "http://www.mpich.org/static/downloads/"
       list_depth = 2

By default, Spack only looks at the top-level page available at
``list_url``.  ``list_depth`` tells it to follow up to 2 levels of
links from the top-level page.  Note that here, this implies two
levels of subdirectories, as the ``mpich`` website is structured much
like a filesystem.  But ``list_depth`` really refers to link depth
when spidering the page.

.. _attribute_parallel:

Parallel Builds
------------------

By default, Spack will invoke ``make()`` with a ``-j <njobs>``
argument, so that builds run in parallel.  It figures out how many
jobs to run by determining how many cores are on the host machine.
Specifically, it uses the number of CPUs reported by Python's
`multiprocessing.cpu_count()
<http://docs.python.org/library/multiprocessing.html#multiprocessing.cpu_count>`_.

If a package does not build properly in parallel, you can override
this setting by adding ``parallel = False`` to your package.  For
example, OpenSSL's build does not work in parallel, so its package
looks like this:

.. code-block:: python
   :emphasize-lines: 8
   :linenos:

   class Openssl(Package):
       homepage = "http://www.openssl.org"
       url      = "http://www.openssl.org/source/openssl-1.0.1h.tar.gz"

       version('1.0.1h', '8d6d684a9430d5cc98a62a5d8fbda8cf')
       depends_on("zlib")

       parallel = False

Similarly, you can disable parallel builds only for specific make
commands, as ``libdwarf`` does:

.. code-block:: python
   :emphasize-lines: 9, 12
   :linenos:

   class Libelf(Package):
       ...

       def install(self, spec, prefix):
           configure("--prefix=" + prefix,
                     "--enable-shared",
                     "--disable-dependency-tracking",
                     "--disable-debug")
           make()

           # The mkdir commands in libelf's install can fail in parallel
           make("install", parallel=False)

The first make will run in parallel here, but the second will not.  If
you set ``parallel`` to ``False`` at the package level, then each call
to ``make()`` will be sequential by default, but packagers can call
``make(parallel=True)`` to override it.


.. _dependencies:

Dependencies
------------------------------

We've covered how to build a simple package, but what if one package
relies on another package to build?  How do you express that in a
package file?  And how do you refer to the other package in the build
script for your own package?

Spack makes this relatively easy.  Let's take a look at the
``libdwarf`` package to see how it's done:

.. code-block:: python
   :emphasize-lines: 9
   :linenos:

   class Libdwarf(Package):
       homepage = "http://www.prevanders.net/dwarf.html"
       url      = "http://www.prevanders.net/libdwarf-20130729.tar.gz"
       list_url = homepage

       version('20130729', '4cc5e48693f7b93b7aa0261e63c0e21d')
       ...

       depends_on("libelf")

       def install(self, spec, prefix):
           ...

``depends_on()``
~~~~~~~~~~~~~~~~~~~~~

The highlighted ``depends_on('libelf')`` call tells Spack that it
needs to build and install the ``libelf`` package before it builds
``libdwarf``.  This means that in your ``install()`` method, you are
guaranteed that ``libelf`` has been built and installed successfully,
so you can rely on it for your libdwarf build.

Dependency specs
~~~~~~~~~~~~~~~~~~~~~~

``depends_on`` doesn't just take the name of another package.  It
takes a full spec.  This means that you can restrict the versions or
other configuration options of ``libelf`` that ``libdwarf`` will build
with.  Here's an example.  Suppose that in the ``libdwarf`` package
you write:

.. code-block:: python

   depends_on("libelf@0.8:")

Now ``libdwarf`` will require a version of ``libelf`` version ``0.8``
or higher in order to build.  If some versions of ``libelf`` are
installed but they are all older than this, then Spack will build a
new version of ``libelf`` that satisfies the spec's version
constraint, and it will build ``libdwarf`` with that one.  You could
just as easily provide a version range:

.. code-block:: python

   depends_on("libelf@0.8.2:0.8.4:")

Or a requirement for a particular variant:

.. code-block:: python

   depends_on("libelf@0.8+debug")

Both users *and* package authors can use the same spec syntax to refer
to different package configurations.  Users use the spec syntax on the
command line to find installed packages or to install packages with
particular constraints, and package authors can use specs to describe
relationships between packages.

.. _virtual-dependencies:

Virtual dependencies
-----------------------------

In some cases, more than one package can satisfy another package's
dependency.  One way this can happen is if a pacakge depends on a
particular *interface*, but there are multiple *implementations* of
the interface, and the package could be built with any of them.  A
*very* common interface in HPC is the `Message Passing Interface (MPI)
<http://www.mcs.anl.gov/research/projects/mpi/>`_, which is used in
many large-scale parallel applications.

MPI has several different implementations (e.g., `MPICH
<http://www.mpich.org>`_, `OpenMPI <http://www.open-mpi.org>`_, and
`MVAPICH <http://mvapich.cse.ohio-state.edu>`_) and scientific
applications can be built with any one of them.  Complicating matters,
MPI does not have a standardized ABI, so a package built with one
implementation cannot simply be relinked with another implementation.
Many pacakage managers handle interfaces like this by requiring many
similar package files, e.g., ``foo``, ``foo-mvapich``, ``foo-mpich``,
but Spack avoids this explosion of package files by providing support
for *virtual dependencies*.

``provides``
~~~~~~~~~~~~~~~~~~~~~

In Spack, ``mpi`` is handled as a *virtual package*.  A package like
``mpileaks`` can depend on it just like any other package, by
supplying a ``depends_on`` call in the package definition.  For example:

.. code-block:: python
   :linenos:
   :emphasize-lines: 7

   class Mpileaks(Package):
       homepage = "https://github.com/hpc/mpileaks"
       url = "https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz"

       version('1.0', '8838c574b39202a57d7c2d68692718aa')

       depends_on("mpi")
       depends_on("adept-utils")
       depends_on("callpath")

Here, ``callpath`` and ``adept-utils`` are concrete pacakges, but
there is no actual package file for ``mpi``, so we say it is a
*virtual* package.  The syntax of ``depends_on``, is the same for
both.  If we look inside the package file of an MPI implementation,
say MPICH, we'll see something like this:

.. code-block:: python

   class Mpich(Package):
       provides('mpi')
       ...

The ``provides("mpi")`` call tells Spack that the ``mpich`` package
can be used to satisfy the dependency of any package that
``depends_on('mpi')``.

Versioned Interfaces
~~~~~~~~~~~~~~~~~~~~~~

Just as you can pass a spec to ``depends_on``, so can you pass a spec
to ``provides`` to add constraints.  This allows Spack to support the
notion of *versioned interfaces*.  The MPI standard has gone through
many revisions, each with new functions added, and each revision of
the standard has a version number.  Some packages may require a recent
implementation that supports MPI-3 fuctions, but some MPI versions may
only provide up to MPI-2.  Others may need MPI 2.1 or higher.  You can
indicate this by adding a version constraint to the spec passed to
``provides``:

.. code-block:: python

   provides("mpi@:2")

Suppose that the above ``provides`` call is in the ``mpich2`` package.
This says that ``mpich2`` provides MPI support *up to* version 2, but
if a package ``depends_on("mpi@3")``, then Spack will *not* build that
package with ``mpich2``.

``provides when``
~~~~~~~~~~~~~~~~~~~~~~~~~~

The same package may provide different versions of an interface
depending on *its* version.  Above, we simplified the ``provides``
call in ``mpich`` to make the explanation easier.  In reality, this is
how ``mpich`` calls ``provides``:

.. code-block:: python

   provides('mpi@:3', when='@3:')
   provides('mpi@:1', when='@1:')

The ``when`` argument to ``provides`` allows you to specify optional
constraints on the *providing* package, or the *provider*.  The
provider only provides the declared virtual spec when *it* matches
the constraints in the when clause.  Here, when ``mpich`` is at
version 3 or higher, it provides MPI up to version 3.  When ``mpich``
is at version 1 or higher, it provides the MPI virtual pacakge at
version 1.

The ``when`` qualifier ensures that Spack selects a suitably high
version of ``mpich`` to satisfy some other package that ``depends_on``
a particular version of MPI.  It will also prevent a user from
building with too low a version of ``mpich``.  For example, suppose
the package ``foo`` declares this:

.. code-block:: python

   class Foo(Package):
       ...
       depends_on('mpi@2')

Suppose a user invokes ``spack install`` like this:

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


.. graphviz::

   digraph {
       mpileaks -> mpi
       mpileaks -> "callpath@1.0+debug" -> mpi
       "callpath@1.0+debug" -> dyninst
       dyninst  -> libdwarf -> "libelf@0.8.11"
       dyninst  -> "libelf@0.8.11"
   }


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

   mpileaks@2.3%gcc@4.7.3=linux-ppc64
       ^callpath@1.0%gcc@4.7.3+debug=linux-ppc64
           ^dyninst@8.1.2%gcc@4.7.3=linux-ppc64
               ^libdwarf@20130729%gcc@4.7.3=linux-ppc64
                   ^libelf@0.8.11%gcc@4.7.3=linux-ppc64
           ^mpich@3.0.4%gcc@4.7.3=linux-ppc64

.. graphviz::

   digraph {
       "mpileaks@2.3\n%gcc@4.7.3\n=linux-ppc64" -> "mpich@3.0.4\n%gcc@4.7.3\n=linux-ppc64"
       "mpileaks@2.3\n%gcc@4.7.3\n=linux-ppc64" -> "callpath@1.0\n%gcc@4.7.3+debug\n=linux-ppc64" -> "mpich@3.0.4\n%gcc@4.7.3\n=linux-ppc64"
       "callpath@1.0\n%gcc@4.7.3+debug\n=linux-ppc64" -> "dyninst@8.1.2\n%gcc@4.7.3\n=linux-ppc64"
       "dyninst@8.1.2\n%gcc@4.7.3\n=linux-ppc64" -> "libdwarf@20130729\n%gcc@4.7.3\n=linux-ppc64" -> "libelf@0.8.11\n%gcc@4.7.3\n=linux-ppc64"
       "dyninst@8.1.2\n%gcc@4.7.3\n=linux-ppc64" -> "libelf@0.8.11\n%gcc@4.7.3\n=linux-ppc64"
   }

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

   dyninst@8.0.1%gcc@4.7.3=linux-ppc64
       ^libdwarf@20130729%gcc@4.7.3=linux-ppc64
           ^libelf@0.8.13%gcc@4.7.3=linux-ppc64

This is useful when you want to know exactly what Spack will do when
you ask for a particular spec.


.. _install-method:

Implementing the ``install`` method
------------------------------------------

The last element of a package is its ``install()`` method.  This is
where the real work of installation happens, and it's the main part of
the package you'll need to customize for each piece of software.

.. literalinclude::  ../../../var/spack/packages/libelf/package.py
   :start-after: 0.8.12
   :linenos:

``install`` takes a ``spec``: a description of how the package should
be built, and a ``prefix``: the path to the directory where the
software should be installed.


Spack provides wrapper functions for ``configure`` and ``make`` so
that you can call them in a similar way to how you'd call a shell
comamnd.  In reality, these are Python functions.  Spack provides
these functions to make writing packages more natural. See the section
on :ref:`shell wrappers <shell-wrappers>`.



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

.. _install-environment:

The Install environment
--------------------------

In general, you should not have to do much differently in your install
method than you would when installing a pacakge on the command line.
In fact, you may need to do *less* than you would on the command line.

Spack tries to set environment variables and modify compiler calls so
that it *appears* to the build system that you're building with a
standard system install of everything.  Obviously that's not going to
cover *all* build systems, but it should make it easy to port packages
to Spack if they use a standard build system.  Usually with autotools
or cmake, building and installing is easy.  With builds that use
custom Makefiles, you may need to add logic to modify the makefiles.

The remainder of the section covers the way Spack's build environment
works.

Environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~

Spack sets a number of standard environment variables that serve two
purposes:

 #. Make build systems use Spack's compiler wrappers for their builds.
 #. Allow build systems to find dependencies more easily

The Compiler enviroment variables that Spack sets are:

  ============  ===============================
    Variable     Purpose
  ============  ===============================
    ``CC``       C compiler
    ``CXX``      C++ compiler
    ``F77``      Fortran 77 compiler
    ``FC``       Fortran 90 and above compiler
  ============  ===============================

All of these are standard variables respected by most build systems.
If your project uses ``autotools`` or ``CMake``, then it should pick
them up automatically when you run ``configure`` or ``cmake`` in the
``install()`` function.  Many traditional builds using GNU Make and
BSD make also respect these variables, so they may work with these
systems.

If your build system does *not* automatically pick these variables up
from the environment, then you can simply pass them on the command
line or use a patch as part of your build process to get the correct
compilers into the project's build system.  There are also some file
editing commands you can use -- these are described later in the
`section on file manipulation <file-manipulation_>`_.

In addition to the compiler variables, these variables are set before
entering ``install()`` so that packages can locate dependencies
easily:

  =======================  =============================
    ``PATH``                Set to point to ``/bin`` directories of dpeendencies
    ``CMAKE_PREFIX_PATH``   Path to dependency prefixes for CMake
    ``PKG_CONFIG_PATH``     Path to any pkgconfig directories for dependencies
  =======================  =============================

``PATH`` is set up to point to dependencies ``/bin`` directories so
that you can use tools installed by dependency packages at build time.
For example, ``$MPICH_ROOT/bin/mpicc`` is frequently used by dependencies of
``mpich``.

``CMAKE_PREFIX_PATH`` contains a colon-separated list of prefixes
where ``cmake`` will search for dependency libraries and headers.
This causes all standard CMake find commands to look in the paths of
your dependencies, so you *do not* have to manually specify arguments
like ``-D DEPENDENCY_DIR=/path/to/dependency`` to ``cmake``.  More on
this is `in the CMake documentation <http://www.cmake.org/cmake/help/v3.0/variable/CMAKE_PREFIX_PATH.html>`_.

``PKG_CONFIG_PATH`` is for packages that attempt to discover
dependencies using the GNU ``pkg-config`` tool.  It is similar to
``CMAKE_PREFIX_PATH`` in that it allows a build to automatically
discover its dependencies.


Compiler interceptors
~~~~~~~~~~~~~~~~~~~~~~~~~

As mentioned, ``CC``, ``CXX``, ``F77``, and ``FC`` are set to point to
Spack's compiler wrappers.  These are simply called ``cc``, ``c++``,
``f77``, and ``f90``, and they live in ``$SPACK_ROOT/lib/spack/env``.

``$SPACK_ROOT/lib/spack/env`` is added first in the ``PATH``
environment variable when ``install()`` runs so that system compilers
are not picked up instead.

All of these compiler wrappers point to a single compiler wrapper
script that figures out which *real* compiler it should be building
with.  This comes either from spec `concretization
<abstract-and-concrete>`_ or from a user explicitly asking for a
particular compiler using, e.g., ``%intel`` on the command line.

In addition to invoking the right compiler, the compiler wrappers add
flags to the compile line so that dependencies can be easily found.
These flags are added for each dependency, if they exist:

Compile-time library search paths
  * ``-L$dep_prefix/lib``
  * ``-L$dep_prefix/lib64``
Runtime library search paths (RPATHs)
  * ``-Wl,-rpath=$dep_prefix/lib``
  * ``-Wl,-rpath=$dep_prefix/lib64``
Include search paths
  * ``-I$dep_prefix/include``

An example of this would be the ``libdwarf`` build, which has one
dependency: ``libelf``.  Every call to ``cc`` in the ``libdwarf``
build will have ``-I$LIBELF_PREFIX/include``,
``-L$LIBELF_PREFIX/lib``, and ``-Wl,-rpath=$LIBELF_PREFIX/lib``
inserted on the command line.  This is done transparently to the
project's build system, which will just think it's using a system
where ``libelf`` is readily available.  Because of this, you **do
not** have to insert extra ``-I``, ``-L``, etc. on the command line.

Another useful consequence of this is that you often do *not* have to
add extra parameters on the ``configure`` line to get autotools to
find dependencies.  The ``libdwarf`` install method just calls
configure like this:

.. code-block:: python

   configure("--prefix=" + prefix)

Because of the ``-L`` and ``-I`` arguments, configure will
successfully find ``libdwarf.h`` and ``libdwarf.so``, without the
packager having to provide ``--with-libdwarf=/path/to/libdwarf`` on
the command line.

Forking ``install()``
~~~~~~~~~~~~~~~~~~~~~

To give packagers free reign over their install environemnt, Spack
forks a new process each time it invokes a package's ``install()``
method.  This allows packages to have their own completely sandboxed
build environment, without impacting other jobs that the main Spack
process runs.  Packages are free to change the environment or to
modify Spack internals, because each ``install()`` call has its own
dedicated process.


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
``prefix`` object.  Here is a full list:

  =========================  ================================================
  Prefix Attribute           Location
  =========================  ================================================
  ``prefix.bin``             ``$prefix/bin``
  ``prefix.sbin``            ``$prefix/sbin``
  ``prefix.etc``             ``$prefix/etc``
  ``prefix.include``         ``$prefix/include``
  ``prefix.lib``             ``$prefix/lib``
  ``prefix.lib64``           ``$prefix/lib64``
  ``prefix.libexec``         ``$prefix/libexec``
  ``prefix.share``           ``$prefix/share``
  ``prefix.doc``             ``$prefix/doc``
  ``prefix.info``            ``$prefix/info``

  ``prefix.man``             ``$prefix/man``
  ``prefix.man[1-8]``        ``$prefix/man/man[1-8]``

  ``prefix.share_man``       ``$prefix/share/man``
  ``prefix.share_man[1-8]``  ``$prefix/share/man[1-8]``
  =========================  ================================================

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

Shell command functions
----------------------------

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


.. _file-manipulation:

File manipulation functions
------------------------------

Many builds are not perfect. If a build lacks an install target, or if
it does not use systems like CMake or autotools, which have standard
ways of setting compilers and options, you may need to edit files or
install some files yourself to get them working with Spack.

You can do this with standard Python code, and Python has rich
libraries with functions for file manipulation and filtering.  Spack
also provides a number of convenience functions of its own to make
your life even easier.  These functions are described in this section.

All of the functions in this section can be included by simply
running:

.. code-block:: python

   from spack import *

This is already part of the boilerplate for packages created with
``spack create`` or ``spack edit``.


Filtering functions
~~~~~~~~~~~~~~~~~~~~~~

:py:func:`filter_file(regex, repl, *filenames, **kwargs) <spack.filter_file>`
  Works like ``sed`` but with Python regular expression syntax.  Takes
  a regular expression, a replacement, and a set of files.  ``repl``
  can be a raw string or a callable function.  If it is a raw string,
  it can contain ``\1``, ``\2``, etc. to refer to capture groups in
  the regular expression.  If it is a callable, it is passed the
  Python ``MatchObject`` and should return a suitable replacement
  string for the particular match.

  Examples:

  #. Replacing ``#!/usr/bin/perl`` with ``#!/usr/bin/env perl`` in ``bib2xhtml``:

     .. code-block:: python

        filter_file(r'#!/usr/bin/perl',
                    '#!/usr/bin/env perl', join_path(prefix.bin, 'bib2xhtml'))

  #. Switching the compilers used by ``mpich``'s MPI wrapper scripts from
     ``cc``, etc. to the compilers used by the Spack build:

     .. code-block:: python

        filter_file('CC="cc"', 'CC="%s"' % self.compiler.cc,
                    join_path(prefix.bin, 'mpicc'))

        filter_file('CXX="c++"', 'CXX="%s"' % self.compiler.cxx,
                    join_path(prefix.bin, 'mpicxx'))

:py:func:`change_sed_delimiter(old_delim, new_delim, *filenames) <spack.change_sed_delim>`
    Some packages, like TAU, have a build system that can't install
    into directories with, e.g. '@' in the name, because they use
    hard-coded ``sed`` commands in their build.

    ``change_sed_delimiter`` finds all ``sed`` search/replace commands
    and change the delimiter.  e.g., if the file contains commands
    that look like ``s///``, you can use this to change them to
    ``s@@@``.

    Example of changing ``s///`` to ``s@@@`` in TAU:

    .. code-block:: python

       change_sed_delimiter('@', ';', 'configure')
       change_sed_delimiter('@', ';', 'utils/FixMakefile')
       change_sed_delimiter('@', ';', 'utils/FixMakefile.sed.default')


File functions
~~~~~~~~~~~~~~~~~~~~~~

:py:func:`ancestor(dir, n=1) <spack.ancestor>`
  Get the n\ :sup:`th` ancestor of the directory ``dir``.

:py:func:`can_access(path) <spack.can_access>`
  True if we can read and write to the file at ``path``.  Same as
  native python ``os.access(file_name, os.R_OK|os.W_OK)``.

:py:func:`install(src, dest) <spack.install>`
  Install a file to a particular location.  For example, install a
  header into the ``include`` directory under the install ``prefix``:

  .. code-block:: python

     install('my-header.h', join_path(prefix.include))

:py:func:`join_path(prefix, *args) <spack.join_path>` Like
  ``os.path.join``, this joins paths using the OS path separator.
  However, this version allows an arbitrary number of arguments, so
  you can string together many path components.

:py:func:`mkdirp(*paths) <spack.mkdirp>`
  Create each of the directories in ``paths``, creating any parent
  directories if they do not exist.

:py:func:`working_dir(dirname, kwargs) <spack.working_dir>`
  This is a Python `Context Manager
  <https://docs.python.org/2/library/contextlib.html>`_ that makes it
  easier to work with subdirectories in builds.  You use this with the
  Python ``with`` statement to change into a working directory, and
  when the with block is done, you change back to the original
  directory.  Think of it as a safe ``pushd`` / ``popd`` combination,
  where ``popd`` is guaranteed to be called at the end, even if
  exceptions are thrown.

  Example usage:

  #. The ``libdwarf`` build first runs ``configure`` and ``make`` in a
     subdirectory called ``libdwarf``.  It then implements the
     installation code itself.  This is natural with ``working_dir``:

     .. code-block:: python

        with working_dir('libdwarf'):
            configure("--prefix=" + prefix, "--enable-shared")
            make()
            install('libdwarf.a',  prefix.lib)

  #. Many CMake builds require that you build "out of source", that
     is, in a subdirectory.  You can handle creating and ``cd``'ing to
     the subdirectory like the LLVM package does:

     .. code-block:: python

        with working_dir('spack-build', create=True):
            cmake('..',
                  '-DLLVM_REQUIRES_RTTI=1',
                  '-DPYTHON_EXECUTABLE=/usr/bin/python',
                  '-DPYTHON_INCLUDE_DIR=/usr/include/python2.6',
                  '-DPYTHON_LIBRARY=/usr/lib64/libpython2.6.so',
                  *std_cmake_args)
            make()
            make("install")

     The ``create=True`` keyword argument causes the command to create
     the directory if it does not exist.


:py:func:`touch(path) <spack.touch>`
  Create an empty file at ``path``.


.. _pacakge-lifecycle:

Package Workflow Commands
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

A typical package workflow might look like this:

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


Keeping the stage directory on success
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, ``spack install`` will delete the staging area once a
pacakge has been successfully built and installed.  Use
``--keep-stage`` to leave the build directory intact:

.. code-block:: sh

   spack install --keep-stage <spec>

This allows you to inspect the build directory and potentially debug
the build.  You can use ``purge`` or ``clean`` later to get rid of the
unwanted temporary files.


Keeping the install prefix on failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, ``spack install`` will delete any partially constructed
install prefix if anything fails during ``install()``.  If you want to
keep the prefix anyway (e.g. to diagnose a bug), you can use
``--keep-prefix``:

.. code-block:: sh

   spack install --keep-prefix <spec>

Note that this may confuse Spack into thinking that the package has
been installed properly, so you may need to use ``spack uninstall -f``
to get rid of the install prefix before you build again:

.. code-block:: sh

   spack uninstall -f <spec>


Interactive Shell Support
--------------------------

Spack provides some limited shell support to make life easier for
packagers.  You can enable these commands by sourcing a setup file in
the ``/share/spack`` directory.  For ``bash`` or ``ksh``, run::

  . $SPACK_ROOT/share/spack/setup-env.sh

For ``csh`` and ``tcsh`` run:

  setenv SPACK_ROOT /path/to/spack
  source $SPACK_ROOT/share/spack/setup-env.csh

``spack cd`` will then be available.


``spack cd``
~~~~~~~~~~~~~~~~~

``spack cd`` allows you to quickly cd to pertinent directories in Spack.
Suppose you've staged a package but you want to modify it before you
build it:

.. code-block:: sh

   $ spack stage libelf
   ==> Trying to fetch from http://www.mr511.de/software/libelf-0.8.13.tar.gz
   ######################################################################## 100.0%
   ==> Staging archive: /Users/gamblin2/src/spack/var/spack/stage/libelf@0.8.13%gcc@4.8.3=linux-ppc64/libelf-0.8.13.tar.gz
   ==> Created stage in /Users/gamblin2/src/spack/var/spack/stage/libelf@0.8.13%gcc@4.8.3=linux-ppc64.
   $ spack cd libelf
   $ pwd
   /Users/gamblin2/src/spack/var/spack/stage/libelf@0.8.13%gcc@4.8.3=linux-ppc64/libelf-0.8.13

``spack cd`` here changed he current working directory to the
directory containing theexpanded ``libelf`` source code.  There are a
number of other places you can cd to in the spack directory hierarchy:

.. command-output:: spack cd -h

Some of these change directory into package-specific locations (stage
directory, install directory, package directory) and others change to
core spack locations.  For example, ``spack cd -m`` will take you to
the main python source directory of your spack install.


``spack location``
~~~~~~~~~~~~~~~~~~~~~~

``spack location`` is the same as ``spack cd`` but it does not require
shell support.  It simply prints out the path you ask for, rather than
cd'ing to it.  In bash, this::

  cd $(spack location -b <spec>)

is the same as::

  spack cd -b <spec>

``spack location`` is intended for use in scripts or makefiles that
need to know where packages are installed.  e.g., in a makefile you
might write:

.. code-block:: makefile

   DWARF_PREFIX = $(spack location -i libdwarf)
   CXXFLAGS += -I$DWARF_PREFIX/include
   CXXFLAGS += -L$DWARF_PREFIX/lib
