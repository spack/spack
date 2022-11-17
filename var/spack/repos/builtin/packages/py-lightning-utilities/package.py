# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightningUtilities(PythonPackage):
    """Common Python utilities and GitHub Actions in Lightning Ecosystem"""

    homepage = "https://github.com/Lightning-AI/utilities"
    pypi = "lightning-utilities/lightning-utilities-0.4.1.tar.gz"

    maintainers = ["adamjstewart"]

    version("0.4.1", sha256="969697b0debffd808d4cf3b74af4952f82bf6726f4ce561119037871547690a5")
    version("0.4.0", sha256="961c29774c2c8303e0a2f6e6512a2e21e1d8acaf6df182865667af4a51bc176c")
    version("0.3.0", sha256="d769ab9b76ebdee3243d1051d509aafee57d7947734ddc22977deef8a6427f2f")

    # setup.py
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # requirements/base.txt
    depends_on("py-importlib-metadata@4:", when="@0.4.1: ^python@:3.7", type=("build", "run"))

    # Historical dependencies
    depends_on("py-fire", when="@0.3.0", type=("build", "run"))
