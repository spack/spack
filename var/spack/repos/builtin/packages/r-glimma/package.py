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


class RGlimma(RPackage):
    """This package generates interactive visualisations for analysis of
       RNA-sequencing data using output from limma, edgeR or DESeq2 packages
       in an HTML page. The interactions are built on top of the popular
       static representations of analysis results in order to provide
       additional information."""

    homepage = "https://bioconductor.org/packages/release/bioc/html/Glimma.html"
    git      = "https://git.bioconductor.org/packages/Glimma.git"

    version('1.8.2', commit='f4aa1f05c2890d04b01ad4c0ab27f2f729f2c969')

    depends_on('r@3.5.0:3.5.9', when='@1.8.2:', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
