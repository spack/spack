# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Greenx(CMakePackage):
    """GreenX: An open-source library that supports exascale implementations
    of Green's-function-based methodologies."""

    homepage = "https://nomad-coe.github.io/greenX"
    url = "https://github.com/nomad-coe/greenX/archive/refs/tags/v2.1.tar.gz"

    maintainers("RMeli")

    license("Apache-2.0", checked_by="RMeli")

    version("2.1", sha256="2fc1fc2c93b0bab14babc33386f7932192336813cea6db11cd27dbc36b541e41")

    variant("shared", default=True, description="Build shared libraries")
    variant("ac", default=True, description="Enable Analytical Continuation component")
    variant(
        "gmp",
        when="+ac",
        default=True,
        description="Enable GMP library for multiple precision arithmetic",
    )
    variant("minmax", default=True, description="Enable minmax time-frequency grids component")
    variant("lbasis", default=False, description="Enable localized basis component")
    variant("paw", default=False, description="Enable PAW component")

    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    depends_on("blas")
    depends_on("lapack")

    depends_on("gmp", when="+gmp")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("AC_COMPONENT", "ac"),
            self.define_from_variant("ENABLE_GNU_GMP", "gmp"),
            self.define_from_variant("MINMAX_COMPONENT", "minmax"),
            self.define_from_variant("LBASIS_COMPONENT", "lbasis"),
            self.define_from_variant("PAW_COMPONENT", "paw"),
        ]
        return args
