# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsBasix(PythonPackage):
    """Python interface to Basix, a finite element definition and tabulation runtime library"""

    homepage = "https://github.com/FEniCS/basix"
    url = "https://github.com/FEniCS/basix/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/basix.git"
    maintainers("chrisrichardson", "mscroggs", "garth-wells", "jhale")

    version("main", branch="main")
    version("0.6.0", sha256="687ae53153c98facac4080dcdc7081701db1dcea8c5e7ae3feb72aec17f83304")
    version("0.5.1", sha256="69133476ac35f0bd0deccb480676030378c341d7dfb2adaca22cd16b7e1dc1cb")
    version("0.4.2", sha256="a54f5e442b7cbf3dbb6319c682f9161272557bd7f42e2b8b8ccef88bc1b7a22f")
    version(
        "0.3.0",
        sha256="9b148fd2a5485c94011fc6ca977ebdef0e51782a62b3654fc044f35b60e2bd07",
        deprecated=True,
    )
    version(
        "0.2.0",
        sha256="e1ec537737adb283717060221635092474e3f2b5b5ba79dfac74aa496bec2fcb",
        deprecated=True,
    )
    version(
        "0.1.0",
        sha256="2ab41fe6ad4f6c42f01b17a6e7c39debb4e0ae61c334d1caebee78b741bca4e7",
        deprecated=True,
    )

    depends_on("fenics-basix@main", type=("build", "run"), when="@main")
    depends_on("fenics-basix@0.6.0", type=("build", "run"), when="@0.6.0")
    depends_on("fenics-basix@0.5.1", type=("build", "run"), when="@0.5.1")
    depends_on("fenics-basix@0.4.2", type=("build", "run"), when="@0.4.2")
    depends_on("fenics-basix@0.3.0", type=("build", "run"), when="@0.3.0")
    depends_on("fenics-basix@0.2.0", type=("build", "run"), when="@0.2.0")
    depends_on("fenics-basix@0.1.0", type=("build", "run"), when="@0.1.0")

    depends_on("py-setuptools@42:", type="build", when="@0.4:")
    depends_on("py-setuptools@40:", type="build")
    depends_on("py-numpy@1.21:", type=("build", "run"))
    depends_on("cmake@3.19:", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pybind11@2.9.1:", type="build", when="@0.4:")
    depends_on("py-pybind11@2.2.4:", type="build")

    depends_on("xtensor@0.23.10:", type="build", when="@:0.4")

    build_directory = "python"
