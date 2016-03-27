from spack import *
import os

class PyPyside(Package):
    """Python bindings for Qt."""
    homepage = "https://pypi.python.org/pypi/pyside"
    url      = "https://pypi.python.org/packages/source/P/PySide/PySide-1.2.2.tar.gz"

    # This doesn't work, GitHub download isn't the same as the full tarfile.
    # The tarfile for 1.2.3 was removed from PyPI.
    # url = "https://github.com/PySide/pyside-setup/tarball/1.2.3"

    # Version 1.2.4 claims to not work with Python 3.5, mostly
    # because it hasn't been tested.  Otherwise, it's the same as v1.2.3
    # https://github.com/PySide/pyside-setup/issues/58
    # Meanwhile, developers have moved onto pyside2 (for Qt5),
    # and show little interest in certifying PySide 1.2.4 for Python.
    version('1.2.4', '3cb7174c13bd45e3e8f77638926cb8c0')

    # This is not available from pypi
    # version('1.2.3', 'fa5d5438b045ede36104bba25a6ccc10')

# v1.2.2 does not work with Python3
#    version('1.2.2', 'c45bc400c8a86d6b35f34c29e379e44d')

    # TODO: make build dependency
    depends_on("cmake")

    extends('python')
    depends_on('py-setuptools')
    depends_on('qt@:4')

    def patch(self):
        """Undo PySide RPATH handling and add Spack RPATH."""
        # Figure out the special RPATH
        pypkg = self.spec['python'].package
        rpath = self.rpath
        rpath.append(os.path.join(self.prefix, pypkg.site_packages_dir, 'PySide'))

        # Add Spack's standard CMake args to the sub-builds.
        # They're called BY setup.py so we have to patch it.
        filter_file(
            r'OPTION_CMAKE,',
            r'OPTION_CMAKE, ' + (
                '"-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE", '
                '"-DCMAKE_INSTALL_RPATH=%s",' % ':'.join(rpath)),
            'setup.py')


        # Convince PySide that it really CAN work with Python 3.5
        filter_file(
            "'Programming Language :: Python :: 3.4',",
            "'Programming Language :: Python :: 3.4',\n        'Programming Language :: Python :: 3.5',",
            'setup.py')

# As of version 1.2.3, PySide removed the post-install script.
#        # PySide tries to patch ELF files to remove RPATHs
#        # Disable this and go with the one we set.
#        filter_file(
#            r'^\s*rpath_cmd\(pyside_path, srcpath\)',
#            r'#rpath_cmd(pyside_path, srcpath)',
#            'pyside_postinstall.py')


    def install(self, spec, prefix):
        python('setup.py', 'install',
               '--prefix=%s' % prefix,
               '--jobs=%s' % make_jobs)
