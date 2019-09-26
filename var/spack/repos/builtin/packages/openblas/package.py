# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.package_test import compare_output_file, compile_c_and_execute
import spack.architecture


class Openblas(MakefilePackage):
    """OpenBLAS: An optimized BLAS library"""

    homepage = 'http://www.openblas.net'
    url      = 'http://github.com/xianyi/OpenBLAS/archive/v0.2.19.tar.gz'
    git      = 'https://github.com/xianyi/OpenBLAS.git'

    version('develop', branch='develop')
    version('0.3.7', sha256='bde136122cef3dd6efe2de1c6f65c10955bbb0cc01a520c2342f5287c28f9379')
    version('0.3.6', sha256='e64c8fe083832ffbc1459ab6c72f71d53afd3b36e8497c922a15a06b72e9002f')
    version('0.3.5', sha256='0950c14bd77c90a6427e26210d6dab422271bc86f9fc69126725833ecdaa0e85')
    version('0.3.4', sha256='4b4b4453251e9edb5f57465bf2b3cf67b19d811d50c8588cdf2ea1f201bb834f')
    version('0.3.3', sha256='49d88f4494ae780e3d7fa51769c00d982d7cdb73e696054ac3baa81d42f13bab')
    version('0.3.2', sha256='e8ba64f6b103c511ae13736100347deb7121ba9b41ba82052b1a018a65c0cb15')
    version('0.3.1', sha256='1f5e956f35f3acdd3c74516e955d797a320c2e0135e31d838cbdb3ea94d0eb33')
    version('0.3.0',  '42cde2c1059a8a12227f1e6551c8dbd2')
    version('0.2.20', '48637eb29f5b492b91459175dcc574b1')
    version('0.2.19', '28c998054fd377279741c6f0b9ea7941')
    version('0.2.18', '805e7f660877d588ea7e3792cda2ee65')
    version('0.2.17', '664a12807f2a2a7cda4781e3ab2ae0e1')
    version('0.2.16', 'fef46ab92463bdbb1479dcec594ef6dc')
    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')

    variant(
        'shared',
        default=True,
        description='Build shared libraries as well as static libs.'
    )
    variant('ilp64', default=False, description='64 bit integers')
    variant('pic', default=True, description='Build position independent code')

    variant('cpu_target', default='auto',
            description='Set CPU target architecture (leave empty for '
                        'autodetection; GENERIC, SSE_GENERIC, NEHALEM, ...)')

    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('pthreads', 'openmp', 'none'),
        multi=False
    )

    variant(
        'virtual_machine',
        default=False,
        description="Adding options to build openblas on Linux virtual machine"
    )

    variant(
        'avx2',
        default=True,
        description='Enable use of AVX2 instructions'
    )

    variant(
        'avx512',
        default=False,
        description='Enable use of AVX512 instructions'
    )

    # virtual dependency
    provides('blas')
    provides('lapack')

    # OpenBLAS >=3.0 has an official way to disable internal parallel builds
    patch('make.patch', when='@0.2.16:0.2.20')
    #  This patch is in a pull request to OpenBLAS that has not been handled
    #  https://github.com/xianyi/OpenBLAS/pull/915
    #  UPD: the patch has been merged starting version 0.2.20
    patch('openblas_icc.patch', when='@:0.2.19%intel')
    patch('openblas_icc_openmp.patch', when='@:0.2.20%intel@16.0:')
    patch('openblas_icc_fortran.patch', when='%intel@16.0:')
    patch('openblas_icc_fortran2.patch', when='%intel@18.0:')

    # Fixes compilation error on POWER8 with GCC 7
    # https://github.com/xianyi/OpenBLAS/pull/1098
    patch('power8.patch', when='@0.2.18:0.2.19 %gcc@7.1.0: target=power8')

    # Change file comments to work around clang 3.9 assembler bug
    # https://github.com/xianyi/OpenBLAS/pull/982
    patch('openblas0.2.19.diff', when='@0.2.19')

    # Fix CMake export symbol error
    # https://github.com/xianyi/OpenBLAS/pull/1703
    patch('openblas-0.3.2-cmake.patch', when='@0.3.1:0.3.2')

    # Disable experimental TLS code that lead to many threading issues
    # https://github.com/xianyi/OpenBLAS/issues/1735#issuecomment-422954465
    # https://github.com/xianyi/OpenBLAS/issues/1761#issuecomment-421039174
    # https://github.com/xianyi/OpenBLAS/pull/1765
    patch('https://github.com/xianyi/OpenBLAS/commit/4d183e5567346f80f2ef97eb98f8601c47f8cb56.patch',
          sha256='714aea33692304a50bd0ccde42590c176c82ded4a8ac7f06e573dc8071929c33',
          when='@0.3.3')

    # Fix parallel build issues on filesystems
    # with missing sub-second timestamp resolution
    patch('https://github.com/xianyi/OpenBLAS/commit/79ea839b635d1fd84b6ce8a47e086f01d64198e6.patch',
          sha256='f1b066a4481a50678caeb7656bf3e6764f45619686ac465f257c8017a2dc1ff0',
          when='@0.3.0:0.3.3')

    # Add conditions to f_check to determine the Fujitsu compiler
    patch('openblas_fujitsu.patch', when='%fj')

    conflicts('%intel@16', when='@0.2.15:0.2.19')

    @property
    def parallel(self):
        # unclear whether setting `-j N` externally was supported before 0.3
        return self.spec.version >= Version('0.3.0')

    @run_before('edit')
    def check_compilers(self):
        # As of 06/2016 there is no mechanism to specify that packages which
        # depends on Blas/Lapack need C or/and Fortran symbols. For now
        # require both.
        if self.compiler.fc is None:
            raise InstallError(
                'OpenBLAS requires both C and Fortran compilers!'
            )

        # Add support for OpenMP
        if (self.spec.satisfies('threads=openmp') and
            self.spec.satisfies('%clang')):
            if str(self.spec.compiler.version).endswith('-apple'):
                raise InstallError("Apple's clang does not support OpenMP")
            if '@:0.2.19' in self.spec:
                # Openblas (as of 0.2.19) hardcoded that OpenMP cannot
                # be used with any (!) compiler named clang, bummer.
                raise InstallError(
                    'OpenBLAS @:0.2.19 does not support OpenMP with clang!'
                )

    @property
    def make_defs(self):
        # Configure fails to pick up fortran from FC=/abs/path/to/fc, but
        # works fine with FC=/abs/path/to/gfortran.
        # When mixing compilers make sure that
        # $SPACK_ROOT/lib/spack/env/<compiler> have symlinks with reasonable
        # names and hack them inside lib/spack/spack/compilers/<compiler>.py

        make_defs = [
            'CC={0}'.format(spack_cc),
            'FC={0}'.format(spack_fc),
        ]

        # force OpenBLAS to use externally defined parallel build
        if self.spec.version < Version('0.3'):
            make_defs.append('MAKE_NO_J=1')  # flag defined by our make.patch
        else:
            make_defs.append('MAKE_NB_JOBS=0')  # flag provided by OpenBLAS

        if self.spec.variants['virtual_machine'].value:
            make_defs += [
                'DYNAMIC_ARCH=1',
                'NUM_THREADS=64',  # OpenBLAS stores present no of CPUs as max
            ]

        if self.spec.variants['cpu_target'].value != 'auto':
            make_defs += [
                'TARGET={0}'.format(self.spec.variants['cpu_target'].value)
            ]
        # invoke make with the correct TARGET for aarch64
        elif 'aarch64' in spack.architecture.sys_type():
            make_defs += [
                'TARGET=ARMV8'
            ]
        if self.spec.satisfies('%gcc@:4.8.4'):
            make_defs += ['NO_AVX2=1']
        if '~shared' in self.spec:
            if '+pic' in self.spec:
                make_defs.extend([
                    'CFLAGS={0}'.format(self.compiler.pic_flag),
                    'FFLAGS={0}'.format(self.compiler.pic_flag)
                ])
            make_defs += ['NO_SHARED=1']
        # fix missing _dggsvd_ and _sggsvd_
        if self.spec.satisfies('@0.2.16'):
            make_defs += ['BUILD_LAPACK_DEPRECATED=1']

        # Add support for multithreading
        if self.spec.satisfies('threads=openmp'):
            make_defs += ['USE_OPENMP=1', 'USE_THREAD=1']
        elif self.spec.satisfies('threads=pthreads'):
            make_defs += ['USE_OPENMP=0', 'USE_THREAD=1']
        else:
            make_defs += ['USE_OPENMP=0', 'USE_THREAD=0']

        # 64bit ints
        if '+ilp64' in self.spec:
            make_defs += ['INTERFACE64=1']

        if self.spec.target.family == 'x86_64':
            if '~avx2' in self.spec:
                make_defs += ['NO_AVX2=1']
            if '~avx512' in self.spec:
                make_defs += ['NO_AVX512=1']

        return make_defs

    @property
    def headers(self):
        # As in netlib-lapack, the only public headers for cblas and lapacke in
        # openblas are cblas.h and lapacke.h. The remaining headers are private
        # headers either included in one of these two headers, or included in
        # one of the source files implementing functions declared in these
        # headers.
        return find_headers(['cblas', 'lapacke'], self.prefix.include)

    @property
    def build_targets(self):
        targets = ['libs', 'netlib']

        # Build shared if variant is set.
        if '+shared' in self.spec:
            targets += ['shared']

        return self.make_defs + targets

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        make('tests', *self.make_defs, parallel=False)

    @property
    def install_targets(self):
        make_args = [
            'install',
            'PREFIX={0}'.format(self.prefix),
        ]
        return make_args + self.make_defs

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        spec = self.spec
        # Openblas may pass its own test but still fail to compile Lapack
        # symbols. To make sure we get working Blas and Lapack, do a small
        # test.
        source_file = join_path(os.path.dirname(self.module.__file__),
                                'test_cblas_dgemm.c')
        blessed_file = join_path(os.path.dirname(self.module.__file__),
                                 'test_cblas_dgemm.output')

        include_flags = spec['openblas'].headers.cpp_flags
        link_flags = spec['openblas'].libs.ld_flags
        if self.compiler.name == 'intel':
            link_flags += ' -lifcore'
        if self.spec.satisfies('threads=pthreads'):
            link_flags += ' -lpthread'
        if spec.satisfies('threads=openmp'):
            link_flags += ' -lpthread ' + self.compiler.openmp_flag

        output = compile_c_and_execute(
            source_file, [include_flags], link_flags.split()
        )
        compare_output_file(output, blessed_file)
