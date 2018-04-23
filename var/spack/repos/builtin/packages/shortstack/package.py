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


class Shortstack(Package):
    """ShortStack is a tool developed to process and analyze smallRNA-seq data
       with respect to a reference genome, and output a comprehensive and
       informative annotation of all discovered small RNA genes."""

    homepage = "http://sites.psu.edu/axtell/software/shortstack/"
    url      = "https://github.com/MikeAxtell/ShortStack/archive/v3.8.3.tar.gz"

    version('3.8.3', '3f21f494f799039f3fa88ea343f2d20d')

    depends_on('perl', type=('build', 'run'))
    depends_on('samtools')
    depends_on('viennarna')
    depends_on('bowtie')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('ShortStack', prefix.bin)
