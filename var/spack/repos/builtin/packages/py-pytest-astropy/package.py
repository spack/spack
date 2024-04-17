# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestAstropy(PythonPackage):
    """Meta-package containing dependencies for testing."""

    homepage = "https://github.com/astropy/pytest-astropy"
    pypi = "pytest-astropy/pytest-astropy-0.10.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.10.0",
        sha256="0b046ddeaa9e61356bd121d91f86e8b745f00b8f7cec41fc9d9502770bf17926",
        url="https://pypi.org/packages/da/e0/fd2bab9dcf0a2e8103a76b4b365cd75b92937fbc39c64aeed7db1bc8fa3f/pytest_astropy-0.10.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.9:")
        depends_on("py-attrs@19.2:", when="@0.9:")
        depends_on("py-hypothesis@5.1:", when="@0.8:")
        depends_on("py-pytest@4.6:", when="@0.8:")
        depends_on("py-pytest-arraydiff", when="@0.6,0.8:0.10")
        depends_on("py-pytest-astropy-header@0.1.2:", when="@0.8:0.10")
        depends_on("py-pytest-cov@2.3.1:", when="@0.9:")
        depends_on("py-pytest-doctestplus@0.11:", when="@0.9:0.10")
        depends_on("py-pytest-filter-subpackage", when="@0.8:0.10")
        depends_on("py-pytest-mock@2:", when="@0.9:")
        depends_on("py-pytest-openfiles@0.3.1:", when="@0.6,0.8:0.10")
        depends_on("py-pytest-remotedata@0.3.1:", when="@0.6,0.8:0.10")
