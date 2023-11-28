# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitBuildCore(PythonPackage):
    """scikit-build-core is a doubly improved build system generator
    for CPython C/C++/Fortran/Cython extensions. It features several
    improvements over the classic scikit-build build system generator."""

    homepage = "https://github.com/scikit-build/scikit-build-core"
    pypi = "scikit_build_core/scikit_build_core-0.2.0.tar.gz"
    git = "https://github.com/scikit-build/scikit-build-core"

    maintainers("wdconinc")

    version("0.6.1", sha256="392254a4ca7235c27a4be98cc24cd708f563171961ce37cff66120ebfda20b7a")
    version("0.6.0", sha256="1bea5ed83610b367f3446badd996f2356690548188d6d38e5b93152df311a7ae")
    version("0.2.0", sha256="d2a76d9447a412038dc5e25dd259b03c25278661a0c7c3da766bb971c1a9acd2")

    variant("pyproject", default=False, description="Enable pyproject.toml support")

    depends_on("python@3.7:", type=("build", "run"))

    # Build system
    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

    # Dependencies
    depends_on("py-exceptiongroup", when="^python@:3.10", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@0.3.0: ^python@:3.7")
    depends_on("py-importlib-resources@1.3:", when="^python@:3.8", type=("build", "run"))
    depends_on("py-packaging@20.9:", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="^python@:3.10", type=("build", "run"))
    depends_on("py-typing-extensions@3.10:", when="^python@:3.7", type=("build", "run"))
    depends_on("cmake@3.15:", type=("build", "run"))

    # Optional dependencies
    depends_on("py-pyproject-metadata@0.5:", when="+pyproject", type=("build", "run"))
    depends_on("py-pathspec@0.10.1:", when="+pyproject", type=("build", "run"))

    # Test dependencies
    depends_on("py-build +virtualenv", type="test")
    depends_on("py-cattrs@22.2:", type="test")
    depends_on("py-importlib-metadata", when="^python@:3.7", type="test")
    depends_on("py-pathspec@0.10.1:", type="test")
    depends_on("py-pybind11", type="test")
    depends_on("py-pyproject-metadata@0.5:", type="test")
    depends_on("py-pytest@7:", type="test")
    depends_on("py-pytest-subprocess@1.5:", type="test")
    depends_on("py-setuptools", type="test")
    depends_on("py-virtualenv", when="@0.6:", type="test")
    depends_on("py-wheel", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("tests"):
            which("pytest")()
