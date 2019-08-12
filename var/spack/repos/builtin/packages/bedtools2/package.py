# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('2.27.1', '8e0afcab95a824e42a6e99c5436a8438')
    version('2.27.0', '052f22eb214ef2e7e7981b3c01167302')
    version('2.26.0', '52227e7efa6627f0f95d7d734973233d')
    version('2.25.0', '534fb4a7bf0d0c3f05be52a0160d8e3d')
    version('2.23.0', '4fa3671b3a3891eefd969ad3509222e3')

    depends_on('zlib')

    def install(self, spec, prefix):
        make("prefix=%s" % prefix, "install")
