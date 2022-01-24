# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ProdUtil(CMakePackage):
    """
    Product utilities for the NCEP models.

    This is part of NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-prod_util"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-prod_util/archive/refs/tags/v1.2.2.tar.gz"

    maintainers = ['kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    version('1.2.2', sha256='c51b903ea5a046cb9b545b5c04fd28647c58b4ab6182e61710f0287846350ef8')

    depends_on('w3nco')
