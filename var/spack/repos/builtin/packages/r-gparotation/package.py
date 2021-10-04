# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGparotation(RPackage):
    """Gradient Projection Algorithm Rotation for Factor Analysis. See
    ?GPArotation.Intro for more details."""

    homepage = "https://cloud.r-project.org/package=GPArotation"
    url      = "https://cloud.r-project.org/src/contrib/GPArotation_2014.11-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/GPArotation"

    version('2014.11-1', sha256='351bc15fc8dc6c8ea5045fbba22180d1e68314fc34d267545687748e312e5096')

    depends_on('r@2.0.0:', type=('build', 'run'))
