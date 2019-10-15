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

    version('7.5.1-10.1-x86_64', sha256='2c833f43c9147d9a25a20947a4c5a5f5c33b2443240fd767f63b330c482e68e0',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.1/cudnn-10.1-linux-x64-v7.5.1.10.tgz')
    version('7.5.1-10.1-ppc64le', sha256='a9e23bc83c970daec20874ccd1d8d80b648adf15440ecd0164818b330b1e2663',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.1/cudnn-10.1-linux-ppc64le-v7.5.1.10.tgz')
    version('7.5.1-10.0-x86_64', sha256='c0a4ec438920aa581dd567117b9c316745b4a451ac739b1e04939a3d8b229985',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.1/cudnn-10.0-linux-x64-v7.5.1.10.tgz')
    version('7.5.1-10.0-ppc64le', sha256='d9205718da5fbab85433476f9ff61fcf4b889d216d6eea26753bbc24d115dd70',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.1/cudnn-10.0-linux-ppc64le-v7.5.1.10.tgz')
    version('7.5.0-10.1-x86_64', sha256='c31697d6b71afe62838ad2e57da3c3c9419c4e9f5635d14b683ebe63f904fbc8',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.0/cudnn-10.1-linux-x64-v7.5.0.56.tgz')
    version('7.5.0-10.1-ppc64le', sha256='15415eb714ab86ab6c7531f2cac6474b5dafd989479b062776c670b190e43638',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.0/cudnn-10.1-linux-ppc64le-v7.5.0.56.tgz')
    version('7.5.0-10.0-x86_64', sha256='701097882cb745d4683bb7ff6c33b8a35c7c81be31bac78f05bad130e7e0b781',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.0/cudnn-10.0-linux-x64-v7.5.0.56.tgz')
    version('7.5.0-10.0-ppc64le', sha256='f0c1cbd9de553c8e2a3893915bd5fff57b30e368ef4c964d783b6a877869e93a',
            url='https://developer.download.nvidia.com/compute/redist/cudnn/v7.5.0/cudnn-10.0-linux-ppc64le-v7.5.0.56.tgz')
    version('7.3.0', sha256='403f9043ff2c7b2c5967454872275d07bca11fd41dfc7b21995eadcad6dbe49b',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v7.3.0/cudnn-9.0-linux-x64-v7.3.0.29.tgz')
    version('7.2.1', sha256='cf007437b9ac6250ec63b89c25f248d2597fdd01369c80146567f78e75ce4e37',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v7.2.1/cudnn-9.0-linux-x64-v7.2.1.38.tgz')
    version('6.0', sha256='9b09110af48c9a4d7b6344eb4b3e344daa84987ed6177d5c44319732f3bb7f9c',
            url='http://developer.download.nvidia.com/compute/redist/cudnn/v6.0/cudnn-8.0-linux-x64-v6.0.tgz')
    version('5.1', sha256='c10719b36f2dd6e9ddc63e3189affaa1a94d7d027e63b71c3f64d449ab0645ce',
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
