# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nccl(MakefilePackage):
    """Optimized primitives for collective multi-GPU communication."""

    homepage = "https://github.com/NVIDIA/nccl"
    url      = "https://github.com/NVIDIA/nccl/archive/v1.3.4-1.tar.gz"

    version('1.3.4-1', '5b9ce7fbdce0fde68e0f66318e6ff422')
    version('1.3.0-1', 'f6fb1d56913a7d212ca0c300e76f01fb')

    depends_on('cuda')

    @property
    def build_targets(self):
        return ['CUDA_HOME={0}'.format(self.spec['cuda'].prefix)]

    @property
    def install_targets(self):
        return ['PREFIX={0}'.format(self.prefix), 'install']
