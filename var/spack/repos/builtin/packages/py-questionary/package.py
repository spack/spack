# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuestionary(PythonPackage):
    """Questionary is a Python library for effortlessly building
    pretty command line interfaces.
    """

    homepage = "https://github.com/tmbo/questionary"
    pypi = "questionary/questionary-1.9.0.tar.gz"

    license("MIT")

    version(
        "1.9.0",
        sha256="fa50c06af4e3826d986efbc90be16e42ff367a634e6a169e42a3f9fccd90648b",
        url="https://pypi.org/packages/0d/44/972fd92022c4dbc28fa4cbb2e161e60e2f116eb8c64b58c2c90a4b57c4c9/questionary-1.9.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.9", when="@1.7:1.9")
        depends_on("py-prompt-toolkit@2:", when="@1.5:1")
