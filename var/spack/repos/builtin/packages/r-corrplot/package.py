# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCorrplot(RPackage):
    """A graphical display of a correlation matrix or general matrix.
    It also contains some algorithms to do matrix reordering."""

    homepage = "https://cran.r-project.org/package=corrplot"
    url      = "https://cran.r-project.org/src/contrib/corrplot_0.77.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/corrplot"

    version('0.77', '2a5d54fd5c65618b9afba1a32f6b4542')
