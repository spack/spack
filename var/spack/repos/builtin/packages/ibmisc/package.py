# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ibmisc(CMakePackage):
    """Misc. reusable utilities used by IceBin."""

    homepage = "https://github.com/citibeth/ibmisc"
    url      = "https://github.com/citibeth/ibmisc/archive/v0.1.0.tar.gz"

    maintainers = ['citibeth']

    version('0.2.0', sha256='46ea0eb515475f482de333c7e7ad14f621ad2a41baafd115bc2ecc6a6a0b7580')
    version('0.1.3', sha256='b635848dc50060bafac4b2d43d5da751884c3d5938a894b7f49a1399a01b2b8c')
    version('0.1.2', sha256='021f29d7e667d5a0aee47d40c7a85733e555ae98493d849f4779ff772b131f86')
    version('0.1.1', sha256='2738136fe7f0e9393d6417802cd6d9d1ed9e7da778c815db5bd3ca9a16631064')
    version('0.1.0', sha256='38481a8680aad4b40eca6723b2898b344cf0ef891ebc3581f5e99fbe420fa0d8')

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
    depends_on('proj@:4', when='+proj')
    depends_on('blitz', when='+blitz')
    depends_on('netcdf-cxx4', when='+netcdf')
    depends_on('udunits', when='+udunits2')
    depends_on('googletest', when='+googletest', type='build')
    depends_on('py-cython', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('boost', when='+boost')

    # Build dependencies
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
