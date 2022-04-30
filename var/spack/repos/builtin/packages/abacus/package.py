# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Abacus(MakefilePackage):
    """ABACUS (Atomic-orbital Based Ab-initio Computation at UStc)
    is an open-source computer code package aiming
    for large-scale electronic-structure simulations
    from first principles"""

    maintainers = ['bitllion']

    homepage = "http://abacus.ustc.edu.cn/"

    version(
        '2.2.1',
        '14feca1d8d1ce025d3f263b85ebfbebc1a1efff704b6490e95b07603c55c1d63',
        url='https://github.com/abacusmodeling/abacus-develop/archive/refs/tags/v2.2.1.tar.gz')
    version(
        '2.2.0',
        '09d4a2508d903121d29813a85791eeb3a905acbe1c5664b8a88903f8eda64b8f',
        url='https://github.com/abacusmodeling/abacus-develop/archive/refs/tags/v2.2.0.tar.gz')

    variant('mpi', default=True,
            description='Builds with MPI support. Requires MPI2+')
    variant('openmp', default=True,
            description='Enables OpenMP threads. Use threaded FFTW3')

    depends_on('elpa')
    depends_on('cereal')
    depends_on('libxc')
    depends_on('fftw')
    depends_on('mpi', when='+mpi', type=('build', 'link', 'run'))
    depends_on('mkl',)

    mkl_message = 'Need to set dependent variant to threads=openmp'

    conflicts('+openmp',
              when='^intel-oneapi-mkl',
              msg=mkl_message)

    build_directory = 'source'

    def edit(self, spec, prefix):
        if self.version == Version('2.2.1'):
            makefile_vars = FileFilter('source/Makefile.vars')
            makefile_vars.filter(
                '^\\s*LAPACK_DIR\\s*=.*',
                'LAPACK_DIR = ' +
                spec['mkl'].prefix)
            makefile_vars.filter(
                '^\\s*FFTW_DIR\\s*=.*',
                'FFTW_DIR = ' +
                spec['fftw'].prefix)
            makefile_vars.filter(
                '^\\s*LIBXC_DIR\\s*=.*',
                'LIBXC_DIR = ' +
                spec['libxc'].prefix)
            makefile_vars.filter(
                '^\\s*CEREAL_DIR\\s*=.*',
                'CEREAL_DIR = ' +
                spec['cereal'].prefix)
            makefile_vars.filter(
                '^\\s*ELPA_DIR\\s*=.*',
                'ELPA_DIR = ' +
                spec['elpa'].prefix)

            makefile_system = FileFilter('source/Makefile.system')
            makefile_system.filter(
                '^\\s*ELPA_INCLUDE_DIR\\s*=.*',
                'ELPA_INCLUDE_DIR = -I${ELPA_DIR}/include/' +
                'elpa_openmp-{0}'.format(
                    spec['elpa'].version))

            pwd = os.getcwd() + "/source"
            with open(pwd + '/Makefile.system', "r") as f:
                flist = f.readlines()
                flist[22] = 'ELPA_LIB     = -L${ELPA_LIB_DIR} -lelpa_openmp -Wl,-rpath=${ELPA_LIB_DIR}\n'
                flist[23] = '#ELPA_LIB     = -L${ELPA_LIB_DIR} -lelpa -Wl,-rpath=${ELPA_LIB_DIR}\n'
            with open(pwd + '/Makefile.system', "w") as f:
                f.writelines(flist)

        if self.version == Version('2.2.0'):
            makefile_vars = FileFilter('source/Makefile.vars')
            makefile_vars.filter(
                '^\\s*LAPACK_DIR\\s*=.*',
                'LAPACK_DIR = ' +
                spec['mkl'].prefix)
            makefile_vars.filter(
                '^\\s*FFTW_DIR\\s*=.*',
                'FFTW_DIR = ' +
                spec['fftw'].prefix)
            makefile_vars.filter(
                '^\\s*LIBXC_DIR\\s*=.*',
                'LIBXC_DIR = ' +
                spec['libxc'].prefix)
            makefile_vars.filter(
                '^\\s*CEREAL_DIR\\s*=.*',
                'CEREAL_DIR = ' +
                spec['cereal'].prefix)
            makefile_vars.filter(
                '^\\s*ELPA_DIR\\s*=.*',
                'ELPA_DIR = ' +
                spec['elpa'].prefix)
            makefile_vars.filter(
                '^\\s*ELPA_INCLUDE\\s*=.*',
                'ELPA_INCLUDE = -I${ELPA_DIR}/include/' +
                'elpa_openmp-{0}'.format(
                    spec['elpa'].version))

            pwd = os.getcwd() + "/source"
            with open(pwd + '/Makefile.system', "r") as f:
                flist = f.readlines()
                flist[25] = 'ELPA_LIB     = -L${ELPA_LIB_DIR} -lelpa_openmp -Wl,-rpath=${ELPA_LIB_DIR}\n'
                flist[26] = '#ELPA_LIB     = -L${ELPA_LIB_DIR} -lelpa -Wl,-rpath=${ELPA_LIB_DIR}\n'
            with open(pwd + '/Makefile.system', "w") as f:
                f.writelines(flist)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
