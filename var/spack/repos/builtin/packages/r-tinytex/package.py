# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTinytex(RPackage):
    """Helper Functions to Install and Maintain TeX Live, and Compile LaTeX
    Documents.

    Helper functions to install and maintain the 'LaTeX' distribution named
    'TinyTeX' (<https://yihui.name/tinytex/>), a lightweight, cross-platform,
    portable, and easy-to-maintain version of 'TeX Live'. This package also
    contains helper functions to compile 'LaTeX' documents, and install missing
    'LaTeX' packages automatically."""

    cran = "tinytex"

    version('0.37', sha256='2f4f330711fd6cd96927c18f2f649487b8a83a06ed04b5928a0067163e7948d9')
    version('0.36', sha256='65e6c1b981686573dd406e97b9639224cc2640d55a59d6381360449f10763b78')
    version('0.32', sha256='70fa28195ae6c8b8d43790205b49745c5a062aab78e64cec39bfbe5ed604c29f')
    version('0.28', sha256='76a0650aeab04eb252dc9cfa9ba855d88b09dfc2207c4a8ea2ea04fa0e0eea86')
    version('0.15', sha256='5d0988d3b7f763dfa65c722f177452a21344e428415a4b31aeb51478f0abad90')

    depends_on('r-xfun@0.5:', type=('build', 'run'))
    depends_on('r-xfun@0.19:', type=('build', 'run'), when='@0.28:')
    depends_on('r-xfun@0.23:', type=('build', 'run'), when='@0.32:')
    depends_on('r-xfun@0.29:', type=('build', 'run'), when='@0.36:')
