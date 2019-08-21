# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RFormatr(RPackage):
    """Provides a function tidy_source() to format R source code. Spaces and
    indent will be added to the code automatically, and comments will be
    preserved under certain conditions, so that R code will be more
    human-readable and tidy. There is also a Shiny app as a user interface in
    this package."""

    homepage = "https://cloud.r-project.org/package=formatR"
    url      = "https://cloud.r-project.org/src/contrib/formatR_1.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/formatR"

    version('1.7', sha256='a366621b3ff5f8e86a499b6f87858ad47eefdace138341b1377ecc307a5e5ddb')
    version('1.6', sha256='f5c98f0c3506ca51599671a2cdbc17738d0f326e8e3bb18b7a38e9f172122229')
    version('1.5', 'ac735515b8e4c32097154f1b68c5ecc7')
    version('1.4', '98b9b64b2785b35f9df403e1aab6c73c')

    depends_on('r@3.0.2:', type=('build', 'run'))
