# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nemsiogfs(CMakePackage):
    """
    Performs I/O for the NEMS-GFS model.

    This is part of NOAA's NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-nemsiogfs"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-nemsiogfs/archive/refs/tags/v2.5.3.tar.gz"

    maintainers = ['kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    version('2.5.3', sha256='bf84206b08c8779787bef33e4aba18404df05f8b2fdd20fc40b3af608ae4b9af')

    depends_on('nemsio')
