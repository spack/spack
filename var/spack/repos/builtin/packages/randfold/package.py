# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Randfold(MakefilePackage):
    """Minimum free energy of folding randomization test software"""

    homepage = "http://bioinformatics.psb.ugent.be/supplementary_data/erbon/nov2003/"
    url      = "http://bioinformatics.psb.ugent.be/supplementary_data/erbon/nov2003/downloads/randfold-2.0.1.tar.gz"

    version('2.0.1', 'c9ebf7dc9d62fa4554a738a15fe1ded8')

    depends_on('squid')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('randfold', prefix.bin)
