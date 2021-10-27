# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RReams(RPackage):
    """reams: Resampling-Based Adaptive Model Selection"""

    homepage = "https://cloud.r-project.org/package=reams"
    url      = "https://cloud.r-project.org/src/contrib/reams_0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/reams"

    version('0.1', sha256='ac24ea875b24bd18152afd87538b1f807f442cf2bd1c6ac1a365cf543c88181e')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on('r-leaps', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
