# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Care(CMakePackage, CudaPackage, HipPackage):
    """
    Algorithms for chai managed arrays.
    """

    homepage = "https://github.com/LLNL/CARE"
    git      = "https://github.com/LLNL/CARE.git"

    version('develop', branch='develop', submodules='True')
    version('master', branch='main', submodules='True')
    version('0.3.0', tag='v0.3.0', submodules='True')
    version('0.2.0', tag='v0.2.0', submodules='True')

    variant('openmp', default=False, description='Build Shared Libs')
    variant('implicit_conversions', default=True, description='Enable implicit'
            'conversions to/from raw pointers')
    variant('benchmarks', default=True, description='Build benchmarks.')
    variant('examples', default=True, description='Build examples.')
    variant('docs', default=False, description='Build documentation')
    # TODO: figure out gtest dependency and then set this default True
    # and remove the +tests conflict below.
    variant('tests', default=False, description='Build tests')

    depends_on('blt', type='build')
    depends_on('blt@0.3.7:', type='build', when='+hip')

    depends_on('camp')
    depends_on('umpire@develop')
    depends_on('raja@develop')
    depends_on('chai@develop+enable_pick~benchmarks')

    # WARNING: this package currently only supports an internal cub
    # package. This will cause a race condition if compiled with another
    # package that uses cub. TODO: have all packages point to the same external
    # cub package.
    depends_on('camp+cuda', when='+cuda')
    depends_on('umpire+cuda', when='+cuda')
    depends_on('raja+cuda~openmp', when='+cuda')
    depends_on('chai+cuda', when='+cuda')

    # variants +hip and amdgpu_targets are not automatically passed to
    # dependencies, so do it manually.
    amdgpu_targets = HipPackage.amd_gputargets_list()
    depends_on('camp+hip', when='+hip')
    depends_on('umpire+hip', when='+hip')
    depends_on('raja+hip~openmp', when='+hip')
    depends_on('chai+hip', when='+hip')
    for val in amdgpu_targets:
        depends_on('camp amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)
        depends_on('umpire amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)
        depends_on('raja amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)
        depends_on('chai amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)

    conflicts('+openmp', when='+hip')
    conflicts('+openmp', when='+cuda')
    # TODO: figure out gtest dependency and then remove this.
    conflicts('+tests')

    def cmake_args(self):
        spec = self.spec

        options = []
        options.append('-DBLT_SOURCE_DIR={0}'.format(spec['blt'].prefix))

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=ON',
                '-DCUDA_TOOLKIT_ROOT_DIR=' + spec['cuda'].prefix])

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch[0]))
                flag = '-arch sm_{0}'.format(cuda_arch[0])
                options.append('-DCMAKE_CUDA_FLAGS:STRING={0}'.format(flag))
        else:
            options.append('-DENABLE_CUDA=OFF')

        if '+hip' in spec:
            arch = self.spec.variants['amdgpu_target'].value
            options.extend([
                '-DENABLE_HIP=ON',
                '-DHIP_ROOT_DIR={0}'.format(spec['hip'].prefix),
                '-DHIP_HIPCC_FLAGS=--amdgpu-target={0}'.format(arch)])
        else:
            options.append('-DENABLE_HIP=OFF')

        options.append('-DCARE_ENABLE_IMPLICIT_CONVERSIONS={0}'.format(
            'ON' if '+implicit_conversions' in spec else 'OFF'))

        options.append('-DCAMP_DIR:PATH='
                       + spec['camp'].prefix.share.camp.cmake)
        options.append('-DUMPIRE_DIR:PATH='
                       + spec['umpire'].prefix.share.umpire.cmake)
        options.append('-DRAJA_DIR:PATH='
                       + spec['raja'].prefix.share.raja.cmake)
        options.append('-DCHAI_DIR:PATH='
                       + spec['chai'].prefix.share.chai.cmake)

        options.append('-DCARE_ENABLE_TESTS={0}'.format(
            'ON' if '+tests' in spec else 'OFF'))

        # There are both CARE_ENABLE_* and ENABLE_* variables in here because
        # one controls the BLT infrastructure and the other controls the CARE
        # infrastructure. The goal is to just be able to use the CARE_ENABLE_*
        # variables, but CARE isn't set up correctly for that yet.
        options.append('-DENABLE_BENCHMARKS={0}'.format(
            'ON' if '+benchmarks' in spec else 'OFF'))
        options.append('-DCARE_ENABLE_BENCHMARKS={0}'.format(
            'ON' if '+benchmarks' in spec else 'OFF'))

        options.append('-DENABLE_EXAMPLES={0}'.format(
            'ON' if '+examples' in spec else 'OFF'))
        options.append('-DCARE_ENABLE_EXAMPLES={0}'.format(
            'ON' if '+examples' in spec else 'OFF'))

        options.append('-DENABLE_DOCS={0}'.format(
            'ON' if '+docs' in spec else 'OFF'))
        options.append('-DCARE_ENABLE_DOCS={0}'.format(
            'ON' if '+docs' in spec else 'OFF'))

        return options
