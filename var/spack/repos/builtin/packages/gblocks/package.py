# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gblocks(Package):
    """Gblocks is a computer program written in ANSI C language that eliminates
       poorly aligned positions and divergent regions of an alignment of DNA or
       protein sequences"""

    homepage = "http://molevol.cmima.csic.es/castresana/Gblocks.html"
    url      = "http://molevol.cmima.csic.es/castresana/Gblocks/Gblocks_Linux64_0.91b.tar.Z"

    version('0.91b', 'c2c752ae4cbfda0b8bf09e6662585252')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('Gblocks', prefix.bin)
