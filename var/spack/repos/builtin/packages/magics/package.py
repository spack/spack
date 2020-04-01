# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os


class Magics(CMakePackage):
    """Magics is the latest generation of the ECMWF's Meteorological plotting
       software MAGICS. Although completely redesigned in C++, it is intended
       to be as backwards-compatible as possible with the Fortran interface."""

    homepage = "https://software.ecmwf.int/wiki/display/MAGP/Magics"
    url      = "https://confluence.ecmwf.int/download/attachments/3473464/Magics-4.1.0-Source.tar.gz?api=v2"
    list_url = "https://software.ecmwf.int/wiki/display/MAGP/Releases"

    # The policy on which minor releases remain available and which get deleted
    # after a newer version becomes available is unclear.
    version('4.1.0', sha256='e56fb1bf82d57957a61a76284ad22024f4a7c3c989f6f796e57dfd45d88400c0')
    version('2.34.3', sha256='38487562e83c0470f94d9c7fb9418cbadf92f1e643033237baba2abdc77e6238')
    version('2.34.1', sha256='8df27f8f262ebc32a61f8696df15a7b4a6e4203b2a8e53fe7aa13caa1c4e3fa4')
    version('2.33.0', sha256='32d3079749f89988715a8c3df01b712d9b989b7fd242828ec09563e47c5a3e82')
    version('2.32.0', sha256='233b046c93b84be60ac8011212668de35c2693d89fffcaad333b42b8c4ffad06')
    version('2.31.0', sha256='13c314661bb154499a87db9063238d6ecebad0d4fec37b0f3d90fe34aa37eec6')
    version('2.29.6', sha256='88cfa5e2bd823c4669a3d2fe0349f14545e810333c1b4d031ce74a7a5218a2db')
    version('2.29.4', sha256='82bdb4f7e38776776d2155a82d0acaa017402365a043731708345ac4ac00198f')
    version('2.29.0', sha256='4c5067c4630e831bf81d15454476ff0d050c488b768f6a10272aad62ce8d0f92')

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
    depends_on('python', type='build')
    depends_on('python@:2', type='build', when='@:3')
    depends_on('perl', type='build')
    depends_on('perl-xml-parser', type='build')

    # Non-optional dependencies
    depends_on('proj@:5')
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
    conflicts('+python', when='@4:',
              msg='Python interface is separate from the library '
              'starting with 4.0.0')

    # Replace system python and perl by spack versions:
    def patch(self):
        for plfile in glob.glob('*/*.pl'):
            filter_file('#!/usr/bin/perl', '#!/usr/bin/env perl', plfile)
        for pyfile in glob.glob('*/*.py'):
            filter_file('#!/usr/bin/python',
                        '#!/usr/bin/env {0}'.format(
                            os.path.basename(
                                self.spec['python'].command.path)),
                        pyfile)

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
