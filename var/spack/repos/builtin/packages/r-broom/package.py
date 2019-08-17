# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
