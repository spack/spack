# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Costa(CMakePackage):
    """
    Distributed Communication-Optimal Matrix Transpose and Reshuffle Library
    Based on the paper: https://arxiv.org/abs/2106.06601
    """

    maintainers = ['haampie', 'kabicm']
    homepage = 'https://github.com/eth-cscs/COSTA'
    url = 'https://github.com/eth-cscs/COSTA/releases/download/v2.0/COSTA-v2.0.tar.gz'
    git = 'https://github.com/eth-cscs/COSTA.git'

    # note: The default archives produced with github do not have the archives
    #       of the submodules.
    version('master', branch='master', submodules=True)
    version('2.0', sha256='ef283b904b1b77b7d0de401cbdc3d7850c77368f2b57249c6eaee3017794c4b8')

    variant('scalapack', default=False, description='Build with ScaLAPACK API')
    variant('openmp', default=True, description="Build with OpenMP support")

    depends_on('cmake@3.12:', type='build')
    depends_on('mpi@3:')
    # depends_on('openmp', when="+openmp")
    depends_on('scalapack', when='+scalapack')

    def url_for_version(self, version):
        return 'https://github.com/eth-cscs/COSTA/releases/download/v{0}/COSTA-v{1}.tar.gz'.format(version, version)

    def setup_build_environment(self, env):
        return

    def costa_scalapack_cmake_arg(self):
        spec = self.spec

        if '~scalapack' in spec:
            return 'OFF'
        elif '^intel-mkl' in spec or '^intel-oneapi-mkl' in spec:
            return 'MKL'
        elif '^cray-libsci' in spec:
            return 'CRAY_LIBSCI'

        return 'CUSTOM'

    def cmake_args(self):
        return [
            self.define('COSTA_WITH_BENCHMARKS', 'OFF'),
            self.define('COSTA_WITH_APPS', 'OFF'),
            self.define('COSTA_WITH_TESTS', 'OFF'),
            self.define('COSTA_WITH_PROFILING', 'OFF'),
            self.define('COSTA_SCALAPACK', self.costa_scalapack_cmake_arg())
        ]
