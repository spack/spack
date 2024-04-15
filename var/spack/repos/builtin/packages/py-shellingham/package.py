# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyShellingham(PythonPackage):
    """Tool to Detect Surrounding Shell"""

    homepage = "https://github.com/sarugaku/shellingham"
    pypi = "shellingham/shellingham-1.4.0.tar.gz"

    license("0BSD")

    version(
        "1.5.0",
        sha256="a8f02ba61b69baaa13facdba62908ca8690a94b8119b69f5ec5873ea85f7391b",
        url="https://pypi.org/packages/3d/1a/d31fce69c119df1fddab3706b63c53d363982c55d841d9c3839b12f15327/shellingham-1.5.0-py2.py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="536b67a0697f2e4af32ab176c00a50ac2899c5a05e0d8e2dadac8e58888283f9",
        url="https://pypi.org/packages/76/94/7a764d57d0f46534e0022e651da6547bc5cfe7b6372e7e0ed1dde6f5cb67/shellingham-1.4.0-py2.py3-none-any.whl",
    )
