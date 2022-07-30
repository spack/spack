# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchling(PythonPackage):
    """Modern, extensible Python build backend."""

    homepage = "https://hatch.pypa.io/latest/"
    pypi = "hatchling/hatchling-1.4.1.tar.gz"

    version("1.4.1", sha256="13461b42876ade4f75ee5d2a2c656b288ca0aab7f048ef66657ef166996b2118")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-editables@0.3:", type=("build", "run"))
    depends_on("py-importlib-metadata", when="^python@:3.7", type=("build", "run"))
    depends_on("py-packaging@21.3:", type=("build", "run"))
    depends_on("py-pathspec@0.9:", type=("build", "run"))
    depends_on("py-pluggy@1:", type=("build", "run"))
    depends_on("py-tomli@1.2.2:", when="^python@:3.10", type=("build", "run"))
