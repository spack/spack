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


class RLimma(RPackage):
    """Data analysis, linear models and differential expression
    for microarray data."""

    homepage = "https://www.bioconductor.org/packages/limma/"
    git      = "https://git.bioconductor.org/packages/limma.git"

    version('3.36.2',  commit='0cd5c13e22565182226bd2937ffcf8c59de1ca59')
    version('3.34.9',  commit='6755278a929f942a49e2441fb002a3ed393e1139')
    version('3.32.10', commit='593edf28e21fe054d64137ae271b8a52ab05bc60')

    depends_on('r@3.5.0:3.5.9', when='@3.36.2')
    depends_on('r@3.4.2:3.4.9', when='@3.34.9')
    depends_on('r@3.4.0:3.4.9', when='@3.32.10')
