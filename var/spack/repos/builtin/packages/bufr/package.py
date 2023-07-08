# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bufr(CMakePackage):
    """The NOAA bufr library contains subroutines, functions and other
    utilities that can be used to read (decode) and write (encode)
    data in BUFR, which is a WMO standard format for the exchange of
    meteorological data. This is part of the NCEPLIBS project.

    """

    homepage = "https://noaa-emc.github.io/NCEPLIBS-bufr"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-bufr/archive/refs/tags/bufr_v11.5.0.tar.gz"

    maintainers("t-brown", "AlexanderRichert-NOAA", "edwardhartnett", "Hang-Lei-NOAA", "jbathegit")

    version("11.7.1", sha256="6533ce6eaa6b02c0cb5424cfbc086ab120ccebac3894980a4daafd4dfadd71f8")
    version("11.7.0", sha256="6a76ae8e7682bbc790321bf80c2f9417775c5b01a5c4f10763df92e01b20b9ca")
    version("11.6.0", sha256="af4c04e0b394aa9b5f411ec5c8055888619c724768b3094727e8bb7d3ea34a54")
    version("11.5.0", sha256="d154839e29ef1fe82e58cf20232e9f8a4f0610f0e8b6a394b7ca052e58f97f43")

    def _setup_bufr_environment(self, env, suffix):
        libname = "libbufr_{0}".format(suffix)
        lib = find_libraries(libname, root=self.prefix, shared=False, recursive=True)
        lib_envname = "BUFR_LIB{0}".format(suffix)
        inc_envname = "BUFR_INC{0}".format(suffix)
        include_dir = "include_{0}".format(suffix)

        env.set(lib_envname, lib[0])
        env.set(inc_envname, include_dir)

        # Bufr has _DA (dynamic allocation) libs in versions <= 11.5.0
        if self.spec.satisfies("@:11.5.0"):
            da_lib = find_libraries(
                libname + "_DA", root=self.prefix, shared=False, recursive=True
            )
            env.set(lib_envname + "_DA", da_lib[0])
            env.set(inc_envname + "_DA", include_dir)

    def setup_run_environment(self, env):
        for suffix in ("4", "8", "d"):
            self._setup_bufr_environment(env, suffix)
