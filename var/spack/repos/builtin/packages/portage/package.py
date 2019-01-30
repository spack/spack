# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Portage(CMakePackage):
    """Portage is a framework that computational physics applications can use
       to build a highly customized, hybrid parallel (MPI+X) conservative
       remapping library for transfer of field data between meshes.
    """
    homepage = "http://portage.lanl.gov/"
    git      = "https://github.com/laristra/portage.git"

    # tarballs don't have submodules, so use git tags
    version('develop', branch='master', submodules=True)
    version('1.1.1', tag='v1.1.1', submodules=True)
    version('1.1.0', tag='v1.1.0', submodules=True)

    variant('mpi', default=True, description='Support MPI')

    depends_on("cmake@3.1:", type='build')
    depends_on('mpi', when='+mpi')
    depends_on('lapack')

    def cmake_args(self):
        options = ['-DENABLE_UNIT_TESTS=ON', '-DENABLE_APP_TESTS=ON']

        if '+mpi' in self.spec:
            options.extend([
                '-DENABLE_MPI=ON',
                '-DENABLE_MPI_CXX_BINDINGS=ON',
                '-DCMAKE_CXX_COMPILER=%s' % self.spec['mpi'].mpicxx,
                '-DCMAKE_C_COMPILER=%s' % self.spec['mpi'].mpicc,
            ])
        else:
            options.append('-DENABLE_MPI=OFF')

        return options
