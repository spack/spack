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

    version('2.5.1',  sha256='89aac9c35ad875f1b17144bf9fcbfa7231554d4abce187d9277fcc83da846e4a')
    version('2.5.0',  sha256='4e9d1cbcdd2346cab5b7fc176cd57c07ed3628a0241fad8a48fe4df6a354b120')
    version('2.4.0',  sha256='3c87db4d9825a342fc55bd7f27461099dd46291aea4a4a29bb95d3c896403f94')
    version('2.3.0',  sha256='56bcf353adc17c386377ffcdfc980cbaff36123a1c1132ba09c3c51a7d1c9b82')
    version('2.2.0',  sha256='597c6c1cde4484164e9320af0481e33cfad2330a02315b4c841bdc5b7543caec')
    version('2.1.0',  sha256='4b353b121a0f3ddf5046f0a1ae719a0539e0cddef27cc78a1b33ad7d1d22c007')
    version('2.0.0',  sha256='5d93535395a6684dee1d9d1d3cde859addd76f56581e0111d95a9c685d582426')
    version('1.14.0', sha256='1a99050644b4821477aabc7642bbcae8a19b3191e9227cd8078016d78cdd83ac')
    version('1.13.1', sha256='1a19ab2bfdf265b5e2dcba53c3bd0b5a88f36eff4864dcc38865e33388b600c5')

    depends_on('go@1.16:', type='build')

    def install(self, spec, prefix):
        make()
        make('install', 'prefix=' + prefix)
