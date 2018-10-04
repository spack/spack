##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *
import os


class Figtree(Package):
    """FigTree is designed as a graphical viewer of phylogenetic trees and
       as a program for producing publication-ready figures. As with most of
       my programs, it was written for my own needs so may not be as polished
       and feature-complete as a commercial program. In particular it is
       designed to display summarized and annotated trees produced by BEAST."""

    homepage = "https://github.com/rambaut/figtree"
    url      = "https://github.com/rambaut/figtree/releases/download/v1.4.3/FigTree_v1.4.3.tgz"

    version('1.4.3', sha256='f497d4dd3a6d220f6b62495b6f47a12ade50d87dbd8d6089f168e94d202f937b')

    depends_on('java', type='run')

    def patch(self):
        # we have to change up the executable to point to the right program
        filter_file('lib/figtree.jar',
                    join_path(self.spec.prefix.lib, 'figtree.jar'),
                    'bin/figtree', string=True)

        # also set proper executable flags
        os.chmod('bin/figtree', 0o775)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree('bin', prefix.bin)

        mkdirp(prefix.lib)
        install_tree('lib', prefix.lib)
