# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySqlparse(PythonPackage):
    """A non-validating SQL parser module for Python."""

    homepage = "https://github.com/andialbrecht/sqlparse"
    url = "https://github.com/andialbrecht/sqlparse/archive/0.3.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.4.1",
        sha256="017cde379adbd6a1f15a61873f43e8274179378e95ef3fede90b5aa64d304ed0",
        url="https://pypi.org/packages/14/05/6e8eb62ca685b10e34051a80d7ea94b7137369d8c0be5c3b9d9b6e3f5dae/sqlparse-0.4.1-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="022fb9c87b524d1f7862b3037e541f68597a730a8843245c349fc93e1643dc4e",
        url="https://pypi.org/packages/85/ee/6e821932f413a5c4b76be9c5936e313e4fc626b33f16e027866e1d60f588/sqlparse-0.3.1-py2.py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="40afe6b8d4b1117e7dff5504d7a8ce07d9a1b15aeeade8a2d10f130a834f8177",
        url="https://pypi.org/packages/ef/53/900f7d2a54557c6a37886585a91336520e5539e3ae2423ff1102daf4f3a7/sqlparse-0.3.0-py2.py3-none-any.whl",
    )
    version(
        "0.2.4",
        sha256="d9cf190f51cbb26da0412247dfe4fb5f4098edb73db84e02f9fc21fdca31fed4",
        url="https://pypi.org/packages/65/85/20bdd72f4537cf2c4d5d005368d502b2f464ede22982e724a82c86268eda/sqlparse-0.2.4-py2.py3-none-any.whl",
    )
    version(
        "0.2.3",
        sha256="740a023ef38ce11bbb99a9d143856f56ef4ec5b0d7a853f58c02c65b035114c4",
        url="https://pypi.org/packages/9b/57/d9d2848e5435c8a53461bb7b95421dc9a82cb31235cb101d28667d1a2104/sqlparse-0.2.3-py2.py3-none-any.whl",
    )
