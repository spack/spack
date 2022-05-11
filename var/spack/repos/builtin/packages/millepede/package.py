# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Millepede(MakefilePackage):
    """Millepede II is a package for linear least squares fits
       with a large number of parameters. Developed for the
       alignment and calibration of tracking detectors."""

    homepage = "https://gitlab.desy.de/claus.kleinwort/millepede-ii"
    url      = "https://gitlab.desy.de/claus.kleinwort/millepede-ii/-/archive/V04-11-01/millepede-ii-V04-11-01.tar.gz"

    maintainers = ['iarspider']

    parallel = False

    version('04-11-01', sha256='9869eb84d8d07cecfab15c396f3faa36aef10906e39f8641c48b58e0325b3205')

    depends_on('zlib')
