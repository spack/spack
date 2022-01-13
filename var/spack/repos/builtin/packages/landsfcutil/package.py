# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Landsfcutil(CMakePackage):
    """Utility routines useful for initializing land-surface states in
    NCEP models.

    This is part of NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-landsfcutil"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-landsfcutil/archive/refs/tags/v2.4.1.tar.gz"

    maintainers = ['edwardhartnett', 'kgerheiser', 'Hang-Lei-NOAA']

    version('2.4.1', sha256='831c5005a480eabe9a8542b4deec838c2650f6966863ea2711cc0cc5db51ca14')
