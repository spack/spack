# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Melissa(CMakePackage):
    """Melissa is a file avoiding, adaptive, fault tolerant and elastic
    framework, to run large scale sensitivity analysis on supercomputers.
    """

    homepage = 'https://gitlab.inria.fr/melissa/melissa'
    git = 'https://gitlab.inria.fr/melissa/melissa.git'

    # attention: Git**Hub**.com accounts
    maintainers = ['christoph-conrads', 'raffino']

    version('master', branch='master')
    version('develop', branch='develop')

    variant('no_mpi_api', default=False, description="Enable the deprecated no-MPI API")
    variant('shared', default=True, description="Build shared libraries")

    depends_on('cmake@3.7.2:', type='build')
    depends_on('libzmq@4.1.5:')
    depends_on('mpi')
    depends_on('pkgconfig', type='build')
    depends_on('python@3.5.3:', type=('build', 'run'))

    def cmake_args(self):
        args = [
            self.define('BUILD_TESTING', self.run_tests),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('MELISSA_ENABLE_NO_MPI_API', 'no_mpi_api')
        ]

        return args
