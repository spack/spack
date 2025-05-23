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
    git = "https://github.com/nomad-coe/greenX.git"

    maintainers("RMeli")

    license("Apache-2.0", checked_by="RMeli")

    version("main", branch="main")
    version("2.2", sha256="cf0abb77cc84a3381a690a6ac7ca839da0007bb9e6120f3f25e47de50e29431f")
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

    # fix a missing dependency in the greenXConfig.cmake file.
    # A linking error will show up when clang is used.
    # fix fortran modules installation paths
    patch(
        "https://github.com/nomad-coe/greenX/commit/96c4b61656c13b5aceb2906ad5efb93a745dc6ae.patch?full_index=1",
        sha256="6d591e223be462137a1563cfcf99ab721c896a79eb139baf32c49995d2a2be7c",
        when="@:2.3",
    )

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
