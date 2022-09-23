# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVersioneer(PythonPackage):
    """Versioneer is a tool to automatically update version strings by
    asking your version-control system about the current tree."""

    homepage = "https://github.com/python-versioneer/python-versioneer"
    pypi = "versioneer/versioneer-0.26.tar.gz"
    git = "https://github.com/python-versioneer/python-versioneer.git"

    maintainers = ["scemama"]

    version("0.26", sha256="84fc729aa296d1d26645a8f62f178019885ff6f9a1073b29a4a228270ac5257b")
    version("0.18", sha256="cf895b67f5bc62d61c4837458069ded8f66b4e5764c19f7253c51ee27e8b3a99")

    depends_on("python@3.6:", when="@0.19:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
