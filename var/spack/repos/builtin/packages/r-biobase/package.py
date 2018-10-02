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
#
from spack import *


class RBiobase(RPackage):
    """Functions that are needed by many other packages
    or which replace R functions."""

    homepage = "https://www.bioconductor.org/packages/Biobase/"
    git      = "https://git.bioconductor.org/packages/Biobase.git"

    version('2.40.0', commit='6555edbbcb8a04185ef402bfdea7ed8ac72513a5')
    version('2.38.0', commit='83f89829e0278ac014b0bc6664e621ac147ba424')
    version('2.36.2', commit='15f50912f3fa08ccb15c33b7baebe6b8a59ce075')

    depends_on('r-biocgenerics@0.16.1:', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.36.2', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.40.0', type=('build', 'run'))
