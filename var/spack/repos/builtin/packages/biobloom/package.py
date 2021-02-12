# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Biobloom(AutotoolsPackage):
    """BioBloom Tools (BBT) provides the means to create filters for a given
       reference and then to categorize sequences."""

    homepage = "https://github.com/bcgsc/biobloom"
    url      = "https://github.com/bcgsc/biobloom/releases/download/2.2.0/biobloomtools-2.2.0.tar.gz"

    version('2.3.3', sha256='cd3ca08677aae4cf99da30fdec87a23b12a8320c6d0e21df9d0c3b26b62b6153')
    version('2.3.2', sha256='a1e6b5a58750280c29f82f7d2f795efaeab8bebe1266f2e8f6e285649fd7f38a')
    version('2.3.1', sha256='0a0b8854a1e5c8206b977d8365fdd9b23027b3c500e2bbac140eb6d3d047dc77')
    version('2.3.0', sha256='e5396cd1a463bc34d93433a2314a42bf365770eb8f011327a0119a8113a15913')
    version('2.2.0', sha256='5d09f8690f0b6402f967ac09c5b0f769961f3fe3791000f8f73af6af7324f02c')

    depends_on('boost')
    depends_on('sdsl-lite')
    depends_on('sparsehash')
    depends_on('zlib')

    def configure_args(self):
        # newer versions of sdsl-lite introduce tolerable warnings
        # they must disabled to allow the build to continue

        return ['CXXFLAGS=-w', 'CPPFLAGS=-w']
