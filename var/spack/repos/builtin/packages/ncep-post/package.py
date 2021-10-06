# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NcepPost(CMakePackage):
    """The NCEP Post Processor is a software package designed
    to generate useful products from raw model output."""

    homepage = "https://github.com/NOAA-EMC/EMC_post"
    url      = "https://github.com/NOAA-EMC/EMC_post/archive/refs/tags/upp_v10.0.8.tar.gz"

    maintainers = ['t-brown']

    version('10.0.8', sha256='b3b27d03250450159a8261c499d57168bdd833790c1c80c854d081fe37aaab47')

    variant('wrf-io', default=True, description='Enable WRF I/O.')

    depends_on('bacio')
    depends_on('crtm')
    depends_on('g2')
    depends_on('g2tmpl')
    depends_on('gfsio')
    depends_on('ip')
    depends_on('jasper')
    depends_on('libpng')
    depends_on('mpi')
    depends_on('netcdf-c')
    depends_on('netcdf-fortran')
    depends_on('nemsio')
    depends_on('sfcio')
    depends_on('sigio')
    depends_on('sp')
    depends_on('w3emc')
    depends_on('w3nco')
    depends_on('w3nco')
    depends_on('wrf-io', when='+wrf-io')
    depends_on('zlib')

    patch('cmake_findnetcdf.patch')

    def cmake_args(self):
        args = []
        if '+wrf-io' in self.spec:
            args.append('-DBUILD_WITH_WRFIO:BOOL=ON')
        return args
