# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Masurca(Package):
    """MaSuRCA is whole genome assembly software. It combines the efficiency
       of the de Bruijn graph and Overlap-Layout-Consensus (OLC)
       approaches."""

    homepage = "http://www.genome.umd.edu/masurca.html"
    url      = "ftp://ftp.genome.umd.edu/pub/MaSuRCA/latest/MaSuRCA-3.2.3.tar.gz"

    version('3.2.6', 'f068f91e33fd7381de406a7a954bfe01')
    version('3.2.3', 'd9b4419adfe6b64e42ce986253a50ff5')

    depends_on('perl', type=('build', 'run'))
    depends_on('boost')
    depends_on('zlib')

    def install(self, spec, prefix):
        installer = Executable('./install.sh')
        installer()
        install_tree('.', prefix)
