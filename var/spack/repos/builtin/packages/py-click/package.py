# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClick(PythonPackage):
    """Python composable command line interface toolkit."""

    homepage = "https://click.palletsprojects.com"
    pypi = "click/click-7.1.2.tar.gz"
    git = "https://github.com/pallets/click.git"

    license("BSD-3-Clause")

    version(
        "8.1.7",
        sha256="ae74fb96c20a0277a1d615f1e4d73c8414f5a98db8b799a7931d1582f3390c28",
        url="https://pypi.org/packages/00/2e/d53fa4befbf2cfa713304affc7ca780ce4fc1fd8710527771b58311a3229/click-8.1.7-py3-none-any.whl",
    )
    version(
        "8.1.3",
        sha256="bb4d8133cb15a609f44e8213d9b391b0809795062913b383c62be0ee95b1db48",
        url="https://pypi.org/packages/c2/f1/df59e28c642d583f7dacffb1e0965d0e00b218e0186d7858ac5233dce840/click-8.1.3-py3-none-any.whl",
    )
    version(
        "8.0.3",
        sha256="353f466495adaeb40b6b5f592f9f91cb22372351c84caeb068132442a4518ef3",
        url="https://pypi.org/packages/48/58/c8aa6a8e62cc75f39fee1092c45d6b6ba684122697d7ce7d53f64f98a129/click-8.0.3-py3-none-any.whl",
    )
    version(
        "8.0.1",
        sha256="fba402a4a47334742d782209a7c79bc448911afe1149d07bdabdf480b3e2f4b6",
        url="https://pypi.org/packages/76/0a/b6c5f311e32aeb3b406e03c079ade51e905ea630fc19d1262a46249c1c86/click-8.0.1-py3-none-any.whl",
    )
    version(
        "7.1.2",
        sha256="dacca89f4bfadd5de3d7489b7c8a566eee0d3676333fbb50030263894c38c0dc",
        url="https://pypi.org/packages/d2/3d/fa76db83bf75c4f8d338c2fd15c8d33fdd7ad23a9b5e57eb6c5de26b430e/click-7.1.2-py2.py3-none-any.whl",
    )
    version(
        "7.0",
        sha256="2335065e6395b9e67ca716de5f7526736bfa6ceead690adf616d925bdc622b13",
        url="https://pypi.org/packages/fa/37/45185cb5abbc30d7257104c434fe0b07e5a195a6847506c074527aa599ec/Click-7.0-py2.py3-none-any.whl",
    )
    version(
        "6.6",
        sha256="fcf697e1fd4b567d817c69dab10a4035937fe6af175c05fd6806b69f74cbc6c4",
        url="https://pypi.org/packages/1c/7c/10b4132dd952b6a04e37626258825b8aa8c1eb99545f2eb26a77c21efb55/click-6.6-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@8.1:")
        depends_on("py-colorama", when="@8.0.0-rc1: platform=windows")
        depends_on("py-importlib-metadata", when="@8.0.1: ^python@:3.7")

    # Needed to ensure that Spack can bootstrap black with Python 3.6
