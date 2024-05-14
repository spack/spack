# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FenicsDolfinx(CMakePackage):
    """Next generation FEniCS problem solving environment"""

    homepage = "https://github.com/FEniCS/dolfinx"
    git = "https://github.com/FEniCS/dolfinx.git"
    url = "https://github.com/FEniCS/dolfinx/archive/v0.1.0.tar.gz"
    maintainers("chrisrichardson", "garth-wells", "nate-sime", "jhale")

    license("LGPL-3.0-or-later")

    version("main", branch="main")
    version("0.8.0", sha256="acf3104d9ecc0380677a6faf69eabfafc58d0cce43f7777e1307b95701c7cad9")
    version("0.7.2", sha256="7d9ce1338ce66580593b376327f23ac464a4ce89ef63c105efc1a38e5eae5c0b")
    version("0.6.0", sha256="eb8ac2bb2f032b0d393977993e1ab6b4101a84d54023a67206e3eac1a8d79b80")
    version(
        "0.5.1",
        sha256="a570e3f6ed8e7c570e7e61d0e6fd44fa9dad2c5f8f1f48a6dc9ad22bacfbc973",
        deprecated=True,
    )
    version(
        "0.5.0",
        sha256="503c70c01a44d1ffe48e052ca987693a49f8d201877652cabbe2a44eb3b7c040",
        deprecated=True,
    )
    version(
        "0.4.1",
        sha256="68dcf29a26c750fcea5e02d8d58411e3b054313c3bf6fcbc1d0f08dd2851117f",
        deprecated=True,
    )

    conflicts(
        "%gcc@:9.10",
        when="@0.5.0:",
        msg="fenics-dolfinx requires GCC-10 or newer for C++20 support",
    )
    conflicts(
        "%clang@:9.10",
        when="@0.5.0:",
        msg="fenics-dolfinx requires Clang-10 or newer for C++20 support",
    )

    # Graph partitioner variants
    variant(
        "partitioners",
        description="Graph partioning",
        default=("parmetis",),
        values=("kahip", "parmetis", "scotch"),
        multi=True,
    )

    # Graph partitioner dependencies
    depends_on("kahip@3.12:", when="partitioners=kahip @0.5.0:")
    depends_on("kahip@3.11", when="partitioners=kahip @:0.4.1")
    depends_on("parmetis", when="partitioners=parmetis")
    depends_on("scotch+mpi", when="partitioners=scotch")

    variant("slepc", default=False, description="slepc support")
    variant("adios2", default=False, description="adios2 support")

    depends_on("cmake@3.19:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("mpi")
    depends_on("hdf5+mpi")
    depends_on("boost@1.7.0:+filesystem+program_options+timer")

    depends_on("petsc+mpi+shared")

    depends_on("xtensor@0.23.10:", when="@:0.5")
    depends_on("xtl@0.7.2:", when="@:0.5")

    depends_on("slepc", when="+slepc")
    depends_on("adios2+mpi", when="+adios2")
    depends_on("pugixml", when="@0.5.0:")

    depends_on("fenics-ufcx@main", when="@main")
    depends_on("fenics-ufcx@0.8", when="@0.8")
    depends_on("fenics-ufcx@0.7", when="@0.7")
    depends_on("fenics-ufcx@0.6.0:0.6", when="@0.6.0:0.6")
    depends_on("fenics-ufcx@0.5.0", when="@0.5.1:0.5")
    depends_on("fenics-ufcx@0.4.2", when="@0.4.1")

    depends_on("fenics-basix@main", when="@main")
    depends_on("fenics-basix@0.8", when="@0.8")
    depends_on("fenics-basix@0.7", when="@0.7")
    depends_on("fenics-basix@0.6.0:0.6", when="@0.6.0:0.6")
    depends_on("fenics-basix@0.5.1:0.5", when="@0.5.0:0.5")
    depends_on("fenics-basix@0.4.2", when="@0.4.1")

    conflicts(
        "%gcc@:9.10",
        when="@0.5.0:",
        msg="fenics-dolfinx requires GCC-10 or newer for C++20 support",
    )
    conflicts(
        "%clang@:9.10",
        when="@0.5.0:",
        msg="fenics-dolfinx requires Clang-10 or newer for C++20 support",
    )
    conflicts("%gcc@:8", msg="fenics-dolfinx requires GCC-9 or newer for improved C++17 support")

    root_cmakelists_dir = "cpp"

    def cmake_args(self):
        return [
            self.define("DOLFINX_SKIP_BUILD_TESTS", True),
            self.define_from_variant("DOLFINX_ENABLE_SLEPC", "slepc"),
            self.define_from_variant("DOLFINX_ENABLE_ADIOS2", "adios2"),
            self.define("DOLFINX_UFCX_PYTHON", False),
            self.define("DOLFINX_ENABLE_KAHIP", "partitioners=kahip" in self.spec),
            self.define("DOLFINX_ENABLE_PARMETIS", "partitioners=parmetis" in self.spec),
            self.define("DOLFINX_ENABLE_SCOTCH", "partitioners=scotch" in self.spec),
        ]
