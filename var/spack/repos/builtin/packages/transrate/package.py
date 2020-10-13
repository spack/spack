# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Transrate(Package):
    """Transrate is software for de-novo transcriptome assembly quality
       analysis."""

    homepage = "http://hibberdlab.com/transrate/"
    url      = "https://bintray.com/artifact/download/blahah/generic/transrate-1.0.3-linux-x86_64.tar.gz"

    version('1.0.3', sha256='68d034ecd7012f1d3d505a2edd820c1155cd8b64d2acbf2ac833f30d3800141b')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
