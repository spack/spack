from spack import *

class ModeleControl(Package):
    """Misc. Python Stuff."""

    homepage = "https://github.com/citibeth/modele-control"
    url      = "https://github.com/citibeth/modele-control/tarball/v0.1.0"

    version('develop', git='https://github.com/citibeth/modele-control.git', branch='develop')

    extends('python')
    depends_on('python@:2.8')

    depends_on('netcdf', type='run')

    # depends_on('binutils', type='run')    # ldd; assume already installed on system
    depends_on('netcdf', type='run')    # ncdump

    def install(self, spec, prefix):
        setup_py('install', '--prefix=%s' % prefix)
