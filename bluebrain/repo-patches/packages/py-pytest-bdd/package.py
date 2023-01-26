# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestBdd(PythonPackage):
    """pytest-bdd implements a subset of the Gherkin language to enable
    automating project requirements testing and to facilitate behavioral
    driven development."""

    homepage = "https://github.com/pytest-dev/pytest-bdd"
    pypi = "pytest-bdd/pytest_bdd-6.1.1.tar.gz"

    version("6.1.1", sha256="138af3592bcce5d4684b0d690777cf199b39ce45d423ca28086047ffe6111010")

    depends_on("py-poetry", type="build")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-mako", type=("build", "run"))
    depends_on("py-parse", type=("build", "run"))
    depends_on("py-parse-type", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-pytest@6.2.0:", type=("build", "run"))
