# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPathlib2(PythonPackage):
    """Backport of pathlib from python 3.4"""

    pypi = "pathlib2/pathlib2-2.3.2.tar.gz"

    license("MIT")

    version(
        "2.3.7.post1",
        sha256="5266a0fd000452f1b3467d782f079a4343c63aaa119221fbdc4e39577489ca5b",
        url="https://pypi.org/packages/09/eb/4af4bcd5b8731366b676192675221c5324394a580dfae469d498313b5c4a/pathlib2-2.3.7.post1-py2.py3-none-any.whl",
    )
    version(
        "2.3.6",
        sha256="3a130b266b3a36134dcc79c17b3c7ac9634f083825ca6ea9d8f557ee6195c9c8",
        url="https://pypi.org/packages/76/67/dc02c72177ec79f0176e5bf9921e9c1745a381ed556afb3b3ecc2bb8ba2e/pathlib2-2.3.6-py2.py3-none-any.whl",
    )
    version(
        "2.3.3",
        sha256="5887121d7f7df3603bca2f710e7219f3eca0eb69e0b7cc6e0a022e155ac931a7",
        url="https://pypi.org/packages/2a/46/c696dcf1c7aad917b39b875acdc5451975e3a9b4890dca8329983201c97a/pathlib2-2.3.3-py2.py3-none-any.whl",
    )
    version(
        "2.3.2",
        sha256="d1aa2a11ba7b8f7b21ab852b1fb5afb277e1bb99d5dfc663380b5015c0d80c5a",
        url="https://pypi.org/packages/66/a7/9f8d84f31728d78beade9b1271ccbfb290c41c1e4dc13dbd4997ad594dcd/pathlib2-2.3.2-py2.py3-none-any.whl",
    )
    version(
        "2.1.0",
        sha256="24e0b33e1333b55e73c9d1e9a8342417d519f7789a9d3b440f4acd00ea45157e",
        url="https://pypi.org/packages/b8/1b/02efe53150500722d1b5bbe3d9dd5a417fe07df05566595cf9114ced3c39/pathlib2-2.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six", when="@2.3.2:")
