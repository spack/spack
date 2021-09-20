# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sigio(CMakePackage):
    """The SIGIO library provides an Application Program Interface for performing
    I/O on the sigma restart file of the global spectral model."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-sigio"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-sigio/archive/refs/tags/v2.3.2.tar.gz"

    maintainers = ['t-brown']

    version('2.3.2', sha256='333f3cf3a97f97103cbafcafc2ad89b24faa55b1332a98adc1637855e8a5b613')
