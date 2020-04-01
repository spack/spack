# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Umpire(CMakePackage):
    """An application-focused API for memory management on NUMA & GPU
    architectures"""

    homepage = 'https://github.com/LLNL/Umpire'
    git      = 'https://github.com/LLNL/Umpire.git'

    version('develop', branch='develop', submodules='True')
    version('master', branch='master', submodules='True')
    version('2.1.0', tag='v2.1.0', submodules='True')
    version('2.0.0', tag='v2.0.0', submodules='True')
    version('1.1.0', tag='v1.1.0', submodules='True')
    version('1.0.1', tag='v1.0.1', submodules='True')
    version('1.0.0', tag='v1.0.0', submodules='True')
    version('0.3.5', tag='v0.3.5', submodules='True')
    version('0.3.4', tag='v0.3.4', submodules='True')
    version('0.3.3', tag='v0.3.3', submodules='True')
    version('0.3.2', tag='v0.3.2', submodules='True')
    version('0.3.1', tag='v0.3.1', submodules='True')
    version('0.3.0', tag='v0.3.0', submodules='True')
    version('0.2.4', tag='v0.2.4', submodules='True')
    version('0.2.3', tag='v0.2.3', submodules='True')
    version('0.2.2', tag='v0.2.2', submodules='True')
    version('0.2.1', tag='v0.2.1', submodules='True')
    version('0.2.0', tag='v0.2.0', submodules='True')
    version('0.1.4', tag='v0.1.4', submodules='True')
    version('0.1.3', tag='v0.1.3', submodules='True')

    variant('cuda', default=False, description='Build with CUDA support')
    variant('fortran', default=False, description='Build Fortran API')
    variant('c', default=True, description='Build C API')
    variant('numa', default=False, description='Enable NUMA support')

    depends_on('cuda', when='+cuda')
    depends_on('cmake@3.8:', type='build')
    depends_on('cmake@3.9:', when='+cuda', type='build')

    conflicts('+numa', when='@:0.3.2')
    conflicts('~c', when='+fortran', msg='Fortran API requires C API')

    def cmake_args(self):
        spec = self.spec

        options = []

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=On',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])
        else:
            options.append('-DENABLE_CUDA=Off')

        if '+c' in spec:
            options.append('-DENABLE_C=On')

        if '+fortran' in spec:
            options.append('-DENABLE_FORTRAN=On')

        if '+numa' in spec:
            options.append('-DENABLE_NUMA=On')

        return options
