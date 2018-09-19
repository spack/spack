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


class Vegas2(Package):
    """"VEGAS2 is an extension that uses 1,000 Genomes data to model SNP
        correlations across the autosomes and chromosome X"""

    homepage = "https://vegas2.qimrberghofer.edu.au/"
    url      = "https://vegas2.qimrberghofer.edu.au/vegas2v2"

    version('2', '815d80b86e9e294f99332bb5181e897a', expand=False)

    depends_on('perl', type='run')
    depends_on('r', type='run')
    depends_on('plink')
    depends_on('r-mvtnorm', type='run')
    depends_on('r-corpcor', type='run')

    def url_for_version(self, version):
        url = 'https://vegas2.qimrberghofer.edu.au/vegas2v{0}'
        return url.format(version)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('vegas2v{0}'.format(self.version), prefix.bin)
