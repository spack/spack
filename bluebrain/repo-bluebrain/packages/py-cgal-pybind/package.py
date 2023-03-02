# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCgalPybind(PythonPackage):
    """Python bindings for CGAL"""

    homepage = "https://github.com/BlueBrain/cgal-pybind"
    git = "https://github.com/BlueBrain/cgal-pybind.git"
    pypi = "cgal-pybind/cgal-pybind-0.1.4.tar.gz"

    version("develop", submodules=True)
    version("0.1.4", sha256="ddb125f98ab96d621a4240bef0be58f8b7317656c5b3fa6a40b24bf5c2c5b1c1")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-wheel", type="build")
    depends_on("cmake", type="build")
    depends_on("ninja", type="build")

    depends_on("boost@1.50:")
    depends_on("cgal")
    depends_on("eigen")
    depends_on("py-pybind11")
    depends_on("py-pytest", type="test")

    depends_on("py-numpy@1.14.5:", type=("build", "run"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
