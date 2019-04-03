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


class Tophat(AutotoolsPackage):
    """TopHat is a fast splice junction mapper for RNA-Seq reads.

     It aligns RNA-Seq reads to mammalian-sized genomes using the ultra
     high-throughput short read aligner Bowtie, and then analyzes the
     the mapping results to identify splice junctions between exons."""

    homepage = "https://ccb.jhu.edu/software/tophat/index.shtml"
    url      = "https://ccb.jhu.edu/software/tophat/downloads/tophat-2.1.1.tar.gz"

    version('2.1.1', '4b2391de46457ba6b2b7268a9da593e4')

    depends_on('boost@1.47:')
    depends_on('ncurses')
    depends_on('bowtie2', type='run')

    parallel = False

    def configure_args(self):
        args = ['--with-boost=%s' % self.spec['boost'].prefix]
        return args
