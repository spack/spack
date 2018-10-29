# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cudnn(Package):
    """NVIDIA cuDNN is a GPU-accelerated library of primitives for deep
    neural networks"""

    homepage = "https://developer.nvidia.com/cudnn"

    version('7.3', '72666d3532850752612706601258a0b2',
            url='https://developer.nvidia.com/compute/machine-learning/cudnn/secure/v7.3.0/prod/9.0_2018920/cudnn-9.0-linux-x64-v7.3.0.29.tgz')
    version('6.0', 'a08ca487f88774e39eb6b0ef6507451d',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v6.0/cudnn-8.0-linux-x64-v6.0.tgz')
    version('5.1', '406f4ac7f7ee8aa9e41304c143461a69',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v5.1/cudnn-8.0-linux-x64-v5.1.tgz')

    depends_on('cuda@8:')

    def install(self, spec, prefix):
        install_tree('.', prefix)
