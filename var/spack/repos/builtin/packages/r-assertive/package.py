# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertive(RPackage):
    """assertive: Readable Check Functions to Ensure Code Integrity"""

    homepage = "https://cloud.r-project.org/package=assertive"
    url      = "https://cloud.r-project.org/src/contrib/assertive_0.3-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive"

    version('0.3-6',   sha256='c403169e83c433b65e911f7fd640b378e2a4a4765a36063584b8458168a4ea0a')

    extends('r')
    depends_on('r@3.0.0:', type=('build','run'))
    depends_on('r-assertive-base@0.0-4:', type=('build','run'))
    depends_on('r-assertive-properties@0.0-2:', type=('build','run'))
    depends_on('r-assertive-types@0.0-2:', type=('build','run'))
    depends_on('r-assertive-numbers', type=('build','run'))
    depends_on('r-assertive-strings', type=('build','run'))
    depends_on('r-assertive-datetimes', type=('build','run'))
    depends_on('r-assertive-files', type=('build','run'))
    depends_on('r-assertive-sets@0.0-2:', type=('build','run'))
    depends_on('r-assertive-matrices', type=('build','run'))
    depends_on('r-assertive-models', type=('build','run'))
    depends_on('r-assertive-data', type=('build','run'))
    depends_on('r-assertive-data-uk', type=('build','run'))
    depends_on('r-assertive-data-us', type=('build','run'))
    depends_on('r-assertive-reflection@0.0-2:', type=('build','run'))
    depends_on('r-assertive-code', type=('build','run'))
    depends_on('r-knitr', type=('build','run'))
