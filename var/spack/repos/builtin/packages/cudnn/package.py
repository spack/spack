# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Cudnn(Package):
    """NVIDIA cuDNN is a GPU-accelerated library of primitives for deep
    neural networks"""

    homepage = "https://developer.nvidia.com/cudnn"

    version('7.5.1-10.1-x86_64', '24017f4a56159d48fd5a31c8a930167b',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.1/cudnn-10.1-linux-x64-v7.5.1.10.tgz')
    version('7.5.1-10.1-ppc64le', 'ec0993be21e0998fc12116e4c46bce02',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.1/cudnn-10.1-linux-ppc64le-v7.5.1.10.tgz')
    version('7.5.1-10.0-x86_64', '703ed4be4d242ff4bc0ca48aaf2029bc',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.1/cudnn-10.0-linux-x64-v7.5.1.10.tgz')
    version('7.5.1-10.0-ppc64le', '8348cbab01970b75836d945d8a75915e',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.1/cudnn-10.0-linux-ppc64le-v7.5.1.10.tgz')
    version('7.5.0-10.1-x86_64', '4edc7fcfeada9f2363e97f9875154e8f',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.0/cudnn-10.1-linux-x64-v7.5.0.56.tgz')
    version('7.5.0-10.1-ppc64le', 'b927bc91d93182cb2606e51c9eeee908',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.0/cudnn-10.1-linux-ppc64le-v7.5.0.56.tgz')
    version('7.5.0-10.0-x86_64', 'b05ca261ffee1e08b496bf8a57790ee8',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.0/cudnn-10.0-linux-x64-v7.5.0.56.tgz')
    version('7.5.0-10.0-ppc64le', 'e9d2fcdb5340df2408fa08026a2a3e1c',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.0/cudnn-10.0-linux-ppc64le-v7.5.0.56.tgz')
    version('7.3.0', '72666d3532850752612706601258a0b2',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v7.3.0/cudnn-9.0-linux-x64-v7.3.0.29.tgz')
    version('7.2.1', '17e010153a4a95bf9c2df2a3c3ceea63',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v7.2.1/cudnn-9.0-linux-x64-v7.2.1.38.tgz')
    version('6.0', 'a08ca487f88774e39eb6b0ef6507451d',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v6.0/cudnn-8.0-linux-x64-v6.0.tgz')
    version('5.1', '406f4ac7f7ee8aa9e41304c143461a69',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v5.1/cudnn-8.0-linux-x64-v5.1.tgz')

    depends_on('cuda@8:', when='@5.1:@7')
    depends_on('cuda@9:', when='@7.2:@7.4')
    depends_on('cuda@10:', when='@7.5.0-10.0-ppc64le,7.5.0-10.0-x86_64,7.5.1-10.0-ppc64le,7.5.1-10.0-x86_64')
    depends_on('cuda@10.1:', when='@7.5.0-10.1-ppc64le,7.5.0-10.1-x86_64,7.5.1-10.1-ppc64le,7.5.1-10.1-x86_64')

    def install(self, spec, prefix):
        install_tree('.', prefix)

        if 'target=ppc64le: platform=linux' in spec:
            symlink(os.path.join(prefix, 'targets', 'ppc64le-linux', 'lib'),
                    prefix.lib)
            symlink(
                os.path.join(prefix, 'targets', 'ppc64le-linux', 'include'),
                prefix.include)
