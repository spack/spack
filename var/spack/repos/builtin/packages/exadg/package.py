# Copyright 2013-2024 Lawrence Livermore National Laboratory and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exadg(CMakePackage):
    """ExaDG - High-Order Discontinuous Galerkin for the Exa-Scale.
    
    ExaDG is a software project written in C++ using state-of-the-art programming
    techniques. The software targets the numerical solution of partial differential
    equations (PDE) in the field of computational fluid dynamics, acoustics, and
    solid mechanics using discontinuous Galerkin methods and matrix-free algorithms.
    """

    homepage = "https://github.com/exadg/exadg"
    git = "https://github.com/exadg/exadg.git"
    url = "https://github.com/exadg/exadg/archive/refs/tags/v1.0.0.tar.gz"

    maintainers("nfehn")

    version("develop", branch="master")
    version("1.0.0", sha256="e8b6b6a8e9e8f9f0f1f2f3f4f5f6f7f8f9f0f1f2f3f4f5f6f7f8f9f0f1f2f3")

    # Variants
    variant("shared", default=True, description="Build shared libraries")
    variant("tests", default=True, description="Build tests")
    variant("fftw", default=False, description="Build with FFTW support")
    variant("likwid", default=False, description="Build with LIKWID support")
    variant("precice", default=False, description="Build with preCICE support")

    # Required dependencies
    depends_on("cmake@3.16:", type="build")
    depends_on("deal.ii@9.7:", type="link")
    depends_on("p4est", type="link")  # Required by deal.II, but explicitly needed

    # Optional dependencies
    depends_on("fftw@3:", type="link", when="+fftw")
    depends_on("likwid", type="link", when="+likwid")
    depends_on("precice@2:", type="link", when="+precice")

    # C++ standard requirements
    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("PICKUP_TESTS", "tests"),
            self.define("CMAKE_CXX_STANDARD", "17"),
        ]

        # deal.II configuration
        deal_ii_spec = self.spec["deal.ii"]
        args.append(self.define("DEAL_II_DIR", deal_ii_spec.prefix))

        # Optional FFTW support
        if "+fftw" in self.spec:
            fftw_spec = self.spec["fftw"]
            args.extend([
                self.define("EXADG_WITH_FFTW", "ON"),
                self.define("FFTW_LIB", fftw_spec.prefix.lib),
                self.define("FFTW_INCLUDE", fftw_spec.prefix.include),
            ])
        else:
            args.append(self.define("EXADG_WITH_FFTW", "OFF"))

        # Optional LIKWID support
        if "+likwid" in self.spec:
            likwid_spec = self.spec["likwid"]
            args.extend([
                self.define("EXADG_WITH_LIKWID", "ON"),
                self.define("LIKWID_LIB", likwid_spec.prefix.lib),
                self.define("LIKWID_INCLUDE", likwid_spec.prefix.include),
            ])
        else:
            args.append(self.define("EXADG_WITH_LIKWID", "OFF"))

        # Optional preCICE support
        if "+precice" in self.spec:
            precice_spec = self.spec["precice"]
            args.extend([
                self.define("EXADG_WITH_PRECICE", "ON"),
                self.define("precice_DIR", precice_spec.prefix),
            ])
        else:
            args.append(self.define("EXADG_WITH_PRECICE", "OFF"))

        return args

    def setup_build_environment(self, env):
        """Set up environment variables needed for the build."""
        spec = self.spec
        env.set("DEAL_II_DIR", spec["deal.ii"].prefix)
