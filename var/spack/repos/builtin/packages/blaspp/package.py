# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Blaspp(CMakePackage):
    """BLAS++: C++ API for the Basic Linear Algebra Subroutines (University of
    Texas)."""

    homepage = "https://bitbucket.org/icl/blaspp"
    hg       = "https://bitbucket.org/icl/blaspp"
    maintainers = ['teonnik', 'Sely85']

    version('develop', hg=hg, revision="5191c9d")

    variant('gfort',
            default=False,
            description=('Use GNU Fortran interface. '
                         'Default is Intel interface. (MKL)'))
    variant('ilp64',
            default=False,
            description=('Use 64bit integer interface. '
                         'Default is 32bit. (MKL & ESSL)'))
    variant('openmp',
            default=False,
            description=('Use OpenMP threaded backend. '
                         'Default is sequential. (MKL & ESSL)'))

    depends_on('blas')

    # 1) The CMake options exposed by `blaspp` allow for a value called `auto`.
    #    The value is not needed here as the choice of dependency in the spec
    #    determines the appropriate flags.
    #
    # 2) BLASFinder.cmake handles most options. For `auto`, it searches all
    #    blas libraries listed in `def_lib_list`.
    #
    # 3) ?? Custom blas library can be supplied via `BLAS_LIBRARIES`.
    #
    def cmake_args(self):
        spec = self.spec
        args = ['-DBLASPP_BUILD_TESTS:BOOL={0}'.format(
            'ON' if self.run_tests else 'OFF')]

        if '+gfort' in spec:
            args.append('-DBLAS_LIBRARY_MKL="GNU gfortran conventions"')
        else:
            args.append('-DBLAS_LIBRARY_MKL="Intel ifort conventions"')

        if '+ilp64' in spec:
            args.append('-DBLAS_LIBRARY_INTEGER="int64_t (ILP64)"')
        else:
            args.append('-DBLAS_LIBRARY_INTEGER="int (LP64)"')

        if '+openmp' in spec:
            args.append(['-DUSE_OPENMP=ON',
                         '-DBLAS_LIBRARY_THREADING="threaded"'])
        else:
            args.append('-DBLAS_LIBRARY_THREADING="sequential"')

        # Missing:
        #
        # - acml  : BLAS_LIBRARY="AMD ACML"
        #           BLAS_LIBRARY_THREADING= threaded/sequential
        #
        # - apple : BLAS_LIBRARY="Apple Accelerate" (veclibfort ???)
        #
        if '^mkl' in spec:
            args.append('-DBLAS_LIBRARY="Intel MKL"')
        elif '^essl' in spec:
            args.append('-DBLAS_LIBRARY="IBM ESSL"')
        elif '^openblas' in spec:
            args.append('-DBLAS_LIBRARY="OpenBLAS"')
        elif '^cray-libsci' in spec:
            args.append('-DBLAS_LIBRARY="Cray LibSci"')
        else:  # e.g. netlib-lapack
            args.append('-DBLAS_LIBRARY="generic"')

        return args
