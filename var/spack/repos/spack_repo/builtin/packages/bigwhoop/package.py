# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Bigwhoop(CMakePackage):
    """BigWhoop is a lossy compression algorithm for numerical
    datasets from HPC engineering applications.
    """

    homepage = "https://github.com/ptvogler/BigWhoop"
    url = "https://github.com/ptvogler/BigWhoop/archive/refs/tags/v0.2.0.tar.gz"
    git = "https://github.com/ptvogler/BigWhoop.git"

    maintainers("ptvogler", "gregorweiss")

    license("BSD-2-Clause", checked_by="ptvogler")

    version("main", branch="main")
    version("0.2.0", sha256="48e6aeaf9c6d39c18c030397e0cb46c43491cbf64400dda1efb4293696716692")

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    depends_on("cmake@3.5.1:", type="build")
    depends_on("python", type="build")

    # Build targets
    variant("shared", default=True, description="Build shared libraries")
    variant("utilities", default=False, description="Build bigwhoop utilities")

    # Execution policies
    variant("openmp", default=True, description="Enable OpenMP execution")

    # Advanced settings
    variant("profiling", default=False, description="Enable profiling")
    variant("precision", default="Double", description="Enable double precision")

    # CMake options
    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_UTILITIES", "utilities"),
            self.define_from_variant("BIGWHOOP_WITH_OPENMP", "openmp"),
            self.define_from_variant("BIGWHOOP_WITH_PROFILING", "profiling"),
            self.define("BIGWHOOP_PRECISION", spec.variants["precision"].value),
        ]

        return args
