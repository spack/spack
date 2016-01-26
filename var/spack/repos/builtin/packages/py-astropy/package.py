from spack import *

class PyAstropy(Package):
    """
    The Astropy Project is a community effort to develop a single core
    package for Astronomy in Python and foster interoperability between
    Python astronomy packages.
    """
    homepage = 'http://www.astropy.org/'

    version('1.1.post1', 'b52919f657a37d45cc45f5cb0f58c44d')

    def url_for_version(self, version):
        return 'https://pypi.python.org/packages/source/a/astropy/astropy-{0}.tar.gz'.format(version)

    extends('python')

    depends_on('cfitsio')
    depends_on('expat')
    depends_on('py-h5py')
    depends_on('py-numpy')
    depends_on('py-scipy')

    def install(self, spec, prefix):
        python('setup.py', 'build', '--use-system-cfitsio',
                                    '--use-system-expat')
        python('setup.py', 'install', '--prefix=' + prefix)

