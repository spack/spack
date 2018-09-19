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


class Transabyss(Package):
    """De novo assembly of RNAseq data using ABySS"""

    homepage = "http://www.bcgsc.ca/platform/bioinfo/software/trans-abyss"
    url      = "http://www.bcgsc.ca/platform/bioinfo/software/trans-abyss/releases/1.5.5/transabyss-1.5.5.zip"

    version('1.5.5', '9ebe0394243006f167135cac4df9bee6')

    depends_on('abyss@1.5.2')
    depends_on('python@2.7.6:', type=('build', 'run'))
    depends_on('py-igraph@0.7.0:', type=('build', 'run'))
    depends_on('blat')

    def install(self, spec, prefix):
        install('transabyss', prefix)
        install('transabyss-merge', prefix)
        install_tree('bin', prefix.bin)
        install_tree('utilities', prefix.utilities)
