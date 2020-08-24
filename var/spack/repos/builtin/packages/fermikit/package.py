# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fermikit(MakefilePackage):
    """De novo assembly based variant calling pipeline for Illumina short
    reads"""

    homepage = "https://github.com/lh3/fermikit"
    git      = "https://github.com/lh3/fermikit.git"

    version('2017-11-7', commit='bf9c7112221577ba110665bddca8f1987250bdc7',
            submodules=True)

    depends_on('zlib')

    def install(self, spec, prefix):
        install_tree('fermi.kit', prefix.bin)
