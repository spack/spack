# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Maphyspp(CMakePackage):
    """a Massively Parallel Hybrid Solver in C++"""

    homepage = "https://gitlab.inria.fr/solverstack/maphys/maphyspp"
    git = "https://gitlab.inria.fr/solverstack/maphys/maphyspp.git"
    url = "https://gitlab.inria.fr/api/v4/projects/6194/packages/generic/source/v1.1.9/maphyspp-1.1.9.tar.gz"
    maintainers("fpruvost")

    version("master", branch="master", submodules=True)
    version("1.1.9", sha256="472deef05f69c26337a6f8e769cf36cbe0a50e6ec096757389ed10286a0d7e04")

    # User options
    variant("armadillo", default=False, description="Enable Armadillo interface")
    variant("arpack-ng", default=True, description="Enable arpack eigen/singular value solvers")
    variant("eigen", default=True, description="Enable Eigen interface")
    variant("fabulous", default=True, description="Enable Fabulous Iterative Block Krylov solvers")
    variant("paddle", default=True, description="Enable Paddle for matrix partitioning")
    variant("pastix", default=True, description="Enable Pastix sparse direct solver")

    # Executables to compile
    variant("examples", default=True, description="Compile examples")
    variant("tests", default=False, description="Compile tests")

    # Required dependencies
    depends_on("pkgconfig", type="build")
    depends_on("blaspp")
    depends_on("lapackpp")
    depends_on("mpi")

    # Optional dependencies
    depends_on("armadillo", when="+armadillo")
    depends_on("arpack-ng+icb", when="+arpack-ng")
    depends_on("eigen", when="+eigen")
    depends_on("fabulous", when="+fabulous")
    depends_on("paddle", when="+paddle")
    depends_on("pastix+mpi", when="+pastix")

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("MAPHYSPP_C_DRIVER", True),
            self.define("MAPHYSPP_Fortran_DRIVER", True),
            self.define("MAPHYSPP_COMPILE_BENCH", False),
            self.define("MAPHYSPP_USE_MUMPS", False),
            self.define("MAPHYSPP_USE_QRMUMPS", False),
            self.define("MAPHYSPP_USE_SZ_COMPRESSOR", False),
            self.define_from_variant("MAPHYSPP_COMPILE_EXAMPLES", "examples"),
            self.define_from_variant("MAPHYSPP_COMPILE_TESTS", "tests"),
            self.define_from_variant("MAPHYSPP_USE_ARMADILLO", "armadillo"),
            self.define_from_variant("MAPHYSPP_USE_ARPACK", "arpack-ng"),
            self.define_from_variant("MAPHYSPP_USE_EIGEN", "eigen"),
            self.define_from_variant("MAPHYSPP_USE_FABULOUS", "fabulous"),
            self.define_from_variant("MAPHYSPP_USE_PADDLE", "paddle"),
            self.define_from_variant("MAPHYSPP_USE_PASTIX", "pastix"),
        ]

        return args
