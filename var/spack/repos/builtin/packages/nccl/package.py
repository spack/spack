# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nccl(MakefilePackage):
    """Optimized primitives for collective multi-GPU communication."""

    homepage = "https://github.com/NVIDIA/nccl"
    url      = "https://github.com/NVIDIA/nccl/archive/v2.4.8-1.tar.gz"

    version('2.4.8-1', sha256='e2260da448ebbebe437f74768a346d28c74eabdb92e372a3dc6652a626318924')
    version('2.4.6-1', sha256='ea4421061a7b9c454f2e088f68bfdbbcefab80ce81cafc70ee6c7742b1439591')
    version('2.4.2-1', sha256='e3dd04b22eb541394bd818e5f78ac23a09cc549690d5d55d6fccc1a36155385a')
    version('2.3.7-1', sha256='e6eff80d9d2db13c61f8452e1400ca2f098d2dfe42857cb23413ce081c5b9e9b')
    version('2.3.5-5', sha256='bac9950b4d3980c25baa8e3e4541d2dfb4d21edf32ad3b89022d04920357142f')
    version('1.3.4-1', '5b9ce7fbdce0fde68e0f66318e6ff422')
    version('1.3.0-1', 'f6fb1d56913a7d212ca0c300e76f01fb')

    depends_on('cuda')

    # https://github.com/NVIDIA/nccl/issues/244
    patch('so_reuseport.patch', when='@2.3.7-1:2.4.8-1')

    @property
    def build_targets(self):
        return ['CUDA_HOME={0}'.format(self.spec['cuda'].prefix)]

    @property
    def install_targets(self):
        if self.version >= Version('2.3.5-5'):
            return ['PREFIX={0}'.format(self.prefix), 'src.install']
        else:
            return ['PREFIX={0}'.format(self.prefix), 'install']
