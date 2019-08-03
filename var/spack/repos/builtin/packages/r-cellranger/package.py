# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCellranger(RPackage):
    """Helper functions to work with spreadsheets and the "A1:D10"
    style of cell range specification."""

    homepage = "https://cloud.r-project.org/package=cellranger"
    url      = "https://cloud.r-project.org/src/contrib/cellranger_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/cellranger"

    version('1.1.0', '1abcfea6af5ab2e277cb99e86880456f')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-rematch', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
