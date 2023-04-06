# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxThemeBuilder(PythonPackage):
    """A tool for authoring Sphinx themes with a simple (opinionated) workflow."""

    homepage = "https://github.com/pradyunsg/sphinx-theme-builder"
    pypi = "sphinx-theme-builder/sphinx-theme-builder-0.2.0b1.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]

    version("0.2.0b1", sha256="e9bb4a0a8516bab8769b9ddf003b70e5878611113319eb1fdb690af84a3a595f")

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-flit-core@3.2:", type="build")

    depends_on("py-pyproject-metadata", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))
    depends_on("py-nodeenv", type=("build", "run"))
