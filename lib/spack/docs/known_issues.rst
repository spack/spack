============
Known Issues
============

This is a list of known bugs in Spack. It provides ways of getting around these
problems if you encounter them.

-----------------------------------------------------------------
Default variants are not taken into account during concretization
-----------------------------------------------------------------

**Status:** Expected to be fixed in the next release

Current concretization algorithm does not take into account default values
of variants when adding extra constraints to the spec via CLI. For example
you may encounter the following error when trying to specify which MPI provider
to use:

.. code-block:: console

   $ spack install hdf5 ^openmpi
   ==> Error: hdf5 does not depend on openmpi

although the hdf5 package contains:

.. code-block:: python

   variant('mpi', default=True, description='Enable MPI support')
   depends_on('mpi', when='+mpi')

A workaround is to explicitly activate the variant related to the dependency:

.. code-block:: console

   $ spack install hdf5+mpi ^openmpi

See https://github.com/LLNL/spack/issues/397 for further details.


---------------------------------
``spack extensions`` doesn't work
---------------------------------

**Status:** Up for grabs if you want to try to fix it

Spack provides an ``extensions`` command that lists all available extensions
of a package, the ones that are installed, and the ones that are already
activated. This is very useful in conjunction with ``spack activate``.
Unfortunately, this command no longer works:

.. code-block:: console

   $ spack extensions python
   ==> python@2.7.13%clang@8.0.0-apple~tk~ucs4 arch=darwin-sierra-x86_64 -ckrr4mg has no extensions.


See https://github.com/LLNL/spack/issues/2895 for further details.


----------------------------
``spack setup`` doesn't work
----------------------------

**Status:** Work in progress

Spack provides a ``setup`` command that is useful for the development of
software outside of Spack. Unfortunately, this command no longer works.
See https://github.com/LLNL/spack/issues/2597 and
https://github.com/LLNL/spack/issues/2662 for details. This is expected
to be fixed by https://github.com/LLNL/spack/pull/2664.
