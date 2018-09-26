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


class Wgsim(Package):
    """Wgsim is a small tool for simulating sequence reads from a reference
    genome.

    It is able to simulate diploid genomes with SNPs and insertion/deletion
    (INDEL) polymorphisms, and simulate reads with uniform substitution
    sequencing errors. It does not generate INDEL sequencing errors, but this
    can be partly compensated by simulating INDEL polymorphisms."""

    homepage = "https://github.com/lh3/wgsim"
    git      = "https://github.com/lh3/wgsim.git"

    version('2011.10.17', commit='a12da3375ff3b51a5594d4b6fa35591173ecc229')

    depends_on('zlib')

    def install(self, spec, prefix):
        cc = Executable(spack_cc)
        cc('-g', '-O2', '-Wall', '-o', 'wgsim', 'wgsim.c', '-lz', '-lm')

        install_tree(self.stage.source_path, prefix.bin)
