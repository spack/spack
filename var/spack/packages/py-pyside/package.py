from spack import *
import spack.package
import os

class PyPyside(Package):
    """array processing for numbers, strings, records, and objects."""
    homepage = "https://pypi.python.org/pypi/pyside"
    url      = "https://pypi.python.org/packages/source/P/PySide/PySide-1.2.2.tar.gz"

    version('1.2.2', 'c45bc400c8a86d6b35f34c29e379e44d')

    extends('python')
    depends_on('py-setuptools')
    depends_on('qt@:4')


    def patch(Self):
        """Undo PySide RPATH handling and add Spack RPATH."""
        # Add Spack's standard CMake args to the sub-builds.
        # They're called BY setup.py so we have to patch it.
        filter_file(
            r'OPTION_CMAKE,',
            r'OPTION_CMAKE, ' + (
                '"-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE", '
                '"-DCMAKE_INSTALL_RPATH=%s",' % ':'.join(self.rpath)),
            'setup.py')

        # PySide tries to patch ELF files to remove RPATHs
        # Disable this and go with the one we set.
        filter_file(
            r'rpath_cmd\(pyside_path, srcpath\)',
            r'#rpath_cmd(pyside_path, srcpath)',
            'pyside_postinstall.py')


    def install(self, spec, prefix):
        python('setup.py', 'install',
               '--prefix=%s' % prefix,
               '--jobs=%s' % make_jobs)


