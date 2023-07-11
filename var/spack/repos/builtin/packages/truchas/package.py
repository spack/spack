# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Truchas(CMakePackage):
    """Physics-based modeling and simulation of manufacturing processes.

    Truchas includes coupled physics models for incompressible multi-material
    flow with interface tracking, heat transfer, phase change, view factor
    thermal radiation, species advection-diffusion, elastic/plastic mechanics
    with contact, and electromagnetics. It employs finite volume, finite element,
    and mimetic finite difference discretizations on 3-D unstructured meshes
    composed of mixed cell types.
    """

    homepage = "https://www.truchas.org"
    url = "https://gitlab.com/truchas/truchas/-/archive/22.04.1/truchas-22.04.1.tar.bz2"
    git = "https://gitlab.com/truchas/truchas.git"

    maintainers("pbrady")

    version("develop", branch="master")
    version("22.04.1", sha256="ed2000f27ee5c4bd3024063a374023878c61e8a3c76c37542fffd341d1226dc1")

    # ------------------------------------------------------------ #
    # Variants
    # ------------------------------------------------------------ #

    variant("portage", default=False, description="use the portage data mapping tool")
    variant("metis", default=True, description="use metis for grid partitioning")
    variant("std_name", default=False, description="enable std_mod_proc_name with intel")
    variant("config", default=True, description="use proved truchas config files for cmake")

    # ------------------------------------------------------------ #
    # Build dependencies
    # ------------------------------------------------------------ #
    depends_on("cmake@3.16:", type="build")

    # ------------------------------------------------------------ #
    # Test suite and restart utils
    # ------------------------------------------------------------ #
    depends_on("python@3.5:")
    depends_on("py-numpy@1.12:")
    depends_on("py-h5py")

    # ------------------------------------------------------------ #
    # IO dependencies
    # ------------------------------------------------------------ #
    depends_on("exodusii@2020-05-12: +mpi")
    depends_on("scorpio")
    depends_on("petaca@22.03: +shared")
    depends_on("petaca@22.03: +shared +std_name", when="+std_name")

    # ------------------------------------------------------------ #
    # Partitioning
    # ------------------------------------------------------------ #
    depends_on("chaco")
    depends_on("metis@5:", when="+metis")

    # ------------------------------------------------------------ #
    # Radiation
    # ------------------------------------------------------------ #
    depends_on("chaparral +mpi")

    # ------------------------------------------------------------ #
    # Solvers
    # ------------------------------------------------------------ #
    depends_on("hypre@2.20: ~fortran")

    # ------------------------------------------------------------ #
    # Mapping
    # ------------------------------------------------------------ #
    depends_on("portage@3:", when="+portage")

    def cmake_args(self):
        # baseline config args
        opts = [
            self.define_from_variant("USE_METIS", "metis"),
            self.define_from_variant("USE_PORTAGE", "portage"),
            self.define_from_variant("ENABLE_STD_MOD_PROC_NAME", "std_name"),
        ]

        spec = self.spec
        if "+config" in spec:
            root = self.root_cmakelists_dir

            nag = "nag" in self.compiler.fc

            if spec.satisfies("platform=linux"):
                if nag or "%nag" in spec:
                    opts.append("-C {}/config/linux-nag.cmake".format(root))
                elif "%gcc" in spec:
                    opts.append("-C {}/config/linux-gcc.cmake".format(root))
                elif "%intel" in spec:
                    opts.append("-C {}/config/linux-intel.cmake".format(root))

            elif spec.satisfies("platform=darwin"):
                if nag or "%nag" in spec:
                    opts.append("-C {}/config/mac-nag.cmake".format(root))

            if self.spec.satisfies("%apple-clang@12:"):
                opts.append(
                    self.define("CMAKE_C_FLAGS", "-Wno-error=implicit-function-declaration")
                )

        return opts
