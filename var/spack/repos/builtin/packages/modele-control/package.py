from spack import *

class ModeleControl(Package):
    """Misc. Python Stuff."""

    homepage = "https://github.com/citibeth/modele-control"
    url      = "https://github.com/citibeth/modele-control/tarball/v0.1.0"

    maintainers = ['citibeth']

    version('develop', git='https://github.com/citibeth/modele-control.git', branch='develop')

    extends('python')
    depends_on('python@3:')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-giss', type=('build','run'))
    depends_on('netcdf', type='run')        # ncdump executable

    # depends_on('binutils', type='run')    # ldd; assume already installed on system

    def install(self, spec, prefix):
        setup_py('install', '--prefix=%s' % prefix)
