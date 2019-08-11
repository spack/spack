# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class REllipse(RPackage):
    """This package contains various routines for drawing ellipses and
    ellipse-like confidence regions."""

    homepage = "https://cloud.r-project.org/package=ellipse"
    url      = "https://cloud.r-project.org/src/contrib/ellipse_0.3-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ellipse"

    version('0.4.1', sha256='1a9a9c52195b26c2b4d51ad159ab98aff7aa8ca25fdc6b2198818d1a0adb023d')
    version('0.3-8', '385f5ec5e49bcda4317ca9dffd33f771')

    depends_on('r@2.0.0:', type=('build', 'run'))
