from spack import *
import os

class PyShiboken(Package):
    """Shiboken generates bindings for C++ libraries using CPython source code."""
    homepage = "https://shiboken.readthedocs.org/"
    url      = "https://pypi.python.org/packages/source/S/Shiboken/Shiboken-1.2.2.tar.gz"

    version('1.2.2', '345cfebda221f525842e079a6141e555')

    # TODO: make build dependency
    # depends_on("cmake")

    extends('python')
    depends_on("py-setuptools")
    depends_on("libxml2")
    depends_on("qt@:4.8")

    def patch(self):
        """Undo Shiboken RPATH handling and add Spack RPATH."""
        # Add Spack's standard CMake args to the sub-builds.
        # They're called BY setup.py so we have to patch it.
        pypkg = self.spec['python'].package
        rpath = self.rpath
        rpath.append(os.path.join(self.prefix, pypkg.site_packages_dir, 'Shiboken'))

        filter_file(
            r'OPTION_CMAKE,',
            r'OPTION_CMAKE, ' + (
                '"-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE", '
                '"-DCMAKE_INSTALL_RPATH=%s",' % ':'.join(rpath)),
            'setup.py')

        # Shiboken tries to patch ELF files to remove RPATHs
        # Disable this and go with the one we set.
        filter_file(
            r'^\s*rpath_cmd\(shiboken_path, srcpath\)',
            r'#rpath_cmd(shiboken_path, srcpath)',
            'shiboken_postinstall.py')


    def install(self, spec, prefix):
        python('setup.py', 'install',
               '--prefix=%s' % prefix,
               '--jobs=%s' % make_jobs)
