# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGoogledrive(RPackage):
    """An Interface to Google Drive.

    Manage Google Drive files from R."""

    cran = "googledrive"

    version('2.0.0', sha256='605c469a6a086ef4b049909c2e20a35411c165ce7ce4f62d68fd39ffed8c5a26')

    depends_on('r@3.3:', type=('build', 'run'))
    depends_on('r-cli@3.0.0:', type=('build', 'run'))
    depends_on('r-gargle@1.2.0:', type=('build', 'run'))
    depends_on('r-glue@1.4.2:', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-lifecycle', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-pillar', type=('build', 'run'))
    depends_on('r-purrr@0.2.3:', type=('build', 'run'))
    depends_on('r-rlang@0.4.9:', type=('build', 'run'))
    depends_on('r-tibble@2.0.0:', type=('build', 'run'))
    depends_on('r-uuid', type=('build', 'run'))
    depends_on('r-vctrs@0.3.0:', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
