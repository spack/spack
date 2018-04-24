##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Ibmisc(CMakePackage):
    """Misc. reusable utilities used by IceBin."""

    homepage = "https://github.com/citibeth/ibmisc"
    url      = "https://codeload.github.com/citibeth/ibmisc/tar.gz/v0.1.0.tar.gz"

    maintainers = ['citibeth']

    version('0.1.3', 'bb1876a8d1f0710c1a031280c0fc3f2e')

    version('develop',
        git='https://github.com/citibeth/ibmisc.git',
        branch='develop')

    variant('everytrace', default=True,
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
    variant('doc', default=False,
            description='Build the documentation')

    extends('python')
    depends_on('python@3:')    # Needed for the build...

    depends_on('eigen')
    depends_on('everytrace', when='+everytrace')
    depends_on('proj', when='+proj')
    depends_on('blitz', when='+blitz')
    depends_on('netcdf-cxx4', when='+netcdf')
    depends_on('udunits2', when='+udunits2')
    depends_on('googletest', when='+googletest', type='build')
    depends_on('py-cython', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('boost', when='+boost')

    # Build dependencies
    depends_on('doxygen', type='build')
    depends_on('doxygen', when='+doc', type='build')

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
            '-DBUILD_PYTHON=%s' % ('YES' if '+python' in spec else 'NO'),
            '-DUSE_PROJ4=%s' % ('YES' if '+proj' in spec else 'NO'),
            '-DUSE_BLITZ=%s' % ('YES' if '+blitz' in spec else 'NO'),
            '-DUSE_NETCDF=%s' % ('YES' if '+netcdf' in spec else 'NO'),
            '-DUSE_BOOST=%s' % ('YES' if '+boost' in spec else 'NO'),
            '-DUSE_UDUNITS2=%s' % ('YES' if '+udunits2' in spec else 'NO'),
            '-DUSE_GTEST=%s' % ('YES' if '+googletest' in spec else 'NO'),
            '-DBUILD_DOCS=%s' % ('YES' if '+doc' in spec else 'NO')]

        if '+python' in spec:
            args.append(
                '-DCYTHON_EXECUTABLE=%s' % spec['py-cython'].command.path)

        return args
