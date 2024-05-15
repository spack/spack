# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultivoro(PythonPackage):
    """Python bindings for Voro++ library with OpenMP support."""

    homepage = "https://github.com/eleftherioszisis/multivoro"
    git = "https://github.com/eleftherioszisis/multivoro.git"
    pypi = "multivoro/multivoro-0.1.0.tar.gz"

    version("0.1.0", sha256="890fc013c77f77ea50ac7d0ef14e2e40d9a6acb2f822ef0161d6e94759909f62")

    depends_on("py-scikit-build-core@0.4.3:", type=("build", "link"))
    depends_on("py-nanobind", type=("build", "link"))

    depends_on("py-numpy", type=("build", "run"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test(self):
        python("-m", "pytest", "tests")
