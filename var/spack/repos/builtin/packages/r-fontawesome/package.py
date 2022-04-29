# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RFontawesome(RPackage):
    """Easily Work with 'Font Awesome' Icons.

    Easily and flexibly insert 'Font Awesome' icons into 'R Markdown' documents
    and 'Shiny' apps. These icons can be inserted into HTML content through
    inline 'SVG' tags or 'i' tags. There is also a utility function for
    exporting 'Font Awesome' icons as 'PNG' images for those situations where
    raster graphics are needed."""

    cran = "fontawesome"

    version('0.2.2', sha256='572db64d1b3c9be301935e0ca7baec69f3a6e0aa802e23f1f224b3724259df64')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-rlang@0.4.10:', type=('build', 'run'))
    depends_on('r-htmltools@0.5.1.1:', type=('build', 'run'))
