# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bacio(CMakePackage):
    """The bacio ibrary performs binary I/O for the NCEP models, processing
    unformatted byte-addressable data records, and transforming the little
    endian files and big endian files."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-bacio"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-bacio/archive/refs/tags/v2.4.1.tar.gz"

    maintainers = ['t-brown']

    version('2.4.1', sha256='7b9b6ba0a288f438bfba6a08b6e47f8133f7dba472a74ac56a5454e2260a7200')
