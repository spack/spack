# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RSass(RPackage):
    """Syntactically Awesome Style Sheets ('Sass').

    An 'SCSS' compiler, powered by the 'LibSass' library. With this, R
    developers can use variables, inheritance, and functions to generate
    dynamic style sheets. The package uses the 'Sass CSS' extension language,
    which is stable, powerful, and CSS compatible."""

    cran = "sass"

    version('0.4.0', sha256='7d06ca15239142a49e88bb3be494515abdd8c75f00f3f1b0ee7bccb55019bc2b')

    depends_on('r-fs', type=('build', 'run'))
    depends_on('r-rlang@0.4.10:', type=('build', 'run'))
    depends_on('r-htmltools@0.5.1:', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-rappdirs', type=('build', 'run'))
    depends_on('gmake', type='build')
