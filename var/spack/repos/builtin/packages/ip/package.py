# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ip(CMakePackage):
    """The NCEP general interpolation library (iplib) contains Fortran 90
    subprograms to be used for interpolating between nearly all grids used at
    NCEP. This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-ip"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-ip/archive/refs/tags/v3.3.3.tar.gz"

    maintainers = ['t-brown', 'kgerheiser', 'edwardhartnett', 'Hang-Lei-NOAA']

    version('4.0.0', sha256='a2ef0cc4e4012f9cb0389fab6097407f4c623eb49772d96eb80c44f804aa86b8')
    version('3.3.3', sha256='d5a569ca7c8225a3ade64ef5cd68f3319bcd11f6f86eb3dba901d93842eb3633', preferred=True)

    depends_on('sp')

    def setup_run_environment(self, env):
        for suffix in ('4', '8', 'd'):
            lib = find_libraries('libip_4', root=self.prefix,
                                 shared=False, recursive=True)
            env.set('IP_LIB' + suffix, lib[0])
            env.set('IP_INC' + suffix, join_path(self.prefix, 'include_' + suffix))
