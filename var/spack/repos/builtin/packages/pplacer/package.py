##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Pplacer(Package):
    """Pplacer places query sequences on a fixed reference phylogenetic tree
       to maximize phylogenetic likelihood or posterior probability according
       to a reference alignment. Pplacer is designed to be fast, to give
       useful information about uncertainty, and to offer advanced
       visualization and downstream analysis.
    """

    homepage = "http://matsen.fhcrc.org/pplacer/"
    url      = "https://github.com/matsen/pplacer/releases/download/v1.1.alpha19/pplacer-linux-v1.1.alpha19.zip"

    version('1.1.alpha19', 'e6b78604882d41d4bf13592c7edebfa2')

    def install(self, spec, prefix):
        install_tree('scripts', prefix.bin)
        force_remove(join_path(prefix.bin, 'setup.py'))
        install('guppy', prefix.bin)
        install('pplacer', prefix.bin)
        install('rppr', prefix.bin)
