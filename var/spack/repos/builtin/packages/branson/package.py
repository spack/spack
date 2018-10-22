# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Branson(CMakePackage):
    """Branson's purpose is to study different algorithms for parallel Monte
    Carlo transport. Currently it contains particle passing and mesh passing
    methods for domain decomposition."""

    homepage = "https://github.com/lanl/branson"
    url      = "https://github.com/lanl/branson/archive/1.01.zip"
    git      = "https://github.com/lanl/branson.git"

    tags = ['proxy-app']

    version('develop', branch='develop')
    version('1.01', 'cf7095a887a8dd7d417267615bd0452a')

    depends_on('mpi@2:')
    depends_on('boost')
    depends_on('metis')
    depends_on('parmetis')

    root_cmakelists_dir = 'src'

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append('-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc)
        args.append('-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx)
        args.append('-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc)
        return args

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.doc)
        install('spack-build/BRANSON', prefix.bin)
        install('LICENSE.txt', prefix.doc)
        install('README.md', prefix.doc)
