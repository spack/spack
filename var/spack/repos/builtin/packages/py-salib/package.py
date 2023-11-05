# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySalib(PythonPackage):
    """Python implementations of commonly used sensitivity analysis methods."""

    homepage = "https://salib.readthedocs.org"
    pypi = "SALib/SALib-1.4.0.1.tar.gz"

    maintainers("schmitts")

    version("1.4.4", sha256="50a6459088700f55261a683752818530d14ede30cece2c324ac94d4b9e288b6d")
    version("1.4.0.1", sha256="dbf6e865af9f3be82a79cf64889ed66d6d3b6803f0c22a242a112876789d49e7")

    depends_on("py-setuptools@38.3:", type=("build", "run"))
    depends_on("py-numpy@1.16.5:", type=("build", "run"))
    depends_on("py-scipy@1.5.2:", type=("build", "run"))
    depends_on("py-matplotlib@3.2.2:", type=("build", "run"))
    depends_on("py-pandas@1.1.2:", type=("build", "run"))
    depends_on("py-pathos@0.2.5:", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@1.4.4: ^python@:3.7", type=("build", "run"))
    depends_on("py-setuptools-scm", when="@1.4.4:", type=("build", "run"))
    depends_on("py-wheel", when="@1.4.4:", type=("build", "run"))
