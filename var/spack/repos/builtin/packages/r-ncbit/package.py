# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNcbit(RPackage):
    """Making NCBI taxonomic data locally available and searchable as an R
       object."""

    homepage = "https://cloud.r-project.org/package=ncbit"
    url      = "https://cloud.r-project.org/src/contrib/ncbit_2013.03.29.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ncbit"

    version('2013.03.29', '29582d7e5c8bbf9683c57c4f6ac3e891')

    depends_on('r@2.10:', type=('build', 'run'))
