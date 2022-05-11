# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Gfsio(CMakePackage):
    """The GFSIO library provides an API to convert GFS Gaussian output into
    grib output.

    This is part of the NOAA NCEPLIBS project."""

    homepage = "https://github.com/NOAA-EMC/NCEPLIBS-gfsio"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-gfsio/archive/refs/tags/v1.4.1.tar.gz"

    maintainers = ['t-brown', 'kgerheiser', 'Hang-Lei-NOAA', 'edwardhartnett']

    version('1.4.1', sha256='eab106302f520600decc4f9665d7c6a55e7b4901fab6d9ef40f29702b89b69b1')

    def setup_run_environment(self, env):
        lib = find_libraries('libgfsio', root=self.prefix, shared=False, recursive=True)
        # Only one library version, but still need to set _4 to make NCO happy
        for suffix in ('4', ''):
            env.set('GFSIO_LIB' + suffix, lib[0])
            env.set('GFSIO_INC' + suffix, join_path(self.prefix, 'include'))

    def flag_handler(self, name, flags):
        if self.spec.satisfies('%fj'):
            if name == 'fflags':
                flags.append('-Free')
        return (None, None, flags)
