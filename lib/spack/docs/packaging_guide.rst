Packaging Guide
=====================

This guide is intended for developers or administrators who want to
*package* their software so that Spack can install it.  We assume that
you have at least some familiarty with Python, and that you've read
the :ref:`guide for regular users <basic_usage>`, especially the part
about *specs*.


Package files
-------------------------

There are two parts of Spack, a language for describing builds of
software (*specs*), and *packages*: Python modules thatactually build
the software.  A package essentially takes a spec and implements it
for a particular piece of software.  It allows a developer to
encapsulate build logic for different versions, compilers, and
platforms in one place, and it is designed to make things easy for
you, the packager, as much as possible.

Packages in spack live in ``$prefix/lib/spack/spack/packages``:

.. command-output::  cd $SPACK_ROOT/lib/spack/spack/packages;  ls *.py
   :shell:
   :ellipsis: 5


Package lifecycle
------------------------------

``spack install`` command performs a number of tasks before it finally
installs each package.  It downloads an archive, expands it in a
temporary directory, and then performs the installation.  Spack has
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



Dependencies
-------------------------



Virtual dependencies
-------------------------



Packaging commands
-------------------------

``spack edit``
~~~~~~~~~~~~~~~~~~~~

``spack create``
~~~~~~~~~~~~~~~~~~~~

``spack checksum``
~~~~~~~~~~~~~~~~~~~~

``spack graph``
~~~~~~~~~~~~~~~~~~~~
