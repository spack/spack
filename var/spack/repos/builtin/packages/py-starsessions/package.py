# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStarsessions(PythonPackage):
    """Advanced sessions for Starlette and FastAPI frameworks."""

    homepage = "https://github.com/alex-oleshkevich/starsessions"
    pypi = "starsessions/starsessions-2.1.1.tar.gz"

    license("MIT")

    version(
        "2.1.1",
        sha256="e3573ce6f3531b201021443fa5c7ec72d360835dcb102d384c4f87ac942005a6",
        url="https://pypi.org/packages/d0/97/8b0aaa98329252cf85bdc79b794ae7ac965a96842abde41ab724c298c957/starsessions-2.1.1-py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="c0758f2a1a2438ec7ba88b232e82008f2261a75584f01179c787b3636fae6040",
        url="https://pypi.org/packages/18/fa/6d33ea610c65f9ed27223860e1f4e25b2ac17c8780a69b6cf65ece037428/starsessions-1.3.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:3", when="@2.0.0-alpha1:")
        depends_on("python@:3", when="@:1")
        depends_on("py-itsdangerous@2.0.1:")
        depends_on("py-starlette", when="@1.1.4:")
