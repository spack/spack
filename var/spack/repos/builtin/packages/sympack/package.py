# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sympack(CMakePackage, CudaPackage):
    """symPACK is a sparse symmetric matrix direct linear solver,
    with optional support for CUDA devices"""

    homepage = "https://go.lbl.gov/sympack"
    url = "https://github.com/symPACK/symPACK/archive/refs/tags/v3.0.tar.gz"
    git = "https://github.com/symPACK/symPACK.git"

    maintainers("bonachea")

    version("master", branch="master")

    version("3.0", sha256="bd04284bb6a309a71cd4f9f54f72345ff98fa7ba5719498df1e8a00ef05c41de")
    version("2.0.1", sha256="21c172e902531c94c3bb5932c15de4b4ec9adf9c0d8e2071bb12cdbdfa25ca52")
    version("2.0", sha256="93fcfbadab73718e249e7ed12641a3c6be58b19cafdf6bad12a6a09c3d1eb4a1")

    depends_on("cmake@3.11:", type="build")

    depends_on("upcxx@2019.9.0:")
    depends_on("upcxx@2022.3.0:+cuda", when="+cuda")

    depends_on("mpi")

    variant(
        "cuda",
        default=False,
        when="@3.0:",
        description="Enables solver to offload large operations to CUDA GPUs",
    )
    conflicts("+cuda", when="@:2", msg="symPACK version 3.0 or later required for CUDA support")
    depends_on("cuda@6.0:", when="+cuda")

    variant("scotch", default=False, description="Enable SCOTCH ordering")
    depends_on("scotch~mpi", when="+scotch")

    variant("ptscotch", default=False, description="Enable PT-SCOTCH ordering")
    depends_on("scotch+mpi", when="+ptscotch")

    variant("metis", default=False, description="Enable MeTiS ordering")
    depends_on("metis", when="+metis")

    variant("parmetis", default=False, description="Enable ParMETIS ordering")
    depends_on("parmetis", when="+parmetis")

    build_targets = ["all", "run_sympack2D"]

    def cmake_args(self):
        # UPC++ is picky about what C++ compiler we use:
        meta = join_path(self.spec["upcxx"].prefix.bin, "upcxx-meta")
        cxx = Executable(meta)("CXX", output=str, error=str).strip()
        args = [
            "-DCMAKE_CXX_COMPILER=" + cxx,
            self.define_from_variant("ENABLE_CUDA", "cuda"),
            self.define_from_variant("ENABLE_SCOTCH", "scotch"),
            self.define_from_variant("ENABLE_PTSCOTCH", "ptscotch"),
            self.define_from_variant("ENABLE_METIS", "metis"),
            self.define_from_variant("ENABLE_PARMETIS", "parmetis"),
        ]
        return args

    @run_after("install")
    def finish_install(self):
        # Test driver is not installed by default
        mkdirp(self.prefix.bin)
        install(join_path(self.build_directory, "run_sympack2D"), self.prefix.bin)
