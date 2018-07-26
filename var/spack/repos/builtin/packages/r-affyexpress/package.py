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


class RAffyexpress(RPackage):
    """The purpose of this package is to provide a comprehensive and
    easy-to-use tool for quality assessment and to identify differentially
    expressed genes in the Affymetrix gene expression data."""

    homepage = "https://www.bioconductor.org/packages/AffyExpress/"
    git      = "https://git.bioconductor.org/packages/AffyExpress.git"

    version('1.42.0', commit='f5c5cf6173f4419e25f4aeff5e6b705a40abc371')

    depends_on('r@3.4.0:3.4.9', when='@1.42.0')
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
