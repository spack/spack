# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RQuestionr(RPackage):
    """Set of functions to make the processing and analysis of surveys easier :
    interactive shiny apps and addins for data recoding, contingency tables,
    dataset metadata handling, and several convenience functions."""

    homepage = "https://cloud.r-project.org/package=questionr"
    url      = "https://cloud.r-project.org/src/contrib/questionr_0.7.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/questionr"

    version('0.7.4', sha256='818ad87723aa7ebe466b3a639c9e86b7f77e6a341c8d9a933073925a21d4555c')

    depends_on('r@3.5.0:',          type=('build', 'run'))
    depends_on('r-shiny@1.0.5:',    type=('build', 'run'))
    depends_on('r-miniui',          type=('build', 'run'))
    depends_on('r-rstudioapi',      type=('build', 'run'))
    depends_on('r-highr',           type=('build', 'run'))
    depends_on('r-styler',          type=('build', 'run'))
    depends_on('r-classint',        type=('build', 'run'))
    depends_on('r-htmltools',       type=('build', 'run'))
    depends_on('r-labelled@2.6.0:', type=('build', 'run'))
