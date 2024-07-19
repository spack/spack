# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libgain(AutotoolsPackage):
    """GaIn is intended to provide routines with a relatively simple interface
    for calculation of overlap, kinetic and 2,3 and 4 center Coulomb integrals
    over either Solid or Cubic Harmonics Gaussian basis sets."""

    homepage = "https://bigdft.org/"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    license("GPL-3.0-only")

    version(
        "1.0.0",
        sha256="3e02637433272f5edfee74ea47abf93ab7e3f1ce717664d22329468a5bd45c3a",
        url="https://gitlab.com/l_sim/bigdft-suite/-/raw/1.9.1/GaIn-1.0.tar.gz",
    )
    variant(
        "shared", default=True, description="Build shared libraries"
    )  # Not default in bigdft, but is typically the default expectation

    def configure_args(self):
        fcflags = []
        cflags = []
        cxxflags = []

        if self.spec.satisfies("+shared"):
            fcflags.append("-fPIC")
            cflags.append("-fPIC")
            cxxflags.append("-fPIC")

        args = [
            f"FCFLAGS={' '.join(fcflags)}",
            f"CFLAGS={' '.join(cflags)}",
            f"CXXFLAGS={' '.join(cxxflags)}",
        ]
        return args

    depends_on("fortran", type="build")  # generated

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libGaIn", root=self.prefix, shared=shared, recursive=True)
