# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsDolfinx(PythonPackage):
    """Python interface to the next generation FEniCS problem solving
    environment"""

    homepage = "https://github.com/FEniCS/dolfinx"
    url = "https://github.com/FEniCS/dolfinx/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/dolfinx.git"
    maintainers("chrisrichardson", "garth-wells", "nate-sime", "jhale")

    license("LGPL-3.0-only")

    version("main", branch="main")
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

    depends_on("cmake@3.19:", type="build")
    depends_on("hdf5", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("python@3.8:", when="@0.6.1:", type=("build", "run"))
    depends_on("python@3.8:3.10", when="@0.5:0.6.0", type=("build", "run"))
    depends_on("python@3.7:3.10", when="@0.4", type=("build", "run"))

    depends_on("fenics-dolfinx@main", when="@main")
    depends_on("fenics-dolfinx@0.7.2", when="@0.7.2")
    depends_on("fenics-dolfinx@0.6.0", when="@0.6.0")
    depends_on("fenics-dolfinx@0.5.1", when="@0.5.1")
    depends_on("fenics-dolfinx@0.5.0", when="@0.5.0")
    depends_on("fenics-dolfinx@0.4.1", when="@0.4.1")

    depends_on("py-fenics-basix@main", type=("build", "run"), when="@main")
    depends_on("fenics-basix@main", type=("build", "link"), when="@main")
    depends_on("fenics-basix@0.7", type=("build", "link"), when="@0.7")
    depends_on("fenics-basix@0.6.0:0.6", type=("build", "link"), when="@0.6.0:0.6")
    depends_on("fenics-basix@0.5.1:0.5", type=("build", "link"), when="@0.5.0:0.5")
    depends_on("fenics-basix@0.4.2", type=("build", "link"), when="@0.4.1")

    depends_on("py-fenics-ffcx@main", type=("build", "run"), when="@main")
    depends_on("py-fenics-ffcx@0.7", type=("build", "run"), when="@0.7")
    depends_on("py-fenics-ffcx@0.6", type=("build", "run"), when="@0.6")
    depends_on("py-fenics-ffcx@0.5.0.post0", type=("build", "run"), when="@0.5.0:0.5")
    depends_on("py-fenics-ffcx@0.4.2", type=("build", "run"), when="@0.4.1")

    depends_on("py-fenics-ufl@main", type=("build", "run"), when="@main")
    depends_on("py-fenics-ufl@2023.2", type=("build", "run"), when="@0.7")
    depends_on("py-fenics-ufl@2023.1", type=("build", "run"), when="@0.6")
    depends_on("py-fenics-ufl@2022.2.0", type=("build", "run"), when="@0.5.0:0.5")
    depends_on("py-fenics-ufl@2022.1.0", type=("build", "run"), when="@0.4.1")

    depends_on("py-numpy@1.21:", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-petsc4py", type=("build", "run"))
    depends_on("py-cffi", type=("build", "run"))

    depends_on("py-nanobind@1.8:", when="@0.8:", type="build")
    depends_on("py-scikit-build-core+pyproject@0.5:", when="@0.8:", type="build")

    depends_on("py-pybind11@2.7.0:", when="@:0.7", type=("build", "run"))
    depends_on("py-setuptools@42:", when="@:0.7", type="build")
    depends_on("xtensor@0.23.10:", type="build", when="@:0.5")

    build_directory = "python"
