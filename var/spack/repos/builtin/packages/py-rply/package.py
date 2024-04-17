# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRply(PythonPackage):
    """A pure Python Lex/Yacc that works with RPython."""

    homepage = "https://github.com/alex/rply/"
    pypi = "rply/rply-0.7.8.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.7.8",
        sha256="28ffd11d656c48aeb8c508eb382acd6a0bd906662624b34388751732a27807e7",
        url="https://pypi.org/packages/c0/7c/f66be9e75485ae6901ae77d8bdbc3c0e99ca748ab927b3e18205759bde09/rply-0.7.8-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-appdirs", when="@0.7.4:")
