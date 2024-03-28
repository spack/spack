# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestOpenfiles(PythonPackage):
    """A plugin for the pytest framework that allows developers to detect
    whether any file handles or other file-like objects were inadvertently
    left open at the end of a unit test"""

    homepage = "https://github.com/astropy/pytest-openfiles"
    pypi = "pytest-openfiles/pytest-openfiles-0.5.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.5.0",
        sha256="b02389b5666d552e236ccf8d4e971abe97b320653ee77316de23db181dbe4f3a",
        url="https://pypi.org/packages/c5/85/039b16aed2c8017033d96c8d35ded2e0b2d165b0fd7f38bfe04bb0b669a7/pytest_openfiles-0.5.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-psutil", when="@0.4:")
        depends_on("py-pytest@4.6:", when="@0.5:")
