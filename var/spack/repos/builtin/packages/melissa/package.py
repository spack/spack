# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Melissa(CMakePackage):
    """
    Melissa is a file avoiding, adaptive, fault tolerant and elastic framework,
    to run large scale sensitivity analysis on supercomputers.
    """

    homepage = "https://github.com/melissa-sa/melissa"
    url      = "https://github.com/melissa-sa/melissa/archive/V1.0.tar.gz"

    maintainers = ['christoph-conrads', 'raffino']

    version('develop', branch='develop', git='git@gitlab.inria.fr:melissa/melissa.git')

    variant('no_mpi_api', default=False, description="Enable the deprecated no-MPI API")
    variant('shared', default=True, description="Build shared libraries")

    depends_on('cmake@3.7.2:', type='build')
    depends_on('libzmq')
    depends_on('mpi')
    depends_on('pkgconfig', type='build')
    depends_on('py-numpy')

    def cmake_args(self):
        args = [
            self.define('BUILD_TESTING', self.run_tests),
            self.define_from_variant('CMAKE_BUILD_TYPE', 'build_type'),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('MELISSA_ENABLE_NO_MPI_API', 'no_mpi_api')
        ]

        return args
