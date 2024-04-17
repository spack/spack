# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInquirer(PythonPackage):
    """Collection of common interactive command line user interfaces, based on Inquirer.js."""

    homepage = "https://github.com/magmax/python-inquirer"
    pypi = "inquirer/inquirer-3.1.3.tar.gz"

    license("MIT")

    version(
        "3.1.3",
        sha256="a7441fd74d06fcac4385218a1f5e8703f7a113f7944e01af47b8c58e84f95ce5",
        url="https://pypi.org/packages/a5/e7/009c1ad178a2ec0ab21606ef3efc151b2a7be56a3735a521c93049425a02/inquirer-3.1.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@3.1:")
        depends_on("py-blessed@1.19:", when="@2.9:")
        depends_on("py-python-editor@1.0.4:", when="@2.9:3.1")
        depends_on("py-readchar@3.0.6:", when="@2.10:")
