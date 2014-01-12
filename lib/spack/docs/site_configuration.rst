.. _site-configuration:

Site-specific configuration
===================================

.. _temp-space:

Temporary space
----------------------------

By default, Spack will try to do all of its building in temporary
space.  There are two main reasons for this.  First, Spack is designed
to run out of a user's home directory, and on may systems the home
directory is network mounted and potentially not a very fast
filesystem.  We create build stages in a temporary directory to avoid
this.  Second, many systems impose quotas on home directories, and
``/tmp`` or similar directories often have more available space.  This
helps conserve space for installations in users' home directories.

You can customize temporary directories by editing
``lib/spack/spack/globals.py``.  Specifically, find this part of the file:

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
               '/var/tmp/%u/spcak-stage',
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
