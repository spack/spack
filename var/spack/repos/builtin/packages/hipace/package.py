# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hipace(CMakePackage):
    """Highly efficient Plasma Accelerator Emulation, quasistatic
    particle-in-cell code
    """

    homepage = "https://hipace.readthedocs.io"
    # url      = "https://github.com/Hi-PACE/hipace/archive/refs/tags/21.06.tar.gz"
    git      = "https://github.com/Hi-PACE/hipace.git"

    maintainers = ['ax3l', 'MaxThevenet', 'SeverinDiederichs']

    version('develop', branch='development')

    variant('compute',
            default='omp',
            values=('omp', 'cuda', 'hip', 'sycl', 'noacc'),
            multi=False,
            description='On-node, accelerated computing backend')
    variant('mpi', default=True,
            description='Enable MPI support')
    variant('openpmd', default=True,
            description='Enable openPMD I/O')
    variant('precision',
            default='double',
            values=('single', 'double'),
            multi=False,
            description='Floating point precision (single/double)')

    depends_on('cmake@3.15.0:', type='build')
    depends_on('cuda@9.2.88:', when='compute=cuda')
    depends_on('fftw@3:', when='compute=omp')
    depends_on('fftw +mpi', when='+mpi compute=omp')
    depends_on('mpi', when='+mpi')
    depends_on('openpmd-api@hipace', when='+openpmd')
    depends_on('openpmd-api ~mpi', when='+openpmd ~mpi')
    depends_on('openpmd-api +mpi', when='+openpmd +mpi')
    depends_on('pkgconfig', type='build', when='compute=omp')
    depends_on('rocfft', when='compute=hip')
    depends_on('rocprim', when='compute=hip')
    depends_on('rocrand', when='compute=hip')
    depends_on('llvm-openmp', when='%apple-clang compute=omp')

    def cmake_args(self):
        spec = self.spec

        args = [
            # do not super-build dependencies
            '-HiPACE_openpmd_internal=OFF',
            # variants
            '-DHiPACE_COMPUTE={0}'.format(
                spec.variants['compute'].value.upper()),
            self.define_from_variant('HiPACE_MPI', 'mpi'),
            self.define_from_variant('HiPACE_OPENPMD', 'openpmd'),
            '-DHiPACE_PRECISION={0}'.format(
                spec.variants['precision'].value.upper()),
        ]

        return args
