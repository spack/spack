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


class RPbkrtest(RPackage):
    """Test in mixed effects models. Attention is on mixed effects models as
    implemented in the 'lme4' package. This package implements a parametric
    bootstrap test and a Kenward Roger modification of F-tests for linear mixed
    effects models and a parametric bootstrap test for generalized linear mixed
    models."""

    homepage = "http://people.math.aau.dk/~sorenh/software/pbkrtest/"
    url      = "https://cran.r-project.org/src/contrib/pbkrtest_0.4-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pbkrtest"

    version('0.4-6', '0a7d9ff83b8d131af9b2335f35781ef9')
    version('0.4-4', '5e54b1b1b35413dd1d24ef15735ec645')

    depends_on('r@3.2.3:')

    depends_on('r-lme4@1.1.10:', type=('build', 'run'))
    depends_on('r-matrix@1.2.3:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
