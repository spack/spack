# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySoupsieve(PythonPackage):
    """A modern CSS selector implementation for Beautiful Soup."""

    homepage = "https://github.com/facelessuser/soupsieve"
    pypi = "soupsieve/soupsieve-1.9.3.tar.gz"

    license("MIT")

    # Circular dependency on beautifulsoup4
    skip_modules = ["soupsieve"]

    version(
        "2.4.1",
        sha256="1c1bfee6819544a3447586c889157365a27e10d88cde3ad3da0cf0ddf646feb8",
        url="https://pypi.org/packages/49/37/673d6490efc51ec46d198c75903d99de59baffdd47aea3d071b80a9e4e89/soupsieve-2.4.1-py3-none-any.whl",
    )
    version(
        "2.3.2.post1",
        sha256="3b2503d3c7084a42b1ebd08116e5f81aadfaea95863628c80a3b774a11b7c759",
        url="https://pypi.org/packages/16/e3/4ad79882b92617e3a4a0df1960d6bce08edfb637737ac5c3f3ba29022e25/soupsieve-2.3.2.post1-py3-none-any.whl",
    )
    version(
        "2.2.1",
        sha256="c2c1c2d44f158cdbddab7824a9af8c4f83c76b1e23e049479aa432feb6c4c23b",
        url="https://pypi.org/packages/36/69/d82d04022f02733bf9a72bc3b96332d360c0c5307096d76f6bb7489f7e57/soupsieve-2.2.1-py3-none-any.whl",
    )
    version(
        "1.9.6",
        sha256="feb1e937fa26a69e08436aad4a9037cd7e1d4c7212909502ba30701247ff8abd",
        url="https://pypi.org/packages/39/36/f35056eb9978a622bbcedc554993d10777e3c6ff1ca24cde53f4be9c5fc4/soupsieve-1.9.6-py2.py3-none-any.whl",
    )
    version(
        "1.9.3",
        sha256="a5a6166b4767725fd52ae55fee8c8b6137d9a51e9f1edea461a062a759160118",
        url="https://pypi.org/packages/0b/44/0474f2207fdd601bb25787671c81076333d2c80e6f97e92790f8887cf682/soupsieve-1.9.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.4")

    # Historical dependencies
