# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mold(MakefilePackage):
    """mold is a faster drop-in replacement for existing Unix linkers"""

    homepage = "https://github.com/rui314/mold"
    url      = "https://github.com/rui314/mold/archive/refs/tags/v1.2.1.tar.gz"

    maintainers = ['haampie']

    version('1.2.1', sha256='41868663ff18afee3fa35e5e3fdf3d9575eb2e4ff49967b8f42f479c61c1ec34')

    depends_on('intel-tbb@2021:')

    # xxhash is vendored and doesn't have a SYSTEM_XXHASH variable
    # depends_on('xxhash')

    # not on darwin.
    depends_on('mimalloc', when='platform=linux')
    depends_on('mimalloc', when='platform=cray')
    depends_on('openssl', when='platform=linux')
    depends_on('openssl', when='platform=cray')

    depends_on('pkgconfig', when='^openssl', type='build')  # used to detect openssl
    depends_on('python@3:', type='build')  # just used to compute a relative path

    def make_args(self, spec, prefix):
        return [
            'SYSTEM_MIMALLOC=1',
            'SYSTEM_TBB=1',
            'PREFIX={}'.format(prefix)
        ]

    def build(self, spec, prefix):
        make(*self.make_args(spec, prefix))

    def install(self, spec, prefix):
        make('install', *self.make_args(spec, prefix))
