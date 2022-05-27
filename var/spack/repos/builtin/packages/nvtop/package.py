# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nvtop(CMakePackage, CudaPackage):
    """Nvtop stands for Neat Videocard TOP, a (h)top like task monitor
    for AMD and NVIDIA GPUS. It can handle multiple GPUs and print
    information about them in a htop familiar way"""

    homepage = "https://github.com/Syllo/nvtop"
    url      = "https://github.com/Syllo/nvtop/archive/refs/tags/2.0.1.zip"

    maintainers = ['marcost2']

    version('2.0.1', sha256='ef18ce85d632eb1c22d3a3653976b2c088260039702df39fd0181f7cd3ae277d')
    version('2.0.0', sha256='1651f34274c334a682f280dcb2f28d9642d44c7b22afe8c431cab91345b50f31')
    version('1.2.2', sha256='543cbfdae3241fab1ea022402734c12e69d5988583193adaab69fdfae6e14c84')
    version('1.2.1', sha256='197992cdd0e2e151fce91a7ba56f717e4d85b317c396001e8dbd84dc2ba363cd')

    variant('support', values=('nvidia', 'amd'), default='nvidia,amd', multi=True,
            description='Which GPU vendors to build support for')

    depends_on('ncurses')
    depends_on('libdrm', when='support=amd')

    def cmake_args(self):
        return [self.define('NVIDIA_SUPPORT', self.spec.satisfies('support=nvidia')),
                self.define('AMDGPU_SUPPORT', self.spec.satisfies('support=amd'))]
