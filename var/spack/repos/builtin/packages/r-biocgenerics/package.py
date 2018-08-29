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


class RBiocgenerics(RPackage):
    """S4 generic functions needed by many Bioconductor packages."""

    homepage = "https://www.bioconductor.org/packages/BiocGenerics/"
    git      = "https://git.bioconductor.org/packages/BiocGenerics.git"

    version('0.26.0', commit='5b2a6df639e48c3cd53789e0b174aec9dda6b67d')
    version('0.24.0', commit='3db111e8c1f876267da89f4f0c5406a9d5c31cd1')
    version('0.22.1', commit='9c90bb8926885289d596a81ff318ee3745cbb6ad')

    depends_on('r@3.4.0:3.4.9', when='@0.22.1', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@0.26.0', type=('build', 'run'))
