# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NceplibsSp(CMakePackage):
    """The spectral transform library (splib) contains FORTRAN
    subprograms to be used for a variety of spectral transform
    functions. This is part of the NCEPLIBS project.

    """

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-sp"
    git      = "git@github.com:NOAA-EMC/NCEPLIBS-sp"

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('v2.3.3')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = ['-DCMAKE_BUILD_TYPE=RELEASE']
        return args
