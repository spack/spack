# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rdptools(MakefilePackage):
    """Collection of commonly used RDP Tools for easy building."""

    homepage = "https://github.com/rdpstaff/RDPTools"
    url      = "https://github.com/rdpstaff/RDPTools/archive/2.0.2.tar.gz"

    version('2.0.3', sha256='2e1a32d0d2fdf775aae6e5a33035a6065775c781c1dd28148d588970cf3a6e2b')
    version('2.0.2', sha256='fc3d7f8129b45e602fc2c23e5e037a7f48c14d5a6b05c64f8c1d48e9767ac01d')

    # https://github.com/bioconda/bioconda-recipes/blob/master/recipes/rdptools/meta.yaml
    depends_on('java')
    depends_on('ant')
    depends_on('python')

    def install(self, spec, prefix):
        install_tree('.', prefix)
