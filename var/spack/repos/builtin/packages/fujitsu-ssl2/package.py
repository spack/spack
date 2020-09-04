# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FujitsuSsl2(Package):
    """Fujitsu SSL2 (Scientific Subroutine Library II) is Math library for Fujitsu compiler.
    Fujitsu SSL2 implementation only for Fujitsu compiler.
    Fujitsu SSL2 provides the function of blas, lapack and scalapack.
    """

    homepage = "https://www.fujitsu.com/us/"

    conflicts("%arm")
    conflicts("%cce")
    conflicts("%apple-clang")
    conflicts("%clang")
    conflicts("%gcc")
    conflicts("%intel")
    conflicts("%nag")
    conflicts("%pgi")
    conflicts("%xl")
    conflicts("%xl_r")

    provides("blas")
    provides("lapack")
    provides("scalapack")

    def install(self, spec, prefix):
        raise InstallError("Fujitsu SSL2 is not installable; it is vendor supplied")

    @property
    def libs(self):
        sharedlibs = find_libraries(
            [
                "libfjlapack",
                "libfj90i",
                "libfj90f",
                "libfjsrcinfo",
                "libfj90rt",
            ],
            self.prefix.lib64,
            shared=True,
            recursive=False
        )
        staticlibs = find_libraries(
            [
                "libssl2mt",
                "libssl2mtex",
                "libfj90rt2",
                "libfj90fmt",
            ],
            self.prefix.lib64,
            shared=False,
            recursive=False
        )
        libs = sharedlibs + staticlibs
        return libs

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)
        env.append_flags("fcc_ENV", "-lm -lrt -lpthread -lelf -lz -ldl")
        env.append_flags("FCC_ENV", "-lm -lrt -lpthread -lelf -lz -ldl")
        env.append_flags("FORT90C", "-lm -lrt -lpthread -lelf -lz -ldl")
