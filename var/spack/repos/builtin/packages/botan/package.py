# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Botan(MakefilePackage):
    """Crypto and TLS for Modern C++"""

    homepage = "https://botan.randombit.net/"
    url      = "https://botan.randombit.net/releases/Botan-2.13.0.tar.xz"

    maintainers = ['aumuell']

    version('2.19.1', sha256='e26e00cfefda64082afdd540d3c537924f645d6a674afed2cd171005deff5560')
    version('2.19.0', sha256='240d9e56e6acb91ef4cf06a8a1c6c0f101c61d40cf48cccf139faef821d7040b')
    version('2.18.2', sha256='541a3b13f1b9d30f977c6c1ae4c7bfdfda763cda6e44de807369dce79f42307e')
    version('2.18.1', sha256='f8c7b46222a857168a754a5cc329bb780504122b270018dda5304c98db28ae29')
    version('2.18.0', sha256='cc64852e1e0c5bb30ecd052e4a12d5136125a8ce5c3be2efb6fb061c8677e327')
    version('2.17.3', sha256='79123b654445a4abba486e09a431788545c708237382a3e765664c9f55b03b88')
    version('2.17.2', sha256='ebe27dfe2b55d7e02bf520e926606c48b76b22facb483256b13ab38e018e1e6c')
    version('2.17.1', sha256='741358b3f1638ed7d9b2f59b4e344aa46f4966b15958b5434c0ac1580df0c0c1')
    version('2.17.0', sha256='b97044b312aa718349af7851331b064bc7bd5352400d5f80793bace427d01343')
    version('2.16.0', sha256='92ed6ebc918d86bd1b04221ca518af4cf29cc326c4760740bd2d22e61cea2628')
    version('2.15.0', sha256='d88af1307f1fefac79aa4f2f524699478d69ce15a857cf2d0a90ac6bf2a50009')
    version('2.14.0', sha256='0c10f12b424a40ee19bde00292098e201d7498535c062d8d5b586d07861a54b5')
    version('2.13.0', sha256='f57ae42a41e1091bca58f44f41addebd9a390b651603952c881ec89d50187e90')
    version('2.12.1', sha256='7e035f142a51fca1359705792627a282456d49749bf62a37a8e48375d41baaa9')
    version('2.12.0', sha256='1eaefd459d52f27de1805cff8c68792e0610919648ee98e101980e94edb90a63')
    version('2.11.0', sha256='f7874da2aeb8c018fd77df40b2137879bf90b66f5589490c991e83fb3e8094be')

    variant('doc', default=False, description='Build documentation')

    depends_on('python', type='build')
    depends_on('py-sphinx@1.2:', type='build', when='+doc')

    def edit(self, spec, prefix):
        configure = Executable('./configure.py')
        configure(*self.configure_args())

    def configure_args(self):
        spec = self.spec
        args = ['--prefix={0}'.format(self.prefix)]
        if '+doc' in spec:
            args.append('--with-documentation')
        else:
            args.append('--without-documentation')
        return args
