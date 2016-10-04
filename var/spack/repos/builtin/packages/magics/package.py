##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Magics(Package):
    """Magics is the latest generation of the ECMWF's Meteorological plotting
       software MAGICS. Although completely redesigned in C++, it is intended
       to be as backwards-compatible as possible with the Fortran interface."""

    homepage = "https://software.ecmwf.int/wiki/display/MAGP/Magics"
    url      = "https://software.ecmwf.int/wiki/download/attachments/3473464/Magics-2.29.0-Source.tar.gz"

    # Maintainers of Magics do not keep tarballs of minor releases. Once the
    # next minor released is published the previous one becomes unavailable.
    # That is why the preferred version is the latest stable one.
    version('2.29.4', '91c561f413316fb665b3bb563f3878d1')
    version('2.29.0', 'db20a4d3c51a2da5657c31ae3de59709', preferred=True)

    # The patch changes the hardcoded path to python in shebang to enable the
    # usage of the first python installation that appears in $PATH
    patch('no_hardcoded_python.patch')

    # The patch reorders includes and adds namespaces where necessary to
    # resolve ambiguity of invocations of isnan and isinf functions. The
    # patch is not needed since the version 2.29.1
    patch('resolve_isnan_ambiguity.patch', when='@2.29.0')

    variant('bufr', default=False, description='Enable BUFR support')
    variant('netcdf', default=False, description='Enable NetCDF support')
    variant('cairo', default=True, description='Enable cairo support[png/jpeg]')
    variant('metview', default=False, description='Enable metview support')
    variant('qt', default=False, description='Enable metview support with qt')

    depends_on('cmake', type='build')
    depends_on('pkg-config', type='build')

    # Currently python is only necessary to run
    # building preprocessing scripts.
    depends_on('python', type='build')
    depends_on('grib-api')
    depends_on('proj')
    depends_on('boost')
    depends_on('expat')
    depends_on('pango', when='+cairo')
    depends_on('netcdf-cxx', when='+netcdf')
    depends_on('libemos', when='+bufr')
    depends_on('qt', when='+metview+qt')

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)
        options.append('-DENABLE_ODB=OFF')
        options.append('-DENABLE_PYTHON=OFF')
        options.append('-DBOOST_ROOT=%s' % spec['boost'].prefix)
        options.append('-DPROJ4_PATH=%s' % spec['proj'].prefix)
        options.append('-DGRIB_API_PATH=%s' % spec['grib-api'].prefix)
        options.append('-DENABLE_TESTS=OFF')

        if '+bufr' in spec:
            options.append('-DENABLE_BUFR=ON')
            options.append('-DLIBEMOS_PATH=%s' % spec['libemos'].prefix)
        else:
            options.append('-DENABLE_BUFR=OFF')

        if '+netcdf' in spec:
            options.append('-DENABLE_NETCDF=ON')
            options.append('-DNETCDF_PATH=%s' % spec['netcdf-cxx'].prefix)
        else:
            options.append('-DENABLE_NETCDF=OFF')

        if '+cairo' in spec:
            options.append('-DENABLE_CAIRO=ON')
        else:
            options.append('-DENABLE_CAIRO=OFF')

        if '+metview' in spec:
            if '+qt' in spec:
                options.append('-DENABLE_METVIEW=ON')
                if spec['qt'].version.up_to(1) == '5':
                    options.append('-DENABLE_QT5=ON')
            else:
                options.append('-DENABLE_METVIEW_NO_QT=ON')
        else:
            options.append('-DENABLE_METVIEW=OFF')

        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            options.append('-DENABLE_FORTRAN=OFF')

        with working_dir('spack-build', create=True):
            cmake('..', *options)
            make()
            make('install')
