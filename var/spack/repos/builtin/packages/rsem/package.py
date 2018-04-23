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


class Rsem(MakefilePackage):
    """RSEM is a software package for estimating gene and isoform expression
       levels from RNA-Seq data."""

    homepage = "http://deweylab.github.io/RSEM/"
    url      = "https://github.com/deweylab/RSEM/archive/v1.3.0.tar.gz"

    version('1.3.0', '273fd755e23d349cc38a079b81bb03b6')

    depends_on('r', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    depends_on('bowtie')
    depends_on('bowtie2')
    depends_on('star')

    def install(self, spec, prefix):
        make('install', 'DESTDIR=%s' % prefix, 'prefix=')
