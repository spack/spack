.. _octavepackage:

-------------
OctavePackage
-------------

Octave has its own build system for installing packages.

^^^^^^
Phases
^^^^^^

This package has
``install`` phase only which essentially executes


.. code-block:: console

   $ octave '--eval' 'pkg prefix <prefix>; pkg install <archive_file>'

Beware that uninstallation is not implemented at the moment. After uninstalling
a package via Spack, you also need to manually uninstall it from Octave
``pkg uninstall <package_name>``.

^^^^^^^^^^^^^^^^^^^^^^^
Finding Octave packages
^^^^^^^^^^^^^^^^^^^^^^^
Most of Octave packages are listed at https://octave.sourceforge.io/packages.php.

^^^^^^^^^^^^
Dependencies
^^^^^^^^^^^^

Usually, the homepage of a package will list dependencies, i.e.
``Dependencies:	Octave >= 3.6.0 struct >= 1.0.12``. The same information should
be available in the ``DESCRIPTION`` file in the root of each archive.
