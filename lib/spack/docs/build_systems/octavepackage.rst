.. _octavepackage:

-------------
OctavePackage
-------------

Octave has its own build system for installing packages. This package has
``install`` phase only which essentially executes


.. code-block:: console

   $ octave '--eval' 'pkg prefix <prefix>; pkg install <archive_file>'

Beware that uninstallation is not implemented at the moment. After uninstalling
a package via Spack, you also need to manually uninstall it from Octave
``pkg uninstall <package_name>``.
