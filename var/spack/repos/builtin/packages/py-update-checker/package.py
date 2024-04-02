# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUpdateChecker(PythonPackage):
    """A python module that will check for package updates."""

    homepage = "https://github.com/bboe/update_checker"
    pypi = "update_checker/update_checker-0.18.0.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.18.0",
        sha256="cbba64760a36fe2640d80d85306e8fe82b6816659190993b7bdabadee4d4bbfd",
        url="https://pypi.org/packages/0c/ba/8dd7fa5f0b1c6a8ac62f8f57f7e794160c1f86f31c6d0fb00f582372a3e4/update_checker-0.18.0-py3-none-any.whl",
    )
    version(
        "0.17",
        sha256="1ff5dc7aab340b4f7710bd6c69d08ff5a5351617cd4ba0eb8886ddb285e2104f",
        url="https://pypi.org/packages/d6/c3/aaf8a162df8e8f9d321237c7c0e63aff95b42d19f1758f96606e3cabb245/update_checker-0.17-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-requests@2.3:", when="@0.17:")
