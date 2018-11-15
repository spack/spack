# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rtax(Package):
    """Rapid and accurate taxonomic classification of short paired-end
       sequence reads from the 16S ribosomal RNA gene"""

    homepage = "https://github.com/davidsoergel/rtax"
    url      = "http://static.davidsoergel.com/rtax-0.984.tgz"

    version('0.984', 'e9dbbe4b3c26b0f0f6c14a5fb46aa587')

    depends_on('usearch')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('rtax', prefix.bin)
        install_tree('scripts', prefix.bin.scripts)
        install_tree('greengenes', prefix.bin.greengenes)
