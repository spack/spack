.. _site-configuration:

Site-specific configuration
===================================

.. _mirrors:

Mirrors
----------------------------

Some sites may not have access to the internet for fetching packages.
These sites will need a local repository of tarballs from which they
can get their files.  Spack has support for this with *mirrors*.  A
mirror is a URL that points to a directory, either on the local
filesystem or on some server, containing tarballs for all of Spack's
packages.

Here's an example of a mirror's directory structure::

    mirror/
        cmake/
            cmake-2.8.10.2.tar.gz
        dyninst/
            DyninstAPI-8.1.1.tgz
            DyninstAPI-8.1.2.tgz
        libdwarf/
            libdwarf-20130126.tar.gz
            libdwarf-20130207.tar.gz
            libdwarf-20130729.tar.gz
        libelf/
            libelf-0.8.12.tar.gz
            libelf-0.8.13.tar.gz
        libunwind/
            libunwind-1.1.tar.gz
        mpich/
            mpich-3.0.4.tar.gz
        mvapich2/
        mvapich2-1.9.tgz

The structure is very simple.  There is a top-level directory.  The
second level directories are named after packages, and the third level
contains tarballs for each package, named as they were in the
package's fetch URL.

``spack mirror``
~~~~~~~~~~~~~~~~~~~~~~~

Mirrors are managed with the ``spack mirror`` command.  The help for
``spack mirror`` looks like this::

    $ spack mirror -h
    usage: spack mirror [-h] SUBCOMMAND ...

    positional arguments:
      SUBCOMMAND
        create           Create a directory to be used as a spack mirror, and fill
                         it with package archives.
        add              Add a mirror to Spack.
        remove           Remove a mirror by name.
        list             Print out available mirrors to the console.

    optional arguments:
      -h, --help         show this help message and exit

The ``create`` command actually builds a mirror by fetching all of its
packages from the internet and checksumming them.

The other three commands are for managing mirror configuration.  They
control the URL(s) from which Spack downloads its packages.


``spack mirror create``
~~~~~~~~~~~~~~~~~~~~~~~

You can create a mirror using the ``spack mirror create`` command, assuming
you're on a machine where you can access the internet.

The command will iterate through all of Spack's packages and download
the safe ones into a directory structure like the one above.  Here is
what it looks like:


.. code-block:: bash

   $ spack mirror create libelf libdwarf
   ==> Created new mirror in spack-mirror-2014-06-24
   ==> Trying to fetch from http://www.mr511.de/software/libelf-0.8.13.tar.gz
   ##########################################################                81.6%
   ==> Checksum passed for libelf@0.8.13
   ==> Added spack-mirror-2014-06-24/libelf/libelf-0.8.13.tar.gz to mirror
   ==> Trying to fetch from http://www.mr511.de/software/libelf-0.8.12.tar.gz
   ######################################################################    98.6%
   ==> Checksum passed for libelf@0.8.12
   ==> Added spack-mirror-2014-06-24/libelf/libelf-0.8.12.tar.gz to mirror
   ==> Trying to fetch from http://www.prevanders.net/libdwarf-20130207.tar.gz
   ######################################################################    97.3%
   ==> Checksum passed for libdwarf@20130207
   ==> Added spack-mirror-2014-06-24/libdwarf/libdwarf-20130207.tar.gz to mirror
   ==> Trying to fetch from http://www.prevanders.net/libdwarf-20130126.tar.gz
   ########################################################                  78.9%
   ==> Checksum passed for libdwarf@20130126
   ==> Added spack-mirror-2014-06-24/libdwarf/libdwarf-20130126.tar.gz to mirror
   ==> Trying to fetch from http://www.prevanders.net/libdwarf-20130729.tar.gz
   #############################################################             84.7%
   ==> Checksum passed for libdwarf@20130729
   ==> Added spack-mirror-2014-06-24/libdwarf/libdwarf-20130729.tar.gz to mirror

Once this is done, you can tar up the ``spack-mirror-2014-06-24`` directory and
copy it over to the machine you want it hosted on.

Custom package sets
^^^^^^^^^^^^^^^^^^^^^^^^

Normally, ``spack mirror create`` downloads all the archives it has
checksums for.  If you want to only create a mirror for a subset of
packages, you can do that by supplying a list of package specs on the
command line after ``spack mirror create``.  For example, this
command::

    $ spack mirror create libelf@0.8.12: boost@1.44:

Will create a mirror for libelf versions greater than or equal to
0.8.12 and boost versions greater than or equal to 1.44.

Mirror files
^^^^^^^^^^^^^^^^^^^^^^^^

If you have a *very* large number of packages you want to mirror, you
can supply a file with specs in it, one per line::

   $ cat specs.txt
   libdwarf
   libelf@0.8.12:
   boost@1.44:
   boost@1.39.0
   ...
   $ spack mirror create -f specs.txt
   ...

This is useful if there is a specific suite of software managed by
your site.


``spack mirror add``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have a mirrror, you need to let spack know about it.  This is
relatively simple.  First, figure out the URL for the mirror.  If it's
a file, you can use a file URL like this one::

    file:///Users/gamblin2/spack-mirror-2014-06-24

That points to the directory on the local filesystem.  If it were on a
web server, you could use a URL like this one:

    https://example.com/some/web-hosted/directory/spack-mirror-2014-06-24

Spack will use the URL as the root for all of the packages it fetches.
You can tell your Spack installation to use that mirror like this:

.. code-block:: bash

   $ spack mirror add local_filesystem file:///Users/gamblin2/spack-mirror-2014-06-24

Each mirror has a name so that you can refer to it again later.

