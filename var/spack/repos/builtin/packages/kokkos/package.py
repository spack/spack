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
from spack import *


class Kokkos(Package):
    """Kokkos implements a programming model in C++ for writing performance
    portable applications targeting all major HPC platforms."""

    homepage = "https://github.com/kokkos/kokkos"
    url      = "https://github.com/kokkos/kokkos/archive/2.03.00.tar.gz"

    version('2.7.00',  'b357f9374c1008754babb4495f95e392')
    version('2.5.00',  '2db83c56587cb83b772d0c81a3228a21')
    version('2.04.11', 'd4849cee6eb9001d61c30f1d9fe74336')
    version('2.04.04', '2c6d1c2569b91c9fcd4117296438e65c')
    version('2.04.00', 'd99ac790ff5f29545d8eb53de90c0a85')
    version('2.03.13', '3874a159a517384541ea5b52f85501ba')
    version('2.03.05', '8727d783453f719eec392e10a36b49fd')
    version('2.03.00', 'f205d659d4304747759fabfba32d43c3')
    version('2.02.15', 'de41e38f452a50bb03363c519fe20769')
    version('2.02.07', 'd5baeea70109249f7dca763074ffb202')
    version('develop', git='https://github.com/kokkos/kokkos',
            branch='develop')

    variant('serial', default=True, description="enable Serial backend (default)")
    variant('qthreads', default=False, description="enable Qthreads backend")
    variant('cuda', default=False, description="enable Cuda backend")
    variant('openmp', default=False, description="enable OpenMP backend")

    # Kokkos options
    variant('aggressive_vectorization', default=False,
            description="set aggressive_vectorization Kokkos option")
    variant('disable_profiling', default=False,
            description="set disable_profiling Kokkos option")
    variant('disable_dualview_modify_check', default=False,
            description="set disable_dualview_modify_check Kokkos option")
    variant('enable_profile_load_print', default=False,
            description="set enable_profile_load_print Kokkos option")
    variant('compiler_warnings', default=False,
            description="set compiler_warnings Kokkos option")
    variant('disable_deprecated_code', default=False,
            description="set disable_deprecated_code Kokkos option")
    variant('enable_eti', default=False,
            description="set enable_eti Kokkos option")

    # CUDA options
    variant('force_uvm', default=False,
            description="set force_uvm Kokkos CUDA option")
    variant('use_ldg', default=False,
            description="set use_ldg Kokkos CUDA option")
    variant('rdc', default=False,
            description="set rdc Kokkos CUDA option")
    variant('enable_lambda', default=False,
            description="set enable_lambda Kokkos CUDA option")

    gpu_values = ('Kepler30', 'Kepler32', 'Kepler35', 'Kepler37',
                  'Maxwell50', 'Maxwell52', 'Maxwell53',
                  'Pascal60', 'Pascal61')

    cuda_options = ('force_uvm', 'use_ldg', 'rdc', 'enable_lambda')

    # Host architecture variant
    variant(
        'host_arch',
        default=None,
        values=('AMDAVX', 'ARMv80', 'ARMv81', 'ARMv8-ThunderX',
                'Power7', 'Power8', 'Power9',
                'WSM', 'SNB', 'HSW', 'BDW', 'SKX', 'KNC', 'KNL'),
        description='Set the host architecture to use'
    )

    # GPU architecture variant
    variant(
        'gpu_arch',
        default=None,
        values=gpu_values,
        description='Set the GPU architecture to use'
    )

    # Checks on Kokkos version and Kokkos options
    conflicts('+aggressive_vectorization', when='@0:2.0.99',)
    conflicts('+disable_profiling', when='@0:2.0.99',)
    conflicts('+disable_dualview_modify_check', when='@0:2.03.04',)
    conflicts('+enable_profile_load_print', when='@0:2.03.04',)
    conflicts('+compiler_warnings', when='@0:2.03.14',)
    conflicts('+disable_deprecated_code', when='@0:2.5.99',)
    conflicts('+enable_eti', when='@0:2.6.99',)

    # Check that we haven't specified a gpu architecture
    # without specifying CUDA
    for p in gpu_values:
        conflicts('gpu_arch={0}'.format(p), when='~cuda',
            msg='Must specify CUDA backend to use a GPU architecture.')

    # Check that we haven't specified a Kokkos CUDA option
    # witout specifying CUDA
    conflicts('+force_uvm', when='~cuda',
        msg='Must enable CUDA to use force_uvm.')
    conflicts('+use_ldg', when='~cuda',
        msg='Must enable CUDA to use use_ldg.')
    conflicts('+rdc', when='~cuda',
        msg='Must enable CUDA to use rdc.')
    conflicts('+enable_lambda', when='~cuda',
        msg='Must enable CUDA to use enable_lambda.')

    # conflicts on kokkos version and cuda enabled
    # see kokkos issue #1296
    # https://github.com/kokkos/kokkos/issues/1296
    conflicts('+cuda', when='@2.5.00:develop',
        msg='Kokkos build system has issue when CUDA enabled'
        ' in version 2.5.00 through 2.7.00, and develop until '
        'issue #1296 is resolved.')

    # Specify that v1.x is required as v2.x has API changes
    depends_on('hwloc@:1')
    depends_on('qthreads', when='+qthreads')
    depends_on('cuda', when='+cuda')

    def install(self, spec, prefix):
        generate = which(join_path(self.stage.source_path,
                                   'generate_makefile.bash'))
        with working_dir('build', create=True):
            g_args = [
                '--prefix=%s' % prefix,
                '--with-hwloc=%s' % spec['hwloc'].prefix,
            ]
            arch_args = []
            kokkos_options_args = []
            cuda_options_args = []

            # Backends
            if 'serial' in spec:
                g_args.append('--with-serial')
            if '+openmp' in spec:
                g_args.append('--with-openmp')
            if 'qthreads' in spec:
                g_args.append('--with-qthreads=%s' % spec['qthreads'].prefix)
            if 'cuda' in spec:
                g_args.append('--with-cuda=%s' % spec['cuda'].prefix)
            # Host architectures
            host_arch = spec.variants['host_arch'].value
            # GPU architectures
            gpu_arch  = spec.variants['gpu_arch'].value
            if host_arch:
                arch_args.append(host_arch)
            if gpu_arch:
                arch_args.append(gpu_arch)
            # Combined architecture flags
            if arch_args:
                g_args.append('--arch={0}'.format(','.join(arch_args)))

            # CUDA options
            if '+force_uvm' in spec:
                cuda_options_args.append('force_uvm')
            if '+use_ldg' in spec:
                cuda_options_args.append('use_ldg')
            if '+rdc' in spec:
                cuda_options_args.append('rdc')
            if '+enable_lambda' in spec:
                cuda_options_args.append('enable_lambda')
            if cuda_options_args:
                g_args.append('--with-cuda-options={0}'
                              .format(','.join(cuda_options_args)))

            # Kokkos options
            if '+aggressive_vectorization' in spec:
                kokkos_options_args.append('aggressive_vectorization')
            if '+disable_profiling' in spec:
                kokkos_options_args.append('disable_profiling')
            if '+disable_dualview_modify_check' in spec:
                kokkos_options_args.append('disable_dualview_modify_check')
            if '+enable_profile_load_print' in spec:
                kokkos_options_args.append('enable_profile_load_print')
            if '+compiler_warnings' in spec:
                kokkos_options_args.append('compiler_warnings')
            if '+disable_deprecated_code' in spec:
                kokkos_options_args.append('disable_deprecated_code')
            if '+enable_eti' in spec:
                kokkos_options_args.append('enable_eti')
            if kokkos_options_args:
                g_args.append('--with-options={0}'
                              .format(','.join(kokkos_options_args)))

            generate(*g_args)
            make()
            make('install')
