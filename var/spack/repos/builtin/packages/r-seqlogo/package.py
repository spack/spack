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


class RSeqlogo(RPackage):
    """seqLogo takes the position weight matrix of a DNA sequence motif and
       plots the corresponding sequence logo as introduced by Schneider and
       Stephens (1990)."""

    homepage = "https://bioconductor.org/packages/seqLogo/"
    git      = "https://git.bioconductor.org/packages/seqLogo.git"

    version('1.44.0', commit='4cac14ff29f413d6de1a9944eb5d21bfe5045fac')

    depends_on('r@3.4.3:3.4.9', when='@1.44.0')
