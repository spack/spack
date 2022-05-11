# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Upp(CMakePackage):
    """
    The Unified Post Processor (UPP) software package is a software
    package designed to generate useful products from raw model
    output.
    """

    homepage = "https://github.com/NOAA-EMC/UPP"
    git = "https://github.com/NOAA-EMC/UPP.git"
    url = "https://github.com/NOAA-EMC/UPP/archive/refs/tags/upp_v10.0.10.tar.gz"

    maintainers = ['kgerheiser', 'edwardhartnett', 'Hang-Lei-NOAA']

    version('10.0.10', sha256='0c96a88d0e79b554d5fcee9401efcf4d6273da01d15e3413845274f73d70b66e')
    version('10.0.9', tag='upp_v10.0.9', submodules=True)

    variant('openmp', default=True)
    variant('postexec', default=True)
    variant('wrf-io', default=False)
    variant('docs', default=False)

    depends_on('mpi')
    depends_on('netcdf-fortran')
    depends_on('bacio')
    depends_on('crtm')
    depends_on('g2')
    depends_on('g2tmpl')
    depends_on('ip')

    depends_on('nemsio', when='+postexec')
    depends_on('sfcio', when='+postexec')
    depends_on('sigio', when='+postexec')
    depends_on('sp', when='+postexec')
    depends_on('w3nco', when='+postexec')
    depends_on('wrf-io', when='+wrf-io')
    depends_on('doxygen', when='+docs')

    def cmake_args(self):
        args = [
            self.define_from_variant('OPENMP', 'openmp'),
            self.define_from_variant('BUILD_POSTEXEC', 'postexec'),
            self.define_from_variant('BUILD_WITH_WRFIO', 'wrf-io'),
            self.define_from_variant('ENABLE_DOCS', 'docs')
        ]

        return args
