# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class G2tmpl(CMakePackage):
    """Utilities for GRIB2 templates."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-g2tmpl"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-g2tmpl/archive/refs/tags/v1.10.0.tar.gz"

    maintainers = ['t-brown']

    version('1.10.0', sha256='dcc0e40b8952f91d518c59df7af64e099131c17d85d910075bfa474c8822649d')
