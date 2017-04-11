============
Known Issues
============

This is a list of known bugs in Spack. It provides ways of getting around these
problems if you encounter them.

-----------------------------------------------------------------
Default variants are not taken into account during concretization
-----------------------------------------------------------------

**Status:** Expected to be fixed in the next release

Current conretization algorithm does not take into account default values
of variants when adding extra constraints to the spec via CLI. For example
you may enounter the following error when trying to specify which MPI provider
to use

.. code-block:: console

   $ spack install hdf5 ^openmpi
   ==> Error: hdf5 does not depend on openmpi

although the hdf5 package contains

.. code-block:: python

   variant('mpi', default=True, description='Enable MPI support')
   depends_on('mpi', when='+mpi')

A workaround is to explicitly activate the variant related to the dependency:

.. code-block:: console

   $ spack install hdf5+mpi ^openmpi

See https://github.com/LLNL/spack/issues/397 for further details.
