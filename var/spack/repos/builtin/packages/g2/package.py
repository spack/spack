# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class G2(CMakePackage):
    """Utilities for coding/decoding GRIB2 messages. This library contains
    Fortran 90 decoder/encoder routines for GRIB edition 2, as well as
    indexing/searching utility routines.

    This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-g2"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-g2/archive/refs/tags/v3.4.3.tar.gz"

    maintainers = ['t-brown', 'kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    version('3.4.5', sha256='c18e991c56964953d778632e2d74da13c4e78da35e8d04cb742a2ca4f52737b6')
    version('3.4.3', sha256='679ea99b225f08b168cbf10f4b29f529b5b011232f298a5442ce037ea84de17c')

    depends_on('jasper')
    depends_on('libpng')

    def setup_run_environment(self, env):
        for suffix in ('4', 'd'):
            lib = find_libraries('libg2_' + suffix, root=self.prefix,
                                 shared=False, recursive=True)
            env.set('G2_LIB' + suffix, lib[0])
            env.set('G2_INC' + suffix, join_path(self.prefix, 'include_' + suffix))
