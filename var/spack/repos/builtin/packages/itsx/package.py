# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Itsx(Package):
    """Improved software detection and extraction of ITS1 and ITS2 from
       ribosomal ITS sequences of fungi and other eukaryotes for use in
       environmental sequencing"""

    homepage = "http://microbiology.se/software/itsx/"
    url      = "http://microbiology.se/sw/ITSx_1.0.11.tar.gz"

    version('1.0.11', '1bff12f1d5742f19be6ca585e9bf81fa')

    depends_on('perl', type=('build', 'run'))
    depends_on('hmmer')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('ITSx', prefix.bin)
        install_tree('ITSx_db', prefix.bin.ITSx_db)
