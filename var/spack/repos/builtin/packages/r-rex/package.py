# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRex(RPackage):
    """A friendly interface for the construction of regular expressions."""

    homepage = "https://cloud.r-project.org/package=rex"
    url      = "https://cloud.r-project.org/src/contrib/rex_1.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rex"

    version('1.1.2', '8820b4d4fe3718f275847b6f2cf83689')

    depends_on('r-lazyeval', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
