# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHtmltools(RPackage):
    """Tools for HTML

    Tools for HTML generation and output."""

    homepage = "https://github.com/rstudio/htmltools"
    cran     = "htmltools"

    version('0.5.1.1', sha256='f0bfe72ffe330f3d6c9ead5857f3a4aef80e002e32558074a3e643f2ab67a4ba')
    version('0.5.1', sha256='6ac82e4451f9558ceb541ea659a736b2ab3245827832b44d3661e7a4d91f6307')
    version('0.3.6', sha256='44affb82f9c2fd76c9e2b58f9229adb003217932b68c3fdbf1327c8d74c868a2')
    version('0.3.5', sha256='29fb7e075744bbffdff8ba4fce3860076de66f39a59a100ee4cfb4fc00722b49')

    depends_on('r@2.14.1:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-base64enc', when='@0.5.1:', type=('build', 'run'))
    depends_on('r-rlang', when='@0.5.1:', type=('build', 'run'))
    depends_on('r-rcpp', when=' @:0.3.6', type=('build', 'run'))
