# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REllipse(RPackage):
    """This package contains various routines for drawing ellipses and
    ellipse-like confidence regions."""

    homepage = "https://cran.r-project.org/package=ellipse"
    url      = "https://cran.r-project.org/src/contrib/ellipse_0.3-8.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ellipse"

    version('0.3-8', '385f5ec5e49bcda4317ca9dffd33f771')

    depends_on('r@2.0.0:')
