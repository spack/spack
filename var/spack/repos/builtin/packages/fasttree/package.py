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


class Fasttree(Package):
    """FastTree infers approximately-maximum-likelihood phylogenetic
       trees from alignments of nucleotide or protein sequences.
       FastTree can handle alignments with up to a million of sequences
       in a reasonable amount of time and memory."""

    homepage = "http://www.microbesonline.org/fasttree"
    url      = "http://www.microbesonline.org/fasttree/FastTree-2.1.10.c"

    version('2.1.10', '1c2c6425a638ec0c61ef064cda687987', expand=False, url='http://www.microbesonline.org/fasttree/FastTree-2.1.10.c')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        cc = Executable(spack_cc)
        cc('-O3', self.compiler.openmp_flag,
           '-DOPENMP', '-finline-functions', '-funroll-loops', '-Wall',
           '-oFastTreeMP', 'FastTree-' + format(spec.version.dotted) + '.c',
           '-lm')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('FastTreeMP', prefix.bin)
