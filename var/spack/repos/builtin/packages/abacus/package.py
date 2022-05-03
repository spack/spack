# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack import *


class Abacus(MakefilePackage):
    """ABACUS (Atomic-orbital Based Ab-initio Computation at UStc)
    is an open-source computer code package aiming
    for large-scale electronic-structure simulations
    from first principles"""

    maintainers = ['bitllion']

    homepage = "http://abacus.ustc.edu.cn/"
    git      = "https://github.com/abacusmodeling/abacus-develop.git"
    url      = "https://github.com/abacusmodeling/abacus-develop/archive/refs/tags/v2.2.1.tar.gz"

    version('develop', branch='develop')
    version('2.2.1', sha256='14feca1d8d1ce025d3f263b85ebfbebc1a1efff704b6490e95b07603c55c1d63')
    version('2.2.0', sha256='09d4a2508d903121d29813a85791eeb3a905acbe1c5664b8a88903f8eda64b8f')

    variant('mpi', default=True,
            description='Builds with MPI support. Requires MPI2+')
    variant('openmp', default=True,
            description='Enables OpenMP threads. Use threaded FFTW3')

    depends_on('elpa+openmp')
    depends_on('cereal')
    depends_on('libxc')
    depends_on('fftw')
    depends_on('mpi', when='+mpi', type=('build', 'link', 'run'))
    depends_on('mkl')

    mkl_message = 'Need to set dependent variant to threads=openmp'

    conflicts('+openmp', msg=mkl_message)

    build_directory = 'source'

    def edit(self, spec, prefix):
        # self.build_directory = os.getcwd() + "/source"

        tempInc = "\
FORTRAN = ifort\n\
CPLUSPLUS = icpc\n\
CPLUSPLUS_MPI = mpiicpc\n\
LAPACK_DIR = %s\n\
FFTW_DIR = %s\n\
ELPA_DIR = %s\n\
ELPA_INCLUDE = -I${ELPA_DIR}/include/elpa_openmp-%s\n\
CEREAL_DIR = %s\n\
OBJ_DIR = obj\n\
OBJ_DIR_serial = obj\n\
NP      = 14" % (spec['mkl'].prefix, spec['fftw'].prefix, spec['elpa'].prefix,
 '{0}'.format(spec['elpa'].version), spec['cereal'].prefix)
        # LIBXC_DIR     = /public/software/libxc-5.0.0
        # LIBTORCH_DIR  = /public/software/libtorch
        # LIBNPY_DIR    = /public/software/libnpy
        with open(self.build_directory + "/Makefile.vars", "w") as f:
            f.write(tempInc)

        tempSystem = "ELPA_LIB = -L${ELPA_LIB_DIR} -lelpa_openmp -Wl,\
-rpath=${ELPA_LIB_DIR}"
        lineList = []
        Pattern1 = re.compile('^ELPA_INCLUDE_DIR')
        Pattern2 = re.compile('^ELPA_LIB\\s*= ')
        with open(self.build_directory + '/Makefile.system', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                elif Pattern1.search(line):
                    pass
                elif Pattern2.search(line):
                    pass
                else:
                    lineList.append(line)
        with open(self.build_directory + '/Makefile.system', 'w') as f:
            for i in lineList:
                f.write(i)
        with open(self.build_directory + '/Makefile.system', 'a') as f:
            f.write(tempSystem)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
