# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLubridate(RPackage):
    """Functions to work with date-times and timespans: fast and user friendly
    parsing of date-time data, extraction and updating of components of a
    date-time (years, months, days, hours, minutes, and seconds), algebraic
    manipulation on date-time and timespan objects. The 'lubridate' package has
    a consistent and memorable syntax that makes working with dates easy and
    fun."""

    homepage = "https://cloud.r-project.org/package=lubridate"
    url      = "https://cloud.r-project.org/src/contrib/lubridate_1.7.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lubridate"

    version('1.7.4', sha256='510ca87bd91631c395655ee5029b291e948b33df09e56f6be5839f43e3104891')
    version('1.7.3', sha256='2cffbf54afce1d068e65241fb876a77b10ee907d5a19d2ffa84d5ba8a2c3f3df')
    version('1.7.1', '17dcb4c6a95189941bbdcffecf61b83b')
    version('1.5.6', 'a5dc44817548ee219d26a10bae92e611')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.13:', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
