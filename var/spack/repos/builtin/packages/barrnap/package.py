# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Barrnap(Package):
    """Barrnap predicts the location of ribosomal RNA genes in genomes."""

    homepage = "https://github.com/tseemann/barrnap"
    url      = "https://github.com/tseemann/barrnap/archive/0.8.tar.gz"

    version('0.8', 'd02ccb800d60fa824bae946dd4fa2358')

    depends_on('hmmer@3.1b:', type='run')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('db', prefix.db)
