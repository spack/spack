# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Warpx(CMakePackage):
    """WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.
    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid OpenMP/MPI parallelization, advanced vectorization
    techniques and load balancing capabilities.

    For WarpX' Python bindings and PICMI input support, see the 'py-warpx' package.
    """

    homepage = "https://ecp-warpx.github.io"
    url      = "https://github.com/ECP-WarpX/WarpX/archive/refs/tags/22.05.tar.gz"
    git      = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers = ['ax3l', 'dpgrote', 'MaxThevenet', 'RemiLehe']
    tags = ['e4s', 'ecp']

    # NOTE: if you update the versions here, also see py-warpx
    version('develop', branch='development')
    version('22.05', sha256='2fa69e6a4db36459b67bf663e8fbf56191f6c8c25dc76301dbd02a36f9b50479')
    version('22.04', sha256='9234d12e28b323cb250d3d2cefee0b36246bd8a1d1eb48e386f41977251c028f')
    version('22.03', sha256='ddbef760c8000f2f827dfb097ca3359e7aecbea8766bec5c3a91ee28d3641564')
    version('22.02', sha256='d74b593d6f396e037970c5fbe10c2e5d71d557a99c97d40e4255226bc6c26e42')
    version('22.01', sha256='e465ffadabb7dc360c63c4d3862dc08082b5b0e77923d3fb05570408748b0d28')
    # 22.01+ requires C++17 or newer
    version('21.12', sha256='847c98aac20c73d94c823378803c82be9a14139f1c14ea483757229b452ce4c1')
    version('21.11', sha256='ce60377771c732033a77351cd3500b24b5d14b54a5adc7a622767b9251c10d0b')
    version('21.10', sha256='d372c573f0360094d5982d64eceeb0149d6620eb75e8fdbfdc6777f3328fb454')
    version('21.09', sha256='861a65f11846541c803564db133c8678b9e8779e69902ef1637b21399d257eab')
    version('21.08', sha256='6128a32cfd075bc63d08eebea6d4f62d33ce0570f4fd72330a71023ceacccc86')
    version('21.07', sha256='a8740316d813c365715f7471201499905798b50bd94950d33f1bd91478d49561')
    version('21.06', sha256='a26039dc4061da45e779dd5002467c67a533fc08d30841e01e7abb3a890fbe30')
    version('21.05', sha256='f835f0ae6c5702550d23191aa0bb0722f981abb1460410e3d8952bc3d945a9fc')
    version('21.04', sha256='51d2d8b4542eada96216e8b128c0545c4b7527addc2038efebe586c32c4020a0')
    # 20.01+ requires C++14 or newer

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
            values=('1', '2', '3', 'rz'),
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
    depends_on('boost@1.66.0: +math', when='+qedtablegen')
    depends_on('cmake@3.15.0:', type='build')
    depends_on('cmake@3.18.0:', type='build', when='@22.01:')
    depends_on('mpi', when='+mpi')
    with when('compute=cuda'):
        depends_on('cuda@9.2.88:')
        depends_on('cuda@11.0:', when='@22.01:')
    with when('compute=hip'):
        depends_on('rocfft', when='+psatd')
        depends_on('rocprim')
        depends_on('rocrand')
    with when('compute=noacc'):
        with when('+psatd'):
            depends_on('fftw@3: ~mpi', when='~mpi')
            depends_on('fftw@3: +mpi', when='+mpi')
            depends_on('pkgconfig', type='build')
    with when('compute=omp'):
        depends_on('llvm-openmp', when='%apple-clang')
        with when('+psatd'):
            depends_on('fftw@3: +openmp')
            depends_on('fftw ~mpi', when='~mpi')
            depends_on('fftw +mpi', when='+mpi')
            depends_on('pkgconfig', type='build')
    with when('+psatd dims=rz'):
        depends_on('lapackpp')
        depends_on('blaspp')
        depends_on('blaspp +cuda', when='compute=cuda')
    with when('+openpmd'):
        depends_on('openpmd-api@0.13.1:')
        depends_on('openpmd-api@0.14.2:', when='@21.09:')
        depends_on('openpmd-api ~mpi', when='~mpi')
        depends_on('openpmd-api +mpi', when='+mpi')

    conflicts('dims=1', when='@:21.12',
              msg='WarpX 1D support starts in 22.01+')
    conflicts('~qed +qedtablegen',
              msg='WarpX PICSAR QED table generation needs +qed')
    conflicts('compute=sycl', when='+psatd',
              msg='WarpX spectral solvers are not yet tested with SYCL '
                  '(use "warpx ~psatd")')

    # The symbolic aliases for our +lib target were missing in the install
    # location
    # https://github.com/ECP-WarpX/WarpX/pull/2626
    patch('2626.patch', when='@21.12')

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

        with when('+openpmd'):
            args.append('-DWarpX_openpmd_internal=OFF')

        return args

    @property
    def libs(self):
        libsuffix = {'1': '1d', '2': '2d', '3': '3d', 'rz': 'rz'}
        dims = self.spec.variants['dims'].value
        return find_libraries(
            ['libwarpx.' + libsuffix[dims]], root=self.prefix, recursive=True,
            shared=True
        )

    # WarpX has many examples to serve as a suitable smoke check. One
    # that is typical was chosen here
    examples_src_dir = 'Examples/Physics_applications/laser_acceleration/'

    def _get_input_options(self, post_install):
        spec = self.spec
        examples_dir = join_path(
            self.install_test_root if post_install else self.stage.source_path,
            self.examples_src_dir)
        dims = spec.variants['dims'].value
        inputs_nD = {'1': 'inputs_1d', '2': 'inputs_2d', '3': 'inputs_3d',
                     'rz': 'inputs_rz'}
        if spec.satisfies('@:21.12'):
            inputs_nD['rz'] = 'inputs_2d_rz'
        inputs = join_path(examples_dir, inputs_nD[dims])

        cli_args = [inputs, "max_step=50", "diag1.intervals=10"]
        # test openPMD output if compiled in
        if '+openpmd' in spec:
            cli_args.append('diag1.format=openpmd')
            # RZ: New openPMD thetaMode output
            if dims == 'rz' and spec.satisfies('@22.04:'):
                cli_args.append('diag1.fields_to_plot=Er Et Ez Br Bt Bz jr jt jz rho')
        return cli_args

    def check(self):
        """Checks after the build phase"""
        if '+app' not in self.spec:
            print("WarpX check skipped: requires variant +app")
            return

        with working_dir("spack-check", create=True):
            cli_args = self._get_input_options(False)
            warpx = Executable(join_path(self.build_directory, 'bin/warpx'))
            warpx(*cli_args)

    @run_after('install')
    def copy_test_sources(self):
        """Copy the example input files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([self.examples_src_dir])

    def test(self):
        """Perform smoke tests on the installed package."""
        if '+app' not in self.spec:
            print("WarpX smoke tests skipped: requires variant +app")
            return

        # our executable names are a variant-dependent and naming evolves
        exe = find(self.prefix.bin, 'warpx.*', recursive=False)[0]

        cli_args = self._get_input_options(True)
        self.run_test(exe,
                      cli_args,
                      [], installed=True, purpose='Smoke test for WarpX',
                      skip_missing=False)
