##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import glob


class Magics(CMakePackage):
    """Magics is the latest generation of the ECMWF's Meteorological plotting
       software MAGICS. Although completely redesigned in C++, it is intended
       to be as backwards-compatible as possible with the Fortran interface."""

    homepage = "https://software.ecmwf.int/wiki/display/MAGP/Magics"
    url      = "https://software.ecmwf.int/wiki/download/attachments/3473464/Magics-2.29.0-Source.tar.gz"

    # Maintainers of Magics do not keep tarballs of minor releases. Once the
    # next minor released is published the previous one becomes unavailable.
    # That is why the preferred version is the latest stable one.
    version('2.32.0', 'e17956fffce9ea826cf994f8d275e0f5')
    version('2.29.4', '91c561f413316fb665b3bb563f3878d1')
    version('2.29.0', 'db20a4d3c51a2da5657c31ae3de59709', preferred=True)

    # The patch reorders includes and adds namespaces where necessary to
    # resolve ambiguity of invocations of isnan and isinf functions. The
    # patch is not needed since the version 2.29.1
    patch('resolve_isnan_ambiguity.patch', when='@2.29.0')

    variant('bufr', default=False, description='Enable BUFR support')
    variant('netcdf', default=False, description='Enable NetCDF support')
    variant('cairo', default=True, description='Enable cairo support[png/jpeg]')
    variant('metview', default=False, description='Enable metview support')
    variant('qt', default=False, description='Enable metview support with qt')
    variant('eccodes', default=False, description='Use eccodes instead of grib-api')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'Production'))

    depends_on('cmake@2.8.11:', type='build')
    depends_on('pkg-config', type='build')

    # Currently python is only necessary to run
    # building preprocessing scripts.
    depends_on('python', type='build')
    depends_on('perl', type='build')
    depends_on('perl-xml-parser', type='build')
    depends_on('eccodes', when='+eccodes')
    depends_on('grib-api', when='~eccodes')
    depends_on('proj')
    depends_on('boost')
    depends_on('expat')
    depends_on('pango', when='+cairo')
    depends_on('netcdf-cxx', when='+netcdf')
    depends_on('libemos', when='+bufr')
    depends_on('qt', when='+metview+qt')

    conflicts('+eccodes', when='@:2.29.0')

    # Replace system python and perl by spack versions:
    def patch(self):
        for plfile in glob.glob('*/*.pl'):
            filter_file('#!/usr/bin/perl', '#!/usr/bin/env perl', plfile)
        for pyfile in glob.glob('*/*.py'):
            filter_file('#!/usr/bin/python', '#!/usr/bin/env python', pyfile)

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DENABLE_ODB=OFF',
            '-DENABLE_PYTHON=OFF',
            '-DBOOST_ROOT=%s' % spec['boost'].prefix,
            '-DPROJ4_PATH=%s' % spec['proj'].prefix,
            '-DENABLE_TESTS=OFF',
        ]

        if '+bufr' in spec:
            args.append('-DENABLE_BUFR=ON')
            args.append('-DLIBEMOS_PATH=%s' % spec['libemos'].prefix)
        else:
            args.append('-DENABLE_BUFR=OFF')

        if '+netcdf' in spec:
            args.append('-DENABLE_NETCDF=ON')
            args.append('-DNETCDF_PATH=%s' % spec['netcdf-cxx'].prefix)
        else:
            args.append('-DENABLE_NETCDF=OFF')

        if '+cairo' in spec:
            args.append('-DENABLE_CAIRO=ON')
        else:
            args.append('-DENABLE_CAIRO=OFF')

        if '+metview' in spec:
            if '+qt' in spec:
                args.append('-DENABLE_METVIEW=ON')
                if spec['qt'].version[0] == 5:
                    args.append('-DENABLE_QT5=ON')
            else:
                args.append('-DENABLE_METVIEW_NO_QT=ON')
        else:
            args.append('-DENABLE_METVIEW=OFF')

        if '+eccodes' in spec:
            args.append('-DENABLE_ECCODES=ON')
            args.append('-DECCODES_PATH=%s' % spec['eccodes'].prefix)
        else:
            args.append('-DENABLE_ECCODES=OFF')
            args.append('-DGRIB_API_PATH=%s' % spec['grib-api'].prefix)

        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            args.append('-DENABLE_FORTRAN=OFF')

        return args
