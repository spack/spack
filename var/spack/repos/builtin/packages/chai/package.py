# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Chai(CMakePackage):
    """Copy-hiding array interface for data migration between memory spaces"""

    homepage = "https://github.com/LLNL/CHAI"
    url      = "https://github.com/LLNL/CHAI.git"

    version('develop', branch='develop', submodules='True')
    version('master', branch='master', submodules='True')
    version('1.0', tag='v1.0', submodules='True')
    version('1.1.0', tag='v1.1.0', submodules='True')
    version('1.2.0', tag='v1.2.0', submodules='True')

    variant('cuda', default=False, description='Build with CUDA support')

    depends_on('umpire')
    depends_on('cmake@3.8:', type='build')

    depends_on('umpire+cuda', when="+cuda")
    depends_on('cuda', when='+cuda')
    depends_on('cmake@3.9:', type='build', when="+cuda")

    def cmake_args(self):
        spec = self.spec

        options = []

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=On',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])
        else:
            options.append('-DENABLE_CUDA=Off')

        options.append('-Dumpire_DIR:PATH='
                       + spec['umpire'].prefix + "/share/umpire/cmake")
        options.append('-DENABLE_TESTS=Off')
        options.append('-DENABLE_BENCHMARKS=Off')

        return options
