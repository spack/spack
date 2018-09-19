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


class Paml(MakefilePackage):
    """PAML is a package of programs for phylogenetic analyses of DNA or
       protein sewuences using maximum likelihood."""

    homepage = "http://abacus.gene.ucl.ac.uk/software/paml.html"
    url      = "http://abacus.gene.ucl.ac.uk/software/paml4.9e.tgz"

    version('4.9e', 'ac5a062bfea1f4eaac79008434030acf')

    build_directory = 'src'

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install('baseml', prefix.bin)
            install('basemlg', prefix.bin)
            install('chi2', prefix.bin)
            install('codeml', prefix.bin)
            install('evolver', prefix.bin)
            install('infinitesites', prefix.bin)
            install('mcmctree', prefix.bin)
            install('pamp', prefix.bin)
            install('yn00', prefix.bin)
        install_tree('dat', prefix.dat)
        install_tree('Technical', prefix.Technical)
