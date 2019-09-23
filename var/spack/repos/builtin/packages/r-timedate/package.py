# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTimedate(RPackage):
    """Environment for teaching "Financial Engineering and Computational
    Finance". Managing chronological and calendar objects."""

    homepage = "https://cloud.r-project.org/package=timeDate"
    url      = "https://cloud.r-project.org/src/contrib/timeDate_3012.100.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/timeDate"

    version('3043.102', sha256='377cba03cddab8c6992e31d0683c1db3a73afa9834eee3e95b3b0723f02d7473')
    version('3042.101', sha256='6c8d4c7689b31c6a43555d9c7258516556ba03b132e5643691e3e317b89a8c6d')
    version('3012.100', '9f69d3724efbf0e125e6b8e6d3475fe4')

    depends_on('r@2.15.1:', type=('build', 'run'))
