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


class RBroom(RPackage):
    """Convert statistical analysis objects from R into tidy data frames, so
       that they can more easily be combined, reshaped and otherwise processed
       with tools like 'dplyr', 'tidyr' and 'ggplot2'. The package provides
       three S3 generics: tidy, which summarizes a model's statistical
       findings such as coefficients of a regression; augment, which adds
       columns to the original data such as predictions, residuals and cluster
       assignments; and glance, which provides a one-row summary of
       model-level statistics."""

    homepage = "http://github.com/tidyverse/broom"
    url      = "https://cran.r-project.org/src/contrib/broom_0.4.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/broom"
    version('0.4.2', '6eabab1f2eaec10f93cf9aa56d6a61de')

    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-psych', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
