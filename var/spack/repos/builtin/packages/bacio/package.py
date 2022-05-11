# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Bacio(CMakePackage):
    """The bacio ibrary performs binary I/O for the NCEP models, processing
    unformatted byte-addressable data records, and transforming the little
    endian files and big endian files."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-bacio"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-bacio/archive/refs/tags/v2.4.1.tar.gz"

    maintainers = ['t-brown', 'edwardhartnett', 'kgerheiser', 'Hang-Lei-NOAA']

    version('2.5.0', sha256='540a0ed73941d70dbf5d7b21d5d0a441e76fad2bfe37dfdfea0db3e98fc0fbfb')

    # Prefer version 2.4.1 because the library and include directory
    # names changed in verion 2.5.0 (dropping the "_4" they used to
    # contain.) We need some time to let all the using packages adjust
    # to the new names.
    version('2.4.1', sha256='7b9b6ba0a288f438bfba6a08b6e47f8133f7dba472a74ac56a5454e2260a7200', preferred=True)
