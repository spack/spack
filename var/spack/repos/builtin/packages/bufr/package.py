# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Bufr(CMakePackage):
    """The NOAA bufr library contains subroutines, functions and other
    utilities that can be used to read (decode) and write (encode)
    data in BUFR, which is a WMO standard format for the exchange of
    meteorological data. This is part of the NCEPLIBS project.

    """

    homepage = "https://noaa-emc.github.io/NCEPLIBS-bufr"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-bufr/archive/refs/tags/bufr_v11.5.0.tar.gz"

    maintainers = ['t-brown', 'kgerheiser', 'edwardhartnett', 'Hang-Lei-NOAA',
                   'jbathegit']

    version('11.5.0', sha256='d154839e29ef1fe82e58cf20232e9f8a4f0610f0e8b6a394b7ca052e58f97f43')

    def _setup_bufr_environment(self, env, suffix):
        libname = 'libufr_{0}'.format(suffix)
        lib = find_libraries(libname, root=self.prefix,
                             shared=False, recursive=True)
        lib_envname = 'BUFR_LIB{0}'.format(suffix)
        inc_envname = 'BUFR_INC{0}'.format(suffix)
        include_dir = 'include_{0}'.format(suffix)

        env.set(lib_envname, lib[0])
        env.set(inc_envname, include_dir)

        # Bufr has _DA (dynamic allocation) libs in versions <= 11.5.0
        if self.spec.satisfies('@:11.5.0'):
            da_lib = find_libraries(libname + "_DA", root=self.prefix,
                                    shared=False, recursive=True)
            env.set(lib_envname + '_DA', da_lib[0])
            env.set(inc_envname + '_DA', include_dir)

    def setup_run_environment(self, env):
        for suffix in ('4', '8', 'd'):
            self._setup_bufr_environment(env, suffix)
