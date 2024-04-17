# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymysql(PythonPackage):
    """Pure-Python MySQL client library"""

    homepage = "https://github.com/PyMySQL/PyMySQL/"
    pypi = "pymysql/PyMySQL-0.9.2.tar.gz"

    license("MIT")

    version(
        "0.9.2",
        sha256="95f057328357e0e13a30e67857a8c694878b0175797a9a203ee7adbfb9b1ec5f",
        url="https://pypi.org/packages/a7/7d/682c4a7da195a678047c8f1c51bb7682aaedee1dca7547883c3993ca9282/PyMySQL-0.9.2-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-cryptography", when="@0.9:0.9.2")
