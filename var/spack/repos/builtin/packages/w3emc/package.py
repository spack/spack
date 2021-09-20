# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class W3emc(CMakePackage):
    """This library contains Fortran 90 decoder/encoder routines for GRIB
    edition 1 with EMC changes."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-w3emc/"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-w3emc/archive/refs/tags/v2.9.0.tar.gz"

    maintainers = ['t-brown']

    version('2.9.0', sha256='994f59635ab91e34e96cab5fbaf8de54389d09461c7bac33b3104a1187e6c98a')
