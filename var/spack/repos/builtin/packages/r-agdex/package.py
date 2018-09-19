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


class RAgdex(RPackage):
    """A tool to evaluate agreement of differential expression
    for cross-species genomics."""

    homepage = "http://bioconductor.org/packages/AGDEX/"
    git      = "https://git.bioconductor.org/packages/AGDEX.git"

    version('1.24.0', commit='29c6bcfa6919a5c6d8bcb36b44e75145a60ce7b5')

    depends_on('r@3.4.0:3.4.9', when='@1.24.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-gseabase', type=('build', 'run'))
