# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gh(Package):
    """GitHub's official command line tool."""

    homepage = "https://github.com/cli/cli"
    url      = "https://github.com/cli/cli/archive/refs/tags/v2.0.0.tar.gz"

    maintainers = ['lcnzg']

    version('2.5.1',  sha256='9a057b5443c1afa53b5051eeccc4d0f5dea4d1c8c59ca6cb28d41185fed17bd1')
    version('2.5.0',  sha256='54d0a049de817236611e9f3652ecf0b2341fe0024671dd50359aea0f3acbb686')
    version('2.4.0',  sha256='0317d420ce5976fee59f26bec059e5ffcb763b9e7af708176322d11d14d893e1')
    version('2.3.0',  sha256='b10d6c99cc5d58c07efdd8a04cb6f182a3b0aa3b833d5c9a2f05c241ffe40701')
    version('2.2.0',  sha256='c9c8a716f79fbd8f0a165292e94550f15d0208e6cd3383e5ce942fd2a9ada57f')
    version('2.1.0',  sha256='258944c59cb34c9e8716ecc1e7a3d90f72da9b96b4d85ec9b7b773b4370c88ff')
    version('2.0.0',  sha256='5d93535395a6684dee1d9d1d3cde859addd76f56581e0111d95a9c685d582426')
    version('1.14.0', sha256='1a99050644b4821477aabc7642bbcae8a19b3191e9227cd8078016d78cdd83ac')
    version('1.13.1', sha256='1a19ab2bfdf265b5e2dcba53c3bd0b5a88f36eff4864dcc38865e33388b600c5')

    depends_on('go@1.16:', type='build')

    def install(self, spec, prefix):
        make()
        make('install', 'prefix=' + prefix)
