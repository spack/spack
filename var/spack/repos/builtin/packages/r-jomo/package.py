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


class RJomo(RPackage):
    """Similarly to Schafer's package 'pan', 'jomo' is a package for multilevel
    joint modelling multiple imputation (Carpenter and Kenward, 2013)
    <doi:10.1002/9781119942283>. Novel aspects of 'jomo' are the possibility of
    handling binary and categorical data through latent normal variables, the
    option to use cluster-specific covariance matrices and to impute compatibly
    with the substantive model.
    """

    homepage = "https://cran.r-project.org/package=jomo"
    url      = "https://cran.r-project.org/src/contrib/jomo_2.6-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/jomo"

    version('2.6-2', 'eff4a6c1a971708959d65b3224c98a25')

    depends_on('r-lme4', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
