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


class RAnimation(RPackage):
    """Provides functions for animations in statistics, covering topics
    in probability theory, mathematical statistics, multivariate statistics,
    non-parametric statistics, sampling survey, linear models, time series,
    computational statistics, data mining and machine learning.
    These functions maybe helpful in teaching statistics and data analysis."""

    homepage = "https://cran.r-project.org/package=animation"
    url = "https://cran.r-project.org/src/contrib/animation_2.5.tar.gz"

    version('2.5', sha256='b232fef1b318c79710e5e1923d87baba4c85ffe2c77ddb188130e0911d8cb55f')

    extends('r')
    depends_on('r', type=('build', 'run'))
