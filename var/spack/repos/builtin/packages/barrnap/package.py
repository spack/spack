# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Barrnap(Package):
    """Barrnap predicts the location of ribosomal RNA genes in genomes."""

    homepage = "https://github.com/tseemann/barrnap"
    url      = "https://github.com/tseemann/barrnap/archive/0.8.tar.gz"

    version('0.8', 'd02ccb800d60fa824bae946dd4fa2358')
    version('0.7', 'ef2173e250f06cca7569c03404c9d4ab6a908ef7643e28901fbe9a732d20c09b')
    version('0.6', '272642a41634623bda34dccdce487ab791925fa769e3e575d53014956a1f9dce')

    depends_on('hmmer@3.1b:', type='run')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('db', prefix.db)
