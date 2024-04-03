# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPathy(PythonPackage):
    """pathlib.Path subclasses for local and cloud bucket storage"""

    homepage = "https://github.com/justindujardin/pathy"
    pypi = "pathy/pathy-0.10.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.10.1",
        sha256="a7613ee2d99a0a3300e1d836322e2d947c85449fde59f52906f995dbff67dad4",
        url="https://pypi.org/packages/82/c6/683e3955de9a13b14dfa3ea358cd58f3914057e8064a2dcbfd450958e72e/pathy-0.10.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dataclasses@0.6:", when="^python@:3.6")
        depends_on("py-smart-open@5.2.1:6", when="@0.10.1:")
        depends_on("py-typer@0.3:")
