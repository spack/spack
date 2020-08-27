# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGh(RPackage):
    """Minimal client to access the 'GitHub' 'API'."""

    homepage = "https://github.com/r-lib/gh#readme"
    url      = "https://cloud.r-project.org/src/contrib/gh_1.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gh"

    version('1.0.1', sha256='f3c02b16637ae390c3599265852d94b3de3ef585818b260d00e7812595b391d2')

    depends_on('r-ini', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
