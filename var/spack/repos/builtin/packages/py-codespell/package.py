# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCodespell(PythonPackage):
    """check code for common misspellings"""

    homepage = "https://github.com/codespell-project/codespell"
    pypi = "codespell/codespell-2.2.6.tar.gz"

    license("GPL-2.0", checked_by="cmelone")

    version(
        "2.2.6",
        sha256="9ee9a3e5df0990604013ac2a9f22fa8e57669c827124a2e961fe8a1da4cacc07",
        url="https://pypi.org/packages/46/e0/5437cc96b74467c4df6e13b7128cc482c48bb43146fb4c11cf2bcd604e1f/codespell-2.2.6-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2.2.6:")

    conflicts("^py-setuptools-scm@8.0.0")
