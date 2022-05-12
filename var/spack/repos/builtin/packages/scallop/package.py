# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Scallop(AutotoolsPackage):
    """Scallop is a reference-based transcriptome assembler for RNA-seq"""

    homepage = "https://github.com/Kingsford-Group/scallop"
    url      = "https://github.com/Kingsford-Group/scallop/releases/download/v0.10.5/scallop-0.10.5.tar.gz"

    version('0.10.5', sha256='b09e3c61f1b3b1da2a96d9d8429d80326a3bb14f5fe6af9b5e87570d4b86937a')
    version('0.10.3', sha256='04eb3ab27ed8c7ae38e1780d6b2af16b6a2c01807ffafd59e819d33bfeff58a0')

    depends_on('clp')
    # Fixme: There does not seem to be any dependency on boost, please consider removing
    depends_on(Boost.with_default_variants)
    depends_on('htslib@1.5:')

    def configure_args(self):
        return [
            '--with-clp={0}'.format(self.spec['clp'].prefix),
            '--with-htslib={0}'.format(self.spec['htslib'].prefix),
            '--with-boost={0}'.format(self.spec['boost'].prefix),
        ]
