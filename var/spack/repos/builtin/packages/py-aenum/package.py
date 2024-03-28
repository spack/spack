# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAenum(PythonPackage):
    """Advanced Enumerations (compatible with Python's stdlib Enum),
    NamedTuples, and NamedConstants."""

    homepage = "https://github.com/ethanfurman/aenum"
    pypi = "aenum/aenum-2.1.2.tar.gz"

    version(
        "3.1.12",
        sha256="8d79c9e3ec997220e355b96b322e672fb56a53e61744138ed838407e3a07b610",
        url="https://pypi.org/packages/63/5f/5b280c3d3ce897b3616bef3a44004e1fbfd4f2fe757e12b4d0e71de2900f/aenum-3.1.12-py2-none-any.whl",
    )
    version(
        "2.1.2",
        sha256="7a77c205c4bc9d7fe9bd73b3193002d724aebf5909fa0d297534208953891ec8",
        url="https://pypi.org/packages/44/c4/7cda7e7e71e18ad999cb9d23f9969f818af1ed6be71d18db7963680b8320/aenum-2.1.2-py2-none-any.whl",
    )
