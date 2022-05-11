# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQuestionr(RPackage):
    """Functions to Make Surveys Processing Easier.

    Set of functions to make the processing and analysis of surveys easier:
    interactive shiny apps and addins for data recoding, contingency tables,
    dataset metadata handling, and several convenience functions."""

    cran = "questionr"

    version('0.7.7', sha256='ce24c40bd98dbeca615b9eb2a9cd2da26852821dc3840f8394eeecb0739dfd56')
    version('0.7.6', sha256='4b71d049d9e032157e12a7809dbfa2a39262b49d0c7a03ed434791a66f0cee5e')
    version('0.7.4', sha256='818ad87723aa7ebe466b3a639c9e86b7f77e6a341c8d9a933073925a21d4555c')

    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-shiny@1.0.5:', type=('build', 'run'))
    depends_on('r-miniui', type=('build', 'run'))
    depends_on('r-rstudioapi', type=('build', 'run'))
    depends_on('r-highr', type=('build', 'run'))
    depends_on('r-styler', type=('build', 'run'))
    depends_on('r-classint', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-labelled@2.6.0:', type=('build', 'run'))
    depends_on('xclip', when='platform=linux')
