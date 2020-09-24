# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FujitsuSsl2(Package):
    """Fujitsu SSL2 (Scientific Subroutine Library II) is Math library
    for Fujitsu compiler.
    Fujitsu SSL2 implementation only for Fujitsu compiler.
    Fujitsu SSL2 provides the function of blas, lapack and scalapack.
    """

    homepage = "https://www.fujitsu.com/us/"
    has_code = False

    variant("parallel", default=True, description="Build with thread-parallel versions")

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
        raise InstallError(
            "Fujitsu SSL2 is not installable; it is vendor supplied \
             You need to specify it as an external package in packages.yaml"
        )

    @property
    def blas_libs(self):
        spec = self.spec
        sharedlibslist = ["libfj90i", "libfj90f", "libfjsrcinfo", "libfj90rt"]
        staticlibslist = []

        if spec.target == "a64fx":  # Build with SVE support
            sharedlibslist += ["libfjlapacksve"]

            if "+parallel" in spec:  # parallel
                staticlibslist = ["libssl2mtexsve"]

            staticlibslist += ["libssl2mtsve", "libfj90rt2", "libfj90fmt_sve"]

        else:  # Build with NEON support
            sharedlibslist += ["libfjlapack"]

            if "+parallel" in spec:  # parallel
                staticlibslist = ["libssl2mtex"]

            staticlibslist += [
                "libssl2mt",
                "libfj90rt2",
                "libfj90fmt"
            ]

        sharedlibs = find_libraries(
            sharedlibslist, self.prefix.lib64, shared=True, recursive=False
        )
        staticlibs = find_libraries(
            staticlibslist, self.prefix.lib64, shared=False, recursive=False
        )
        libs = sharedlibs + staticlibs
        return libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    @property
    def scalapack_libs(self):
        spec = self.spec
        sharedlibslist = [
            "libmpi_usempi_ignore_tkr",
            "libmpi_mpifh",
            "libfj90i",
            "libfj90f",
            "libfjsrcinfo",
            "libfj90rt",
        ]
        staticlibslist = []

        if spec.target == "a64fx":  # Build with SVE support
            sharedlibslist += ["libfjscalapacksve", "libfjlapacksve"]

            if "+parallel" in spec:  # parallel
                staticlibslist = ["libssl2mtexsve"]

            staticlibslist += [
                "libscalapacksve",
                "libssl2mtsve",
                "libfj90rt2",
                "libfj90fmt_sve",
            ]

        else:  # Build with NEON support
            sharedlibslist += ["libfjscalapack", "libfjlapack"]

            if "+parallel" in spec:  # parallel
                staticlibslist = ["libssl2mtex"]

            staticlibslist += [
                "libscalapack",
                "libssl2mt",
                "libfj90rt2",
                "libfj90fmt"
            ]

        sharedlibs = find_libraries(
            sharedlibslist, self.prefix.lib64, shared=True, recursive=False
        )
        staticlibs = find_libraries(
            staticlibslist, self.prefix.lib64, shared=False, recursive=False
        )
        libs = sharedlibs + staticlibs
        return libs

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)
        env.append_flags("fcc_ENV", "-lm -lrt -lpthread -lelf -lz -ldl")
        env.append_flags("FCC_ENV", "-lm -lrt -lpthread -lelf -lz -ldl")
        env.append_flags("FORT90C", "-lm -lrt -lpthread -lelf -lz -ldl")
