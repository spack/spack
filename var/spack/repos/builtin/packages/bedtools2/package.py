# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bedtools2(Package):
    """Collectively, the bedtools utilities are a swiss-army knife of
       tools for a wide-range of genomics analysis tasks. The most
       widely-used tools enable genome arithmetic: that is, set theory
       on the genome."""

    homepage = "https://github.com/arq5x/bedtools2"
    url      = "https://github.com/arq5x/bedtools2/archive/v2.26.0.tar.gz"

    version('2.29.2', sha256='bc2f36b5d4fc9890c69f607d54da873032628462e88c545dd633d2c787a544a5')
    version('2.27.1', sha256='edcac089d84e63a51f85c3c189469daa7d42180272130b046856faad3cf79112')

    depends_on('zlib')
    depends_on('python', type='build')

    def install(self, spec, prefix):
        make("prefix=%s" % prefix, "install")
