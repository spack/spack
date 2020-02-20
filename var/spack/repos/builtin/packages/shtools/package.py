# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Shtools(Package):
    """SHTOOLS - Spherical Harmonic Tools"""

    homepage = "https://shtools.github.io/SHTOOLS/"
    url      = "https://github.com/SHTOOLS/SHTOOLS/archive/v4.5.tar.gz"

    maintainers = ['eschnett']

    version('4.5', sha256='1975a2a2bcef8c527d321be08c13c2bc479e0d6b81c468a3203f95df59be4f89')

    # Note: This package also provides Python wrappers. We do not
    # install these properly yet, only the Fortran library is
    # installed.

    variant('openmp', default=True, description="Enable OpenMP support")

    depends_on('blas')
    depends_on('fftw')
    depends_on('lapack')

    def install(self, spec, prefix):
        # Options for the Makefile
        makeopts = [
            "F95=f90",
            "F95FLAGS=-fPIC -O3 -std=f2003 -ffast-math",
            "OPENMPFLAGS={0}".format(self.compiler.openmp_flag),
            "BLAS={0}".format(spec['blas'].libs),
            "FFTW={0}".format(spec['fftw'].libs),
            "LAPACK={0}".format(spec['lapack'].libs),
            "PREFIX={0}".format(prefix),
        ]

        target = 'fortran-mp' if spec.satisfies('+openmp') else 'fortran'
        make(target, *makeopts)

        make('install', *makeopts)
