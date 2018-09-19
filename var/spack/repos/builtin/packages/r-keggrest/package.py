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


class RKeggrest(RPackage):
    """This package provides functions and routines useful in the analysis
       of somatic signatures (cf. L. Alexandrov et al., Nature 2013). In
       particular, functions to perform a signature analysis with known
       signatures (LCD = linear combination decomposition) and a signature
       analysis on stratified mutational catalogue (SMC = stratify mutational
       catalogue) are provided."""

    homepage = "http://bioconductor.org/packages/KEGGREST"
    git      = "https://git.bioconductor.org/packages/KEGGREST.git"

    version('1.18.1', commit='f6e6f1987e4db9d977a75609fab0cb710be2e2e4')
    version('1.2.0',  commit='ed48de0def57a909894e237fa4731c4a052d8849')

    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.2.0')
    depends_on('r@3.4.3:3.4.9', when='@1.18.1')
