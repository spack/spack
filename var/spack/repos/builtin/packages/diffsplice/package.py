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


class Diffsplice(MakefilePackage):
    """A novel tool for discovering and quantitating alternative splicing
    variants present in an RNA-seq dataset, without relying on annotated
    transcriptome or pre-determined splice pattern."""

    homepage = "http://www.netlab.uky.edu/p/bioinfo/DiffSplice"
    url      = "http://protocols.netlab.uky.edu/~yin/download/diffsplice/diffsplice_0.1.1.tgz"

    version('0.1.2beta', 'a1df6e0b50968f2c229d5d7f97327336')
    version('0.1.1',     'be90e6c072402d5aae0b4e2cbb8c10ac')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('diffsplice', prefix.bin)
