# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGparotation(RPackage):
    """GPA Factor Rotation.

    Gradient Projection Algorithm Rotation for Factor Analysis. See
    GPArotation.Intro for more details."""

    cran = "GPArotation"

    version('2014.11-1', sha256='351bc15fc8dc6c8ea5045fbba22180d1e68314fc34d267545687748e312e5096')

    depends_on('r@2.0.0:', type=('build', 'run'))
