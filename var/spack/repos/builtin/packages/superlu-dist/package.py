# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SuperluDist(CMakePackage, CudaPackage, ROCmPackage):
    """A general purpose library for the direct solution of large, sparse,
    nonsymmetric systems of linear equations on high performance machines."""

    homepage = "https://crd-legacy.lbl.gov/~xiaoye/SuperLU/"
    url      = "https://github.com/xiaoyeli/superlu_dist/archive/v6.0.0.tar.gz"
    git      = "https://github.com/xiaoyeli/superlu_dist.git"

    tags = ['e4s']

    maintainers = ['xiaoye', 'gchavez2', 'balay', 'pghysels', 'liuyangzhuan']

    version('develop', branch='master')
    version('amd', branch='amd')
    version('7.2.0', sha256='20b60bd8a3d88031c9ce6511ae9700b7a8dcf12e2fd704e74b1af762b3468b8c')
    version('7.1.1', sha256='558053b3d4a56eb661c4f04d4fcab6604018ce5db97115394c161b56c9c278ff')
    version('7.1.0', sha256='edbea877562be95fb22c7de1ff484f18685bec4baa8e4f703c414d3c035d4a66')
    version('6.4.0', sha256='cb9c0b2ba4c28e5ed5817718ba19ae1dd63ccd30bc44c8b8252b54f5f04a44cc')
    version('6.3.1', sha256='3787c2755acd6aadbb4d9029138c293a7570a2ed228806676edcc7e1d3f5a1d3')
    version('6.3.0', sha256='daf3264706caccae2b8fd5a572e40275f1e128fa235cb7c21ee2f8051c11af95')
    version('6.2.0', sha256='15ad1badd81b41e37941dd124d06d3b92e51c4f0ff532ad23fb09c4ebfe6eb9e')
    version('6.1.1', sha256='35d25cff592c724439870444ed45e1d1d15ca2c65f02ccd4b83a6d3c9d220bd1')
    version('6.1.0', sha256='92c6d1424dd830ee2d1e7396a418a5f6645160aea8472e558c4e4bfe006593c4')
    version('6.0.0', sha256='ff6cdfa0263d595708bbb6d11fb780915d8cfddab438db651e246ea292f37ee4')
    version('5.4.0', sha256='3ac238fe082106a2c4dbaf0c22af1ff1247308ffa8f053de9d78c3ec7dd0d801')
    version('5.3.0', sha256='49ed110bdef1e284a0181d6c7dd1fae3aa110cb45f67c6aa5cb791070304d670')
    version('5.2.2', sha256='65cfb9ace9a81f7affac4ad92b9571badf0f10155b3468531b0fffde3bd8e727')
    version('5.2.1', sha256='67cf3c46cbded4cee68e2a9d601c30ab13b08091c8cdad95b0a8e018b6d5d1f1')
    version('5.1.3', sha256='58e3dfdb4ae6f8e3f6f3d5ee5e851af59b967c4483cdb3b15ccd1dbdf38f44f9')
    version('5.1.2', sha256='e34865ad6696ee6a6d178b4a01c8e19103a7d241ba9de043603970d63b0ee1e2')
    version('5.1.0', sha256='73f292ab748b590b6dd7469e6986aeb95d279b8b8b3da511c695a396bdbc996c')
    version('5.0.0', sha256='78d1d6460ff16b3f71e4bcd7306397574d54d421249553ccc26567f00a10bfc6')

    variant('int64', default=False, description='Build with 64 bit integers')
    variant('openmp', default=False, description='Build with OpenMP support (needs a good multithreaded BLAS implementation for good performance)')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('parmetis')
    depends_on('metis@5:')
    depends_on('cmake@3.18.1:', type='build', when='@7.1.0:')
    depends_on('hipblas', when='+rocm')
    depends_on('rocsolver', when='+rocm')

    conflicts('+rocm', when='+cuda')
    conflicts('+cuda', when='@:6.3')
    # See https://github.com/xiaoyeli/superlu_dist/issues/87
    conflicts('^cuda@11.5.0:', when='@7.1.0:7.1 +cuda')

    patch('xl-611.patch', when='@:6.1.1 %xl')
    patch('xl-611.patch', when='@:6.1.1 %xl_r')
    patch('superlu-cray-ftn-case.patch', when='@7.1.1 %cce')
    patch('CMAKE_INSTALL_LIBDIR.patch', when='@7.0.0:7.2.0')

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        def append_define(*args):
            cmake_args.append(CMakePackage.define(*args))

        def append_from_variant(*args):
            cmake_args.append(self.define_from_variant(*args))

        append_define('CMAKE_C_COMPILER', spec['mpi'].mpicc)
        append_define('CMAKE_CXX_COMPILER', spec['mpi'].mpicxx)
        append_define('CMAKE_INSTALL_LIBDIR:STRING', self.prefix.lib)
        append_define('CMAKE_INSTALL_BINDIR:STRING', self.prefix.bin)
        append_define('TPL_BLAS_LIBRARIES', spec['blas'].libs)
        append_define('TPL_LAPACK_LIBRARIES', spec['lapack'].libs)
        append_define('USE_XSDK_DEFAULTS', True)
        append_define('TPL_PARMETIS_LIBRARIES', [
            spec['parmetis'].libs.ld_flags,
            spec['metis'].libs.ld_flags
        ])
        append_define('TPL_PARMETIS_INCLUDE_DIRS', [
            spec['parmetis'].prefix.include,
            spec['metis'].prefix.include
        ])

        if ((spec.satisfies('%xl') or spec.satisfies('%xl_r'))
                and spec.satisfies('@:6.1.1')):
            append_define('CMAKE_C_FLAGS', '-DNoChange')

        append_define('XSDK_INDEX_SIZE', '64' if '+int64' in spec else '32')

        append_from_variant('enable_openmp', 'openmp')
        if '~openmp' in spec:
            append_define('CMAKE_DISABLE_FIND_PACKAGE_OpenMP', True)

        if '+cuda' in spec:
            append_define('TPL_ENABLE_CUDALIB', True)
            append_define(
                'TPL_CUDA_LIBRARIES',
                '-L%s -lcublas -lcudart' % spec['cuda'].libs.directories[0]
            )
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch[0] != 'none':
                append_define('CMAKE_CUDA_FLAGS', '-arch=sm_' + cuda_arch[0])

        if '+rocm' in spec and spec.satisfies('@amd'):
            append_define('TPL_ENABLE_HIPLIB', True)
            append_define('HIP_ROOT_DIR', spec['hip'].prefix)
            rocm_archs = spec.variants['amdgpu_target'].value
            if 'none' not in rocm_archs:
                append_define('HIP_HIPCC_FLAGS',
                              '--amdgpu-target=' + ",".join(rocm_archs))

        append_from_variant('BUILD_SHARED_LIBS', 'shared')
        return cmake_args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        if name == 'cflags' and '%pgi' not in self.spec:
            flags.append('-std=c99')
        return (None, None, flags)

    examples_src_dir = 'EXAMPLE'
    mk_hdr = 'make.inc'
    mk_hdr_in = mk_hdr + '.in'

    @run_after('install')
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([self.examples_src_dir, self.mk_hdr])

    def test(self):
        mk_file = join_path(self.install_test_root, self.mk_hdr)
        # Replace 'SRC' with 'lib' in the library's path
        filter_file(r'^(DSUPERLULIB.+)SRC(.+)', '\\1lib\\2', mk_file)
        # Set library flags for all libraries superlu-dist depends on
        filter_file(r'^LIBS.+\+=.+', '', mk_file)
        filter_file(r'^LIBS[^\+]+=.+', 'LIBS = $(DSUPERLULIB)' +
                    ' {0}'.format(self.spec['blas'].libs.ld_flags) +
                    ' {0}'.format(self.spec['lapack'].libs.ld_flags) +
                    ' {0}'.format(self.spec['parmetis'].libs.ld_flags) +
                    ' {0}'.format(self.spec['metis'].libs.ld_flags) +
                    ' $(CUDALIBS)',
                    mk_file)
        cuda_lib_opts = ''
        if '+cuda' in self.spec:
            cuda_lib_opts = ',-rpath,{0}'.format(
                            self.spec['cuda'].libs.directories[0])
        # Set the rpath for all the libs
        filter_file(r'^LOADOPTS.+', 'LOADOPTS = -Wl' +
                    ',-rpath,{0}'.format(self.prefix.lib) +
                    ',-rpath,{0}'.format(self.spec['blas'].prefix.lib) +
                    ',-rpath,{0}'.format(self.spec['lapack'].prefix.lib) +
                    ',-rpath,{0}'.format(self.spec['parmetis'].prefix.lib) +
                    ',-rpath,{0}'.format(self.spec['metis'].prefix.lib) +
                    cuda_lib_opts,
                    mk_file)

        test_dir = join_path(self.install_test_root, self.examples_src_dir)
        test_exe = 'pddrive'
        with working_dir(test_dir, create=False):
            make(test_exe)
            # Smoke test input parameters: -r 2 -c 2 g20.rua
            test_args = ['-n', '4', test_exe, '-r', '2', '-c', '2', 'g20.rua']
            # Find the correct mpirun command
            mpiexe_f = which('srun', 'mpirun', 'mpiexec')
            if mpiexe_f:
                self.run_test(mpiexe_f.command, test_args, work_dir='.',
                              purpose='superlu-dist smoke test')
            make('clean')
