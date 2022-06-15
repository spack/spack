# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ip2(CMakePackage):
    """The NCEP general interpolation library 2 (ip2lib) contains Fortran
    90 subprograms to be used for interpolating between nearly all
    grids used at NCEP. This library is deprecated; all functionality
    has been moved to the ip library.

    This is part of the NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-ip2"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-ip2/archive/refs/tags/v1.1.2.tar.gz"

    maintainers = ['t-brown', 'kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    version('1.1.2', sha256='73c6beec8fd463ec7ccba3633d8c5d53d385c43d507367efde918c2db0af42ab')

    depends_on('sp')

    def setup_run_environment(self, env):
        for suffix in ('4', '8', 'd'):
            lib = find_libraries('libip2_' + suffix, root=self.prefix,
                                 shared=False, recursive=True)
            env.set('IP2_LIB' + suffix, lib[0])
            env.set('IP2_INC' + suffix, join_path(self.prefix, 'include_' + suffix))
