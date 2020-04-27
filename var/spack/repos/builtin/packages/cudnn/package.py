# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Cudnn(Package):
    """NVIDIA cuDNN is a GPU-accelerated library of primitives for deep
    neural networks"""

    homepage = "https://developer.nvidia.com/cudnn"

    # Latest versions available at:
    #     https://developer.nvidia.com/rdp/cudnn-download
    # Archived versions available at:
    #     https://developer.nvidia.com/rdp/cudnn-archive
    # Note that download links don't work from command line,
    # need to use modified URLs like in url_for_version.

    maintainers = ['adamjstewart']

    # cuDNN 7.6.5
    version('7.6.5.32-10.2-linux-x64',
            sha256='600267f2caaed2fd58eb214ba669d8ea35f396a7d19b94822e6b36f9f7088c20',
            preferred=True)
    version('7.6.5.32-10.1-linux-x64',
            sha256='7eaec8039a2c30ab0bc758d303588767693def6bf49b22485a2c00bf2e136cb3')
    version('7.6.5.32-10.1-osx-x64',
            sha256='8ecce28a5ed388a2b9b2d239e08d7c550f53b79288e6d9e5eb4c152bfc711aff')
    version('7.6.5.32-10.1-linux-ppc64le',
            sha256='97b2faf73eedfc128f2f5762784d21467a95b2d5ba719825419c058f427cbf56')

    version('7.6.5.32-10.0-linux-x64',
            sha256='28355e395f0b2b93ac2c83b61360b35ba6cd0377e44e78be197b6b61b4b492ba')
    version('7.6.5.32-10.0-osx-x64',
            sha256='6fa0b819374da49102e285ecf7fcb8879df4d0b3cc430cc8b781cdeb41009b47')
    version('7.6.5.32-10.0-linux-ppc64le',
            sha256='b1717f4570083bbfc6b8b59f280bae4e4197cc1cb50e9d873c05adf670084c5b')

    version('7.6.5.32-9.2-linux-x64',
            sha256='a2a2c7a8ba7b16d323b651766ee37dcfdbc2b50d920f73f8fde85005424960e4')
    version('7.6.5.32-9.2-linux-ppc64le',
            sha256='a11f44f9a827b7e69f527a9d260f1637694ff7c1674a3e46bd9ec054a08f9a76')

    version('7.6.5.32-9.0-linux-x64',
            sha256='bd0a4c0090d5b02feec3f195738968690cc2470b9bc6026e6fe8ff245cd261c8')

    # cuDNN 7.6.4
    version('7.6.4.38-10.1-linux-x64',
            sha256='32091d115c0373027418620a09ebec3658a6bc467d011de7cdd0eb07d644b099')
    version('7.6.4.38-10.1-osx-x64',
            sha256='bfced062c3689ced2c1fb49c7d5052e6bc3da6974c1eb707e4dcf8cd209d4236')
    version('7.6.4.38-10.1-linux-ppc64le',
            sha256='f3615fea50986a4dfd05d7a0cf83396dfdceefa9c209e8bf9691e20a48e420ce')

    version('7.6.4.38-10.0-linux-x64',
            sha256='417bb5daf51377037eb2f5c87649000ca1b9cec0acb16cfe07cb1d3e9a961dbf')
    version('7.6.4.38-10.0-osx-x64',
            sha256='af01ab841caec25087776a6b8fc7782883da12e590e24825ad1031f9ae0ed4b1')
    version('7.6.4.38-10.0-linux-ppc64le',
            sha256='c1725ad6bd7d7741e080a1e6da4b62eac027a94ac55c606cce261e3f829400bb')

    version('7.6.4.38-9.2-linux-x64',
            sha256='c79156531e641289b6a6952888b9637059ef30defd43c3cf82acf38d67f60a27')
    version('7.6.4.38-9.2-linux-ppc64le',
            sha256='98d8aae2dcd851558397a9a30b73242f257e1556be17c83650e63a0685969884')

    version('7.6.4.38-9.0-linux-x64',
            sha256='8db78c3623c192d4f03f3087b41c32cb0baac95e13408b5d9dabe626cb4aab5d')

    # cuDNN 7.6.3
    version('7.6.3.30-10.1-linux-x64',
            sha256='352557346d8111e2f954c494be1a90207103d316b8777c33e62b3a7f7b708961')
    version('7.6.3.30-10.1-linux-ppc64le',
            sha256='f274735a8fc31923d3623b1c3d2b1d0d35bb176687077c6a4d4353c6b900d8ee')

    # cuDNN 7.5.1
    version('7.5.1.10-10.1-linux-x64',
            sha256='2c833f43c9147d9a25a20947a4c5a5f5c33b2443240fd767f63b330c482e68e0')
    version('7.5.1.10-10.1-linux-ppc64le',
            sha256='a9e23bc83c970daec20874ccd1d8d80b648adf15440ecd0164818b330b1e2663')

    version('7.5.1.10-10.0-linux-x64',
            sha256='c0a4ec438920aa581dd567117b9c316745b4a451ac739b1e04939a3d8b229985')
    version('7.5.1.10-10.0-linux-ppc64le',
            sha256='d9205718da5fbab85433476f9ff61fcf4b889d216d6eea26753bbc24d115dd70')

    # cuDNN 7.5.0
    version('7.5.0.56-10.1-linux-x64',
            sha256='c31697d6b71afe62838ad2e57da3c3c9419c4e9f5635d14b683ebe63f904fbc8')
    version('7.5.0.56-10.1-linux-ppc64le',
            sha256='15415eb714ab86ab6c7531f2cac6474b5dafd989479b062776c670b190e43638')

    version('7.5.0.56-10.0-linux-x64',
            sha256='701097882cb745d4683bb7ff6c33b8a35c7c81be31bac78f05bad130e7e0b781')
    version('7.5.0.56-10.0-linux-ppc64le',
            sha256='f0c1cbd9de553c8e2a3893915bd5fff57b30e368ef4c964d783b6a877869e93a')

    # cuDNN 7.3.0
    version('7.3.0.29-9.0-linux-x64',
            sha256='403f9043ff2c7b2c5967454872275d07bca11fd41dfc7b21995eadcad6dbe49b')

    # cuDNN 7.2.1
    version('7.2.1.38-9.0-linux-x64',
            sha256='cf007437b9ac6250ec63b89c25f248d2597fdd01369c80146567f78e75ce4e37')

    # cuDNN 7.1.3
    version('7.1.3-9.1-linux-x64',
            sha256='dd616d3794167ceb923d706bf73e8d6acdda770751492b921ee6827cdf190228')
    version('7.1.3-9.1-linux-ppc64le',
            sha256='e3b4837f711b98a52faacc872a68b332c833917ef3cf87c0108f1d01af9b2931')

    # cuDNN 6.0
    version('6.0-8.0-linux-x64',
            sha256='9b09110af48c9a4d7b6344eb4b3e344daa84987ed6177d5c44319732f3bb7f9c')

    # cuDNN 5.1
    version('5.1-8.0-linux-x64',
            sha256='c10719b36f2dd6e9ddc63e3189affaa1a94d7d027e63b71c3f64d449ab0645ce')

    # CUDA 10.2
    depends_on('cuda@10.2.0:10.2.999', when='@7.6.5.32-10.2-linux-x64')

    # CUDA 10.1
    depends_on('cuda@10.1.0:10.1.999', when='@7.6.5.32-10.1-osx-x64')
    depends_on('cuda@10.1.0:10.1.999', when='@7.6.5.32-10.1-linux-x64')
    depends_on('cuda@10.1.0:10.1.999', when='@7.6.5.32-10.1-linux-ppc64le')
    depends_on('cuda@10.1.0:10.1.999', when='@7.6.4.38-10.1-osx-x64')
    depends_on('cuda@10.1.0:10.1.999', when='@7.6.4.38-10.1-linux-x64')
    depends_on('cuda@10.1.0:10.1.999', when='@7.6.4.38-10.1-linux-ppc64le')
    depends_on('cuda@10.1.0:10.1.999', when='@7.6.3.30-10.1-linux-x64')
    depends_on('cuda@10.1.0:10.1.999', when='@7.6.3.30-10.1-linux-ppc64le')
    depends_on('cuda@10.1.0:10.1.999', when='@7.5.0.56-10.1-linux-x64')
    depends_on('cuda@10.1.0:10.1.999', when='@7.5.0.56-10.1-linux-ppc64le')

    # CUDA 10.0
    depends_on('cuda@10.0.0:10.0.999', when='@7.6.5.32-10.0-osx-x64')
    depends_on('cuda@10.0.0:10.0.999', when='@7.6.5.32-10.0-linux-x64')
    depends_on('cuda@10.0.0:10.0.999', when='@7.6.5.32-10.0-linux-ppc64le')
    depends_on('cuda@10.0.0:10.0.999', when='@7.6.4.38-10.0-osx-x64')
    depends_on('cuda@10.0.0:10.0.999', when='@7.6.4.38-10.0-linux-x64')
    depends_on('cuda@10.0.0:10.0.999', when='@7.6.4.38-10.0-linux-ppc64le')
    depends_on('cuda@10.0.0:10.0.999', when='@7.5.1.10-10.0-linux-x64')
    depends_on('cuda@10.0.0:10.0.999', when='@7.5.1.10-10.0-linux-ppc64le')
    depends_on('cuda@10.0.0:10.0.999', when='@7.5.0.56-10.0-linux-x64')
    depends_on('cuda@10.0.0:10.0.999', when='@7.5.0.56-10.0-linux-ppc64le')

    # CUDA 9.2
    depends_on('cuda@9.2.0:9.2.999', when='@7.6.5.32-9.2-linux-x64')
    depends_on('cuda@9.2.0:9.2.999', when='@7.6.5.32-9.2-linux-ppc64le')
    depends_on('cuda@9.2.0:9.2.999', when='@7.6.4.38-9.2-linux-x64')
    depends_on('cuda@9.2.0:9.2.999', when='@7.6.4.38-9.2-linux-ppc64le')

    # CUDA 9.1
    depends_on('cuda@9.1.0:9.1.999', when='@7.1.3-9.1-linux-x64')
    depends_on('cuda@9.1.0:9.1.999', when='@7.1.3-9.1-linux-ppc64le')

    # CUDA 9.0
    depends_on('cuda@9.0.0:9.0.999', when='@7.6.5.32-9.0-linux-x64')
    depends_on('cuda@9.0.0:9.0.999', when='@7.6.4.38-9.0-linux-x64')
    depends_on('cuda@9.0.0:9.0.999', when='@7.3.0.29-9.0-linux-x64')
    depends_on('cuda@9.0.0:9.0.999', when='@7.2.1.38-9.0-linux-x64')

    # CUDA 8.0
    depends_on('cuda@8.0.0:8.0.999', when='@6.0-8.0-linux-x64')
    depends_on('cuda@8.0.0:8.0.999', when='@5.1-8.0-linux-x64')

    def url_for_version(self, version):
        url = 'https://developer.download.nvidia.com/compute/redist/cudnn/v{0}/cudnn-{1}-v{2}.tgz'

        if version >= Version('7.2'):
            directory = version[:3]
            ver = version[:4]
            cuda = version[4:]
        elif version >= Version('7.1'):
            directory = version[:3]
            ver = version[:2]
            cuda = version[3:]
        elif version >= Version('7.0'):
            directory = version[:3]
            ver = version[0]
            cuda = version[3:]
        else:
            directory = version[:2]
            ver = version[:2]
            cuda = version[2:]

        return url.format(directory, cuda, ver)

    def setup_run_environment(self, env):
        if 'target=ppc64le: platform=linux' in self.spec:
            env.set('cuDNN_ROOT', os.path.join(
                self.prefix, 'targets', 'ppc64le-linux'))

    def install(self, spec, prefix):
        install_tree('.', prefix)

        if 'target=ppc64le: platform=linux' in spec:
            symlink(os.path.join(prefix, 'targets', 'ppc64le-linux', 'lib'),
                    prefix.lib)
            symlink(
                os.path.join(prefix, 'targets', 'ppc64le-linux', 'include'),
                prefix.include)
