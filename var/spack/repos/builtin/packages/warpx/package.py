# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Warpx(CMakePackage):
    """WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.
    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid OpenMP/MPI parallelization, advanced vectorization
    techniques and load balancing capabilities.

    For WarpX' Python bindings and PICMI input support, see the 'py-warpx' package.
    """

    homepage = "https://ecp-warpx.github.io"
    url      = "https://github.com/ECP-WarpX/WarpX/archive/refs/tags/21.04.tar.gz"
    git      = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers = ['ax3l', 'dpgrote', 'MaxThevenet', 'RemiLehe']

    # NOTE: if you update the versions here, also see py-warpx
    version('develop', branch='development')
    version('21.06', sha256='a26039dc4061da45e779dd5002467c67a533fc08d30841e01e7abb3a890fbe30')
    version('21.05', sha256='f835f0ae6c5702550d23191aa0bb0722f981abb1460410e3d8952bc3d945a9fc')
    version('21.04', sha256='51d2d8b4542eada96216e8b128c0545c4b7527addc2038efebe586c32c4020a0')

    variant('app', default=True,
            description='Build the WarpX executable application')
    variant('ascent', default=False,
            description='Enable Ascent in situ vis')
    variant('compute',
            default='omp',
            values=('omp', 'cuda', 'hip', 'sycl', 'noacc'),
            multi=False,
            description='On-node, accelerated computing backend')
    variant('dims',
            default='3',
            values=('2', '3', 'rz'),
            multi=False,
            description='Number of spatial dimensions')
    variant('eb', default=False,
            description='Embedded boundary support (in development)')
    variant('lib', default=True,
            description='Build WarpX as a shared library')
    variant('mpi', default=True,
            description='Enable MPI support')
    variant('mpithreadmultiple', default=True,
            description='MPI thread-multiple support, i.e. for async_io')
    variant('openpmd', default=True,
            description='Enable openPMD I/O')
    variant('precision',
            default='double',
            values=('single', 'double'),
            multi=False,
            description='Floating point precision (single/double)')
    variant('psatd', default=True,
            description='Enable PSATD solver support')
    variant('qed', default=True,
            description='Enable QED support')
    variant('qedtablegen', default=False,
            description='QED table generation support')
    variant('shared', default=True,
            description='Build a shared version of the library')
    variant('tprof', default=True,
            description='Enable tiny profiling features')

    depends_on('ascent', when='+ascent')
    # note: ~shared is only needed until the new concretizer is in and
    #       honors the conflict inside the Ascent package to find this
    #       automatically
    depends_on('ascent +cuda ~shared', when='+ascent compute=cuda')
    depends_on('ascent +mpi', when='+ascent +mpi')
    depends_on('blaspp', when='+psatd dims=rz')
    depends_on('blaspp +cuda', when='+psatd dims=rz compute=cuda')
    depends_on('boost@1.66.0: +math', when='+qedtablegen')
    depends_on('cmake@3.15.0:', type='build')
    depends_on('cuda@9.2.88:', when='compute=cuda')
    depends_on('fftw@3:', when='+psatd compute=omp')
    depends_on('fftw +mpi', when='+psatd +mpi compute=omp')
    depends_on('lapackpp', when='+psatd dims=rz')
    depends_on('mpi', when='+mpi')
    depends_on('openpmd-api@0.13.1:,dev', when='+openpmd')
    depends_on('openpmd-api ~mpi', when='+openpmd ~mpi')
    depends_on('openpmd-api +mpi', when='+openpmd +mpi')
    depends_on('pkgconfig', type='build', when='+psatd compute=omp')
    depends_on('rocfft', when='+psatd compute=hip')
    depends_on('rocprim', when='compute=hip')
    depends_on('rocrand', when='compute=hip')
    depends_on('llvm-openmp', when='%apple-clang compute=omp')

    conflicts('~qed +qedtablegen',
              msg='WarpX PICSAR QED table generation needs +qed')
    conflicts('compute=sycl', when='+psatd',
              msg='WarpX spectral solvers are not yet tested with SYCL '
                  '(use "warpx ~psatd")')

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            '-DCMAKE_INSTALL_LIBDIR=lib',
            # variants
            self.define_from_variant('WarpX_APP', 'app'),
            self.define_from_variant('WarpX_ASCENT', 'ascent'),
            '-DWarpX_COMPUTE={0}'.format(
                spec.variants['compute'].value.upper()),
            '-DWarpX_DIMS={0}'.format(
                spec.variants['dims'].value.upper()),
            self.define_from_variant('WarpX_EB', 'eb'),
            self.define_from_variant('WarpX_LIB', 'lib'),
            self.define_from_variant('WarpX_MPI', 'mpi'),
            self.define_from_variant('WarpX_MPI_THREAD_MULTIPLE', 'mpithreadmultiple'),
            self.define_from_variant('WarpX_OPENPMD', 'openpmd'),
            '-DWarpX_PRECISION={0}'.format(
                spec.variants['precision'].value.upper()),
            self.define_from_variant('WarpX_PSATD', 'psatd'),
            self.define_from_variant('WarpX_QED', 'qed'),
            self.define_from_variant('WarpX_QED_TABLE_GEN', 'qedtablegen'),
        ]

        return args

    @property
    def libs(self):
        libsuffix = {'2': '2d', '3': '3d', 'rz': 'rz'}
        dims = self.spec.variants['dims'].value
        return find_libraries(
            ['libwarpx.' + libsuffix[dims]], root=self.prefix, recursive=True,
            shared=True
        )
