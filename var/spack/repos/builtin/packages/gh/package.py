# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gh(Package):
    """GitHub's official command line tool."""

    homepage = "https://github.com/cli/cli"
    url      = "https://github.com/cli/cli/archive/refs/tags/v2.0.0.tar.gz"

    maintainers = ['lcnzg']

    version('2.0.0',  sha256='5d93535395a6684dee1d9d1d3cde859addd76f56581e0111d95a9c685d582426')
    version('1.14.0', sha256='1a99050644b4821477aabc7642bbcae8a19b3191e9227cd8078016d78cdd83ac')
    version('1.13.1', sha256='1a19ab2bfdf265b5e2dcba53c3bd0b5a88f36eff4864dcc38865e33388b600c5')

    depends_on('go@1.16:', type='build')

    def install(self, spec, prefix):
        make()
        make('install', 'prefix=' + prefix)