``spack mirror list``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to see all the mirrors Spack knows about you can run ``spack mirror list``::

   $ spack mirror list
   local_filesystem    file:///Users/gamblin2/spack-mirror-2014-06-24

``spack mirror remove``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

And, if you want to remove a mirror, just remove it by name::

   $ spack mirror remove local_filesystem
   $ spack mirror list
   ==> No mirrors configured.

Mirror precedence
~~~~~~~~~~~~~~~~~~~~~~~~~

Adding a mirror really just adds a section in ``~/.spackconfig``::

   [mirror "local_filesystem"]
       url = file:///Users/gamblin2/spack-mirror-2014-06-24
   [mirror "remote_server"]
       url = https://example.com/some/web-hosted/directory/spack-mirror-2014-06-24

If you want to change the order in which mirrors are searched for
packages, you can edit this file and reorder the sections.  Spack will
search the topmost mirror first and the bottom-most mirror last.


.. _temp-space:

Temporary space
----------------------------

.. warning:: Temporary space configuration will be moved to configuration files.
   The intructions here are old and refer to ``__init__.py``

By default, Spack will try to do all of its building in temporary
space.  There are two main reasons for this.  First, Spack is designed
to run out of a user's home directory, and on may systems the home
directory is network mounted and potentially not a very fast
filesystem.  We create build stages in a temporary directory to avoid
this.  Second, many systems impose quotas on home directories, and
``/tmp`` or similar directories often have more available space.  This
helps conserve space for installations in users' home directories.

You can customize temporary directories by editing
``lib/spack/spack/__init__.py``.  Specifically, find this part of the file:

.. code-block:: python

   # Whether to build in tmp space or directly in the stage_path.
   # If this is true, then spack will make stage directories in
   # a tmp filesystem, and it will symlink them into stage_path.
   use_tmp_stage = True

   # Locations to use for staging and building, in order of preference
   # Use a %u to add a username to the stage paths here, in case this
   # is a shared filesystem.  Spack will use the first of these paths
   # that it can create.
   tmp_dirs = ['/nfs/tmp2/%u/spack-stage',
               '/var/tmp/%u/spack-stage',
               '/tmp/%u/spack-stage']

The ``use_tmp_stage`` variable controls whether Spack builds
**directly** inside the ``var/spack/`` directory.  Normally, Spack
will try to find a temporary directory for a build, then it *symlinks*
that temporary directory into ``var/spack/`` so that you can keep
track of what temporary directories Spack is using.

The ``tmp_dirs`` variable is a list of paths Spack should search when
trying to find a temporary directory.  They can optionally contain a
``%u``, which will substitute the current user's name into the path.
The list is searched in order, and Spack will create a temporary stage
in the first directory it finds to which it has write access.  Add
more elements to the list to indicate where your own site's temporary
directory is.


.. _concretization-policies:

Concretization policies
----------------------------

When a user asks for a package like ``mpileaks`` to be installed,
Spack has to make decisions like what version should be installed,
what compiler to use, and how its dependencies should be configured.
This process is called *concretization*, and it's covered in detail in
:ref:`its own section <abstract-and-concrete>`.

The default concretization policies are in the
:py:mod:`spack.concretize` module, specifically in the
:py:class:`spack.concretize.DefaultConcretizer` class.  These are the
important methods used in the concretization process:

* :py:meth:`concretize_version(self, spec) <spack.concretize.DefaultConcretizer.concretize_version>`
* :py:meth:`concretize_architecture(self, spec) <spack.concretize.DefaultConcretizer.concretize_architecture>`
* :py:meth:`concretize_compiler(self, spec) <spack.concretize.DefaultConcretizer.concretize_compiler>`
* :py:meth:`choose_provider(self, spec, providers) <spack.concretize.DefaultConcretizer.choose_provider>`

The first three take a :py:class:`Spec <spack.spec.Spec>` object and
modify it by adding constraints for the version.  For example, if the
input spec had a version range like `1.0:5.0.3`, then the
``concretize_version`` method should set the spec's version to a
*single* version in that range.  Likewise, ``concretize_architecture``
selects an architecture when the input spec does not have one, and
``concretize_compiler`` needs to set both a concrete compiler and a
concrete compiler version.

``choose_provider()`` affects how concrete implementations are chosen
based on a virtual dependency spec.  The input spec is some virtual
dependency and the ``providers`` index is a :py:class:`ProviderIndex
<spack.packages.ProviderIndex>` object.  The ``ProviderIndex`` maps
the virtual spec to specs for possible implementations, and
``choose_provider()`` should simply choose one of these.  The
``concretize_*`` methods will be called on the chosen implementation
later, so there is no need to fully concretize the spec when returning
it.

The ``DefaultConcretizer`` is intendend to provide sensible defaults
for each policy, but there are certain choices that it can't know
about.  For example, one site might prefer ``OpenMPI`` over ``MPICH``,
or another might prefer an old version of some packages.  These types
of special cases can be integrated with custom concretizers.

Writing a custom concretizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To write your own concretizer, you need only subclass
``DefaultConcretizer`` and override the methods you want to change.
For example, you might write a class like this to change *only* the
``concretize_version()`` behavior:

.. code-block:: python

   from spack.concretize import DefaultConcretizer

   class MyConcretizer(DefaultConcretizer):
       def concretize_version(self, spec):
           # implement custom logic here.

Once you have written your custom concretizer, you can make Spack use
it by editing ``globals.py``.  Find this part of the file:

.. code-block:: python

   #
   # This controls how things are concretized in spack.
   # Replace it with a subclass if you want different
   # policies.
   #
   concretizer = DefaultConcretizer()

Set concretizer to *your own* class instead of the default:

.. code-block:: python

   concretizer = MyConcretizer()

The next time you run Spack, your changes should take effect.
