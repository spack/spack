# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnsimarkup(PythonPackage):
    """Produce colored terminal text with an xml-like markup."""

    homepage = "https://github.com/gvalkov/python-ansimarkup"
    pypi = "ansimarkup/ansimarkup-1.5.0.tar.gz"

    maintainers("LydDeb")

    license("BSD-3-Clause")

    version(
        "2.1.0",
        sha256="51ab9f3157125c53e93d8fd2e92df37dfa1757c9f2371ed48554e111c7d4401a",
        url="https://pypi.org/packages/60/99/878823a360a0bd9ae034d39fe37f8fdd976de8da642c2ec608f093efc273/ansimarkup-2.1.0-py3-none-any.whl",
    )
    version(
        "1.5.0",
        sha256="3146ca74af5f69e48a9c3d41b31085c0d6378f803edeb364856d37c11a684acf",
        url="https://pypi.org/packages/22/09/3ad81e40d752ef51a9a8c320c9385de0d98a4dad68c0e4f793befc610f56/ansimarkup-1.5.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-colorama", when="@1.4.1:")
