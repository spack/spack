# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class WrfIo(CMakePackage):
    """The WRFIO package is a lightweight WRF-IO API library for Unified
    Post Processor (UPP). It reads wrf forecasts (WRF state plus
    diagnostics)."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-wrf_io"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-wrf_io/archive/refs/tags/v1.2.0.tar.gz"

    maintainers = ['t-brown']

    version('1.2.0', sha256='000cf5294a2c68460085258186e1f36c86d3d0d9c433aa969a0f92736b745617')

    depends_on('netcdf-c')
    depends_on('netcdf-fortran')
