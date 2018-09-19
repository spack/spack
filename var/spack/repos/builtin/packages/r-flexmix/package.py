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


class RFlexmix(RPackage):
    """flexmix: Flexible Mixture Modeling"""

    homepage = "https://CRAN.R-project.org/package=flexmix"
    url      = "https://cran.r-project.org/src/contrib/flexmix_2.3-14.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/flexmix"

    version('2.3-14', '5be4f7764e6a697f4586e60c2bf6e960')

    depends_on('r@2.15.0:')
    # depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-modeltools@0.2-16:', type=('build', 'run'))
    # depends_on('r-nnet', type=('build', 'run'))
