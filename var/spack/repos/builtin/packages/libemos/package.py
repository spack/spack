# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libemos(CMakePackage):
    """The Interpolation library (EMOSLIB) includes Interpolation software and
       BUFR & CREX encoding/decoding routines."""

    homepage = "https://software.ecmwf.int/wiki/display/EMOS/Emoslib"
    url      = "https://software.ecmwf.int/wiki/download/attachments/3473472/libemos-4.4.2-Source.tar.gz"
    list_url = "https://software.ecmwf.int/wiki/display/EMOS/Releases"

    version('4.5.1', 'eec1ef4de841df3c68c08fa94d7939ff')
    version('4.5.0', '0ad8962a73e3ca90a8094561adc81276')
    version('4.4.9', '24d098cd062d443a544fe17727726285')
    version('4.4.7', '395dcf21cf06872f772fb6b73d8e67b9')
    version('4.4.2', 'f15a9aff0f40861f3f046c9088197376')

    variant('grib', default='eccodes', values=('eccodes', 'grib-api'),
            description='Specify GRIB backend')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'Production'))

    depends_on('eccodes', when='grib=eccodes')
    depends_on('grib-api', when='grib=grib-api')
    depends_on('fftw+float+double')
    depends_on('cmake@2.8.11:', type='build')
    depends_on('pkgconfig', type='build')

    conflicts('grib=eccodes', when='@:4.4.1',
              msg='Eccodes is supported starting version 4.4.2')

    def cmake_args(self):
        args = []

        if self.spec.variants['grib'].value == 'eccodes':
            args.append('-DENABLE_ECCODES=ON')
        else:
            if self.spec.satisfies('@4.4.2:'):
                args.append('-DENABLE_ECCODES=OFF')

        # To support long pathnames that spack generates
        args.append('-DCMAKE_Fortran_FLAGS=-ffree-line-length-none')

        return args
