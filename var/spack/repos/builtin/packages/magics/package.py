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
import glob


class Magics(CMakePackage):
    """Magics is the latest generation of the ECMWF's Meteorological plotting
       software MAGICS. Although completely redesigned in C++, it is intended
       to be as backwards-compatible as possible with the Fortran interface."""

    homepage = "https://software.ecmwf.int/wiki/display/MAGP/Magics"
    url      = "https://software.ecmwf.int/wiki/download/attachments/3473464/Magics-2.29.0-Source.tar.gz"
    list_url = "https://software.ecmwf.int/wiki/display/MAGP/Releases"

    # The policy on which minor releases remain available and which get deleted
    # after a newer version becomes available is unclear.
    version('2.34.3', 'b4180bc4114ffd723b80728947f50c17')
    version('2.34.1', '1ecc5cc20cb0c3f2f0b9171626f09d53')
    version('2.33.0', '8d513fd2244f2974b3517a8b30dd51f6')
    version('2.32.0', 'e17956fffce9ea826cf994f8d275e0f5')
    version('2.31.0', '3564dca9e1b4af096fd631906f5e6c89')
    version('2.29.6', '56d2c31ca75162e5e86ef75d355e87f1')
    version('2.29.4', '91c561f413316fb665b3bb563f3878d1')
    version('2.29.0', 'db20a4d3c51a2da5657c31ae3de59709')

    # The patch reorders includes and adds namespaces where necessary to
    # resolve ambiguity of invocations of isnan and isinf functions. The
    # patch is not needed since the version 2.29.1
    patch('resolve_isnan_ambiguity.patch', when='@2.29.0')

    variant('grib', default='eccodes', values=('eccodes', 'grib-api'),
            description='Specify GRIB backend')
    variant('netcdf', default=False, description='Enable NetCDF support')
    variant('cairo', default=False,
            description='Enable cairo support[png/jpeg]')
    variant('python', default=False, description='Enable Python interface')
    variant('fortran', default=False, description='Enable Fortran interface')
    variant('metview', default=False, description='Enable metview support')
    variant('qt', default=False, description='Enable metview support with qt')
    variant('bufr', default=False, description='Enable BUFR support')

    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'Production'))

    # Build dependencies
    depends_on('cmake@2.8.11:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python@:2', type='build')
    depends_on('perl', type='build')
    depends_on('perl-xml-parser', type='build')

    # Non-optional dependencies
    depends_on('proj')
    depends_on('boost')
    depends_on('expat')

    # Magics (at least up to version 2.34.3) should directly and
    # unconditionally depend on zlib, which is not reflected neither in the
    # installation instructions nor explicitly stated in the cmake script:
    # zlib is pulled as a dependency of png. The dependency on png is formally
    # optional and depends on an unofficial flag ENABLE_PNG, which is
    # redundant, because png is used only when ENABLE_CAIRO=ON. The problem is
    # that files that make calls to png library get compiled and linked
    # unconditionally, which makes png a non-optional dependency (and
    # ENABLE_PNG always has to be set to ON).
    depends_on('zlib')
    depends_on('libpng')

    # GRIB support is non-optional, regardless of what the instruction says.
    depends_on('eccodes', when='grib=eccodes')
    depends_on('grib-api', when='grib=grib-api')

    # Optional dependencies
    depends_on('netcdf-cxx', when='+netcdf')
    depends_on('pango', when='+cairo')
    depends_on('libemos grib=eccodes', when='+bufr grib=eccodes')
    depends_on('libemos grib=grib-api', when='+bufr grib=grib-api')
    depends_on('qt', when='+metview+qt')

    extends('python', when='+python')
    # Python 2 is required for running the building scripts. Since we can't
    # have two different versions of Python at the same time, we haven't even
    # tested if the Python interface supports Python 3.
    depends_on('python', when='+python', type=('link', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('swig', when='+python', type='build')

    conflicts('grib=eccodes', when='@:2.29.0',
              msg='Eccodes is supported starting version 2.29.1')
    conflicts('+python', when='@:2.28',
              msg='Python interface is supported starting version 2.29.0')

    # Replace system python and perl by spack versions:
    def patch(self):
        for plfile in glob.glob('*/*.pl'):
            filter_file('#!/usr/bin/perl', '#!/usr/bin/env perl', plfile)
        for pyfile in glob.glob('*/*.py'):
            filter_file('#!/usr/bin/python', '#!/usr/bin/env python', pyfile)

    def cmake_args(self):
        args = [
            '-DENABLE_ODB=OFF',
            '-DENABLE_SPOT=OFF'
        ]

        if self.spec.variants['grib'].value == 'eccodes':
            args.append('-DENABLE_ECCODES=ON')
        else:
            if self.spec.satisfies('@2.29.1:'):
                args.append('-DENABLE_ECCODES=OFF')

        if '+netcdf' in self.spec:
            args.append('-DENABLE_NETCDF=ON')
        else:
            args.append('-DENABLE_NETCDF=OFF')

        if '+cairo' in self.spec:
            args.append('-DENABLE_CAIRO=ON')
        else:
            args.append('-DENABLE_CAIRO=OFF')

        if '+python' in self.spec:
            args.append('-DENABLE_PYTHON=ON')
        else:
            if self.spec.satisfies('@2.29.0:'):
                args.append('-DENABLE_PYTHON=OFF')

        if '+fortran' in self.spec:
            args.append('-DENABLE_FORTRAN=ON')
        else:
            args.append('-DENABLE_FORTRAN=OFF')

        if '+bufr' in self.spec:
            args.append('-DENABLE_BUFR=ON')
        else:
            args.append('-DENABLE_BUFR=OFF')

        if '+metview' in self.spec:
            if '+qt' in self.spec:
                args.append('-DENABLE_METVIEW=ON')
                if self.spec['qt'].satisfies('@5:'):
                    args.append('-DENABLE_QT5=ON')
            else:
                args.append('-DENABLE_METVIEW_NO_QT=ON')
        else:
            args.append('-DENABLE_METVIEW=OFF')

        return args
