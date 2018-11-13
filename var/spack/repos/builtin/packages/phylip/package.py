# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Phylip(Package):
    """PHYLIP (the PHYLogeny Inference Package) is a package of programs for
       inferring phylogenies (evolutionary trees)."""

    homepage = "http://evolution.genetics.washington.edu/phylip/"
    url      = "http://evolution.gs.washington.edu/phylip/download/phylip-3.697.tar.gz"

    version('3.697', '0e83d17fb4d668213603c86bc21d9012')
    version('3.696', 'dbe5abc26f6089ead3dba41c2db526ee')

    def install(self, spec, prefix):
        with working_dir('src'):
            if self.spec.satisfies('platform=darwin'):
                make('all', '-f', 'Makefile.osx')
                make('put', '-f', 'Makefile.osx')
            else:
                make('all', '-f', 'Makefile.unx')
                make('put', '-f', 'Makefile.unx')
        install_tree('exe', prefix.bin)
