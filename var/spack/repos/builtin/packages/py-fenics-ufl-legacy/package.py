# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsUflLegacy(PythonPackage):
    """The Unified Form Language (UFL) is a domain specific language for
    declaration of finite element discretizations of variational forms. More
    precisely, it defines a flexible interface for choosing finite element
    spaces and defining expressions for weak forms in a notation close to
    mathematical notation."""

    homepage = "https://fenicsproject.org/"
    url = "https://github.com/FEniCS/ufl-legacy/archive/2022.3.0.tar.gz"
    git = "https://github.com/FEniCS/ufl-legacy.git"
    maintainers("chrisrichardson", "garth-wells", "jhale")

    license("LGPL-3.0-or-later")

    version("main", branch="main")
    version("2023.2.0", sha256="d1d3209e8ebd4bd70513c26890f51823bac90edc956233c47bd8e686e064436e")
  

    depends_on("python@3.8:", when="@2023.2.0:", type=("build", "run"))

    depends_on("py-setuptools@62:", when="@2023.2.0:", type="build")
    depends_on("py-setuptools@58:", when="@2022.1.0:2023.1.1.post0", type="build")
    depends_on("py-setuptools@40:", when="@2016.2.0:2021.1.0", type="build")
    depends_on("py-numpy", type=("build", "run"))

    depends_on("py-pytest", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        with working_dir("test"):
            Executable("py.test")()
