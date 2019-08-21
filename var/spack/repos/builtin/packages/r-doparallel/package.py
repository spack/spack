# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDoparallel(RPackage):
    """Provides a parallel backend for the %dopar% function using the parallel
    package."""

    homepage = "https://cloud.r-project.org/package=doParallel"
    url      = "https://cloud.r-project.org/src/contrib/doParallel_1.0.10.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/doParallel"

    version('1.0.15', sha256='71ad7ea69616468996aefdd8d02a4a234759a21ddde9ed1657e3c537145cd86e')
    version('1.0.11', 'd7822f0efd7bdf7582d8b43c986be86c')
    version('1.0.10', 'd9fbde8f315d98d055483ee3493c9b43')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-foreach@1.2.0:', type=('build', 'run'))
    depends_on('r-iterators@1.0.0:', type=('build', 'run'))
