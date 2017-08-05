##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class RRvaidememoire(RPackage):
    """Diverse Basic Statistical and Graphical Functions"""

    homepage = "https://CRAN.R-project.org/package=RVAideMemoire"
    url      = "https://cran.r-project.org/src/contrib/RVAideMemoire_0.9-65.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RVAideMemoire"

    version('0.9-65', '4cac9b634d10890e8fd813b65a3682bf')

    depends_on('r-ade4', type=('build', 'run'))
    depends_on('r-boot', type=('build', 'run'))
    depends_on('r-car', type=('build', 'run'))
    depends_on('r-cramer', type=('build', 'run'))
    depends_on('r-dunn-test', type=('build', 'run'))
    depends_on('r-factominer', type=('build', 'run'))
    depends_on('r-lme4@1.0-4:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-mixomics@5.0.2:', type=('build', 'run'))
    depends_on('r-multcompview', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
    depends_on('r-pls', type=('build', 'run'))
    depends_on('r-pspearman', type=('build', 'run'))
    depends_on('r-vegan', type=('build', 'run'))
