# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsFfcx(PythonPackage):
    """Next generation FEniCS Form Compiler"""

    homepage = "https://github.com/FEniCS/ffcx"
    url = "https://github.com/FEniCS/ffcx/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/ffcx.git"
    maintainers("chrisrichardson", "garth-wells", "jhale")

    version("main", branch="main")
    version("0.7.0", sha256="7f3c3ca91d63ce7831d37799cc19d0551bdcd275bdfa4c099711679533dd1c71")
    version("0.6.0", sha256="076fad61d406afffd41019ae1abf6da3f76406c035c772abad2156127667980e")
    version(
        "0.5.0.post0", sha256="039908c9998b51ba53e5deb3a97016062c262f0a4285218644304f7d3cd35882"
    )
    version("0.4.2", sha256="3be6eef064d6ef907245db5b6cc15d4e603762e68b76e53e099935ca91ef1ee4")

    depends_on("python@3.8:", when="@0.7:", type=("build", "run"))
    depends_on("py-setuptools@62:", when="@0.7:", type="build")
    # Runtime dependency on pkg_resources from setuptools at 0.6.0
    depends_on("py-setuptools@58:", when="@0.4.2:0.6", type=("build", "run"))

    # CFFI is required at runtime for JIT support
    depends_on("py-cffi", type=("build", "run"))
    # py-numpy>=1.21 required because FFCx uses NumPy typing (version
    # requirement not properly set in the FFCx pyproject.toml file)
    depends_on("py-numpy@1.21:", type=("build", "run"))

    depends_on("py-fenics-ufl@main", type=("build", "run"), when="@main")
    depends_on("py-fenics-ufl@2023.3.0:", type=("build", "run"), when="@0.8")
    depends_on("py-fenics-ufl@2023.2.0", type=("build", "run"), when="@0.7")
    depends_on("py-fenics-ufl@2023.1", type=("build", "run"), when="@0.6")
    depends_on("py-fenics-ufl@2022.2.0", type=("build", "run"), when="@0.5.0:0.5")
    depends_on("py-fenics-ufl@2022.1.0", type=("build", "run"), when="@0.4.2")

    depends_on("py-fenics-basix@main", type=("build", "run"), when="@main")
    depends_on("py-fenics-basix@0.7", type=("build", "run"), when="@0.7")
    depends_on("py-fenics-basix@0.6.0:0.6", type=("build", "run"), when="@0.6.0:0.6")
    depends_on("py-fenics-basix@0.5.1:0.5", type=("build", "run"), when="@0.5.0:0.5")
    depends_on("py-fenics-basix@0.4.2", type=("build", "run"), when="@0.4.2")

    depends_on("py-pytest@6:", type="test")
    depends_on("py-sympy", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        with working_dir("test"):
            pytest = which("pytest")
            pytest("--ignore=test_cmdline.py")
