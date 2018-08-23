##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
    version('0.3.2', sha256='e8ba64f6b103c511ae13736100347deb7121ba9b41ba82052b1a018a65c0cb15')
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

    variant('cpu_target', default='',
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

    # virtual dependency
    provides('blas')
    provides('lapack')

    patch('make.patch', when='@0.2.16:')
    #  This patch is in a pull request to OpenBLAS that has not been handled
    #  https://github.com/xianyi/OpenBLAS/pull/915
    #  UPD: the patch has been merged starting version 0.2.20
    patch('openblas_icc.patch', when='@:0.2.19%intel')
    patch('openblas_icc_openmp.patch', when='@:0.2.20%intel@16.0:')
    patch('openblas_icc_fortran.patch', when='%intel@16.0:')
    patch('openblas_icc_fortran2.patch', when='%intel@18.0:')

    # Fixes compilation error on POWER8 with GCC 7
    # https://github.com/xianyi/OpenBLAS/pull/1098
    patch('power8.patch', when='@0.2.18:0.2.19 %gcc@7.1.0: target=ppc64')

    # Change file comments to work around clang 3.9 assembler bug
    # https://github.com/xianyi/OpenBLAS/pull/982
    patch('openblas0.2.19.diff', when='@0.2.19')

    parallel = False

    conflicts('%intel@16', when='@0.2.15:0.2.19')

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
            'MAKE_NO_J=1'
        ]

        if self.spec.variants['virtual_machine'].value:
            make_defs += [
                'DYNAMIC_ARCH=1',
                'NO_AVX2=1'
            ]

        if self.spec.variants['cpu_target'].value:
            make_defs += [
                'TARGET={0}'.format(self.spec.variants['cpu_target'].value)
            ]
        # invoke make with the correct TARGET for aarch64
        elif 'aarch64' in spack.architecture.sys_type():
            make_defs += [
                'TARGET=PILEDRIVER',
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

        return make_defs

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
        make('tests', *self.make_defs)

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
