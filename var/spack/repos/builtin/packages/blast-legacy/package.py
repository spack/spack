# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BlastLegacy(Package):
    """Legacy NCBI BLAST distribution -- no longer supported.
       Contains older programs including `blastall'"""

    homepage = "https://www.ncbi.nlm.nih.gov/"
    url      = "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/blast-2.2.26-x64-linux.tar.gz"

    version('2.2.26', sha256='8a2f986cf47f0f7cbdb3478c4fc7e25c7198941d2262264d0b6b86194b3d063d')

    def install(self, spec, prefix):
        install_tree('.', prefix)
