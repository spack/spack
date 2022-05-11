# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBookdown(RPackage):
    """Authoring Books and Technical Documents with R Markdown.

    Output formats and utilities for authoring books and technical documents
    with R Markdown."""

    cran = "bookdown"

    version('0.24', sha256='8bead2a20542d05f643fe77a949689a17b0ae9ff23efbb918ddab47597db1be3')
    version('0.21', sha256='47c0fa7a65da83753c2f445e0e972913f9203460f1daae3ab255d0d4b30eba76')
    version('0.12', sha256='38eb4c5b877ccd85b16cfe74a48c3bc53de2f276da98e5515f37e7a06e065bb0')
    version('0.5', sha256='b7331fd56f64bd2bddc34e2a188fc491f9ff5308f44f7e3151721247f21ca67e')

    depends_on('r+X', type=('build', 'run'))
    depends_on('r-htmltools@0.3.6:', type=('build', 'run'))
    depends_on('r-knitr@1.22:', type=('build', 'run'))
    depends_on('r-knitr@1.31:', type=('build', 'run'), when='@0.24:')
    depends_on('r-rmarkdown@1.12:', type=('build', 'run'))
    depends_on('r-rmarkdown@2.4:', type=('build', 'run'), when='@0.21:')
    depends_on('r-rmarkdown@2.9:', type=('build', 'run'), when='@0.24:')
    depends_on('r-jquerylib', type=('build', 'run'), when='@0.24:')
    depends_on('r-xfun@0.6:', type=('build', 'run'))
    depends_on('r-xfun@0.13:', type=('build', 'run'), when='@0.21:')
    depends_on('r-xfun@0.22:', type=('build', 'run'), when='@0.24:')
    depends_on('r-tinytex@0.12:', type=('build', 'run'), when='@0.12:')
    depends_on('r-yaml@2.1.14:', type=('build', 'run'))
    depends_on('r-yaml@2.1.19:', type=('build', 'run'), when='@0.21:')
    depends_on('pandoc@1.17.2:')
