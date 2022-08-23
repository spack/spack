# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMesonPython(PythonPackage):
    """Meson Python build backend (PEP 517)."""

    homepage = "https://github.com/FFY00/mesonpy"
    pypi = "meson_python/meson_python-0.7.0.tar.gz"

    version("0.7.0", sha256="9fcfa350f44ca80dd4f5f9c3d251725434acf9a07d9618f382e6cc4629dcbe84")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-meson@0.62:", type=("build", "run"))
    depends_on("py-ninja", type=("build", "run"))
    depends_on("py-pyproject-metadata@0.5:", type=("build", "run"))
    depends_on("py-tomli@1:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", when="^python@:3.7", type=("build", "run"))
    depends_on("py-colorama", when="platform=windows", type=("build", "run"))
