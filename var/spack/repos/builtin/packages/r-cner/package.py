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


class RCner(RPackage):
    """"Large-scale identification and advanced visualization of sets of
        conserved noncoding elements."""

    homepage = "https://bioconductor.org/packages/CNEr/"
    git      = "https://git.bioconductor.org/packages/CNEr.git"

    version('1.14.0', commit='b8634d65c51728c815127e22b45eba7c9b9db897')

    depends_on('r-biostrings@2.33.4:', type=('build', 'run'))
    depends_on('r-dbi@0.7:', type=('build', 'run'))
    depends_on('r-rsqlite@0.11.4:', type=('build', 'run'))
    depends_on('r-genomeinfodb@1.1.3:', type=('build', 'run'))
    depends_on('r-genomicranges@1.23.16:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.25.5:', type=('build', 'run'))
    depends_on('r-xvector@0.5.4:', type=('build', 'run'))
    depends_on('r-genomicalignments@1.1.9:', type=('build', 'run'))
    depends_on('r-s4vectors@0.13.13:', type=('build', 'run'))
    depends_on('r-iranges@2.5.27:', type=('build', 'run'))
    depends_on('r-readr@0.2.2:', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-reshape2@1.4.1:', type=('build', 'run'))
    depends_on('r-ggplot2@2.1.0:', type=('build', 'run'))
    depends_on('r-powerlaw@0.60.3:', type=('build', 'run'))
    depends_on('r-annotate@1.50.0:', type=('build', 'run'))
    depends_on('r-go-db@3.3.0:', type=('build', 'run'))
    depends_on('r-keggrest@1.14.0:', type=('build', 'run'))
    depends_on('r-utils@2.3.0:', type=('build', 'run'))
    depends_on('r@3.4.3:3.4.9', when='@1.14.0')
