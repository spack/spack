from spack import *


class Ibmisc(CMakePackage):
    """Misc. reusable utilities used by IceBin."""

    homepage = "https://github.com/citibeth/ibmisc"
    url      = "https://github.com/citibeth/ibmisc/tarball/123"

    version('0.1.0', '12f2a32432a11db48e00217df18e59fa')

    variant('everytrace', default=False,
            description='Report errors through Everytrace')
    variant('proj', default=True,
            description='Compile utilities for PROJ.4 library')
    variant('blitz', default=True,
            description='Compile utilities for Blitz library')
    variant('netcdf', default=True,
            description='Compile utilities for NetCDF library')
    variant('boost', default=True,
            description='Compile utilities for Boost library')
    variant('udunits2', default=True,
            description='Compile utilities for UDUNITS2 library')
    variant('googletest', default=True,
            description='Compile utilities for Google Test library')
    variant('python', default=True,
            description='Compile utilities for use with Python/Cython')

    extends('python')

    depends_on('eigen')
    depends_on('everytrace', when='+everytrace')
    depends_on('proj', when='+proj')
    depends_on('blitz', when='+blitz')
    depends_on('netcdf-cxx4', when='+netcdf')
    depends_on('udunits2', when='+udunits2')
    depends_on('googletest', when='+googletest', type='build')
    depends_on('py-cython', when='+python', type=nolink)
    depends_on('py-numpy', when='+python', type=nolink)
    depends_on('boost', when='+boost')

    # Build dependencies
    depends_on('cmake', type='build')
    depends_on('doxygen', type='build')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
            '-DUSE_PROJ4=%s' % ('YES' if '+proj' in spec else 'NO'),
            '-DUSE_BLITZ=%s' % ('YES' if '+blitz' in spec else 'NO'),
            '-DUSE_NETCDF=%s' % ('YES' if '+netcdf' in spec else 'NO'),
            '-DUSE_BOOST=%s' % ('YES' if '+boost' in spec else 'NO'),
            '-DUSE_UDUNITS2=%s' % ('YES' if '+udunits2' in spec else 'NO'),
            '-DUSE_GTEST=%s' % ('YES' if '+googletest' in spec else 'NO')]
