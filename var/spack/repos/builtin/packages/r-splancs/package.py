# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSplancs(RPackage):
    """Spatial and Space-Time Point Pattern Analysis"""

    homepage = "https://cloud.r-project.org/package=splancs"
    url      = "https://cloud.r-project.org/src/contrib/splancs_2.01-40.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/splancs"

    version('2.01-40', 'dc08a5c9a1fd2098d78459152f4917ce')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-sp@0.9:', type=('build', 'run'))
