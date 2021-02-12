# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Axel(AutotoolsPackage):
    """Axel is a light command line download accelerator for Linux and Unix"""

    homepage = "https://github.com/axel-download-accelerator/axel"
    url      = "https://github.com/axel-download-accelerator/axel/archive/v2.16.1.tar.gz"

    version('2.17.10', sha256='75af1d30a005939205fcf6239ba93d64227d2a3e617fd5bb4777b7db54eadb4e')
    version('2.17.9',  sha256='e5a06a155c28b01dd62ecc2b3d00ff1eb80b016e9f4c2627a49db4444b97b554')
    version('2.17.8',  sha256='5e5ae1d4f8788e227ed96dab711cadcfb315d737b0e049c34954bd6dafe1b5b8')
    version('2.17.7',  sha256='b05e828fac19acb3bddb7d5e5af69617f29f34aea78dd2045cf30edc834cb4d5')
    version('2.17.6',  sha256='15be4803789d8a3b0aa7ea9629a21ea56ff46ea5d8b484004a00826d4ffcbd00')
    version('2.17.5',  sha256='d0bc9440c61000e6076f3cd446bbe9add763bfc5ad98ba067dac0f9fab8cd2eb')
    version('2.17.4',  sha256='82f9e316d5937e482d272fc05613a7ed67b2d20aeb1d0ae944a75c948dd07bd2')
    version('2.17.3',  sha256='05cfbfb12d1dcc4968200f4eda791002e999be33d38123c6e341560b2b7b9b59')
    version('2.17.2',  sha256='d0c3f126dc7d9b738c60d4d212bb7339cd79e69cfdf8b1b8323e93e2a5107b14')
    version('2.17.1',  sha256='b9ccd51b3c9366c1be17f6321ec1ee660a27b0df8e57e51d1587fd8aea1cd654')
    version('2.16.1', sha256='64529add74df3db828f704b42d4ec3fcdacb8142c84f051f9213637c337e706c')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('gettext')
    depends_on('openssl')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')
