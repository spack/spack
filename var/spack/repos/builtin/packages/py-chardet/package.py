# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChardet(PythonPackage):
    """Universal encoding detector for Python 3"""

    homepage = "https://github.com/chardet/chardet"
    pypi = "chardet/chardet-3.0.4.tar.gz"

    license("LGPL-2.1-or-later")

    version(
        "5.2.0",
        sha256="e1cf59446890a00105fe7b7912492ea04b6e6f06d4b742b2c788469e34c82970",
        url="https://pypi.org/packages/38/6f/f5fbc992a329ee4e0f288c1fe0e2ad9485ed064cac731ed2fe47dcc38cbf/chardet-5.2.0-py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="362777fb014af596ad31334fde1e8c327dfdb076e1960d1694662d46a6917ab9",
        url="https://pypi.org/packages/74/8f/8fc49109009e8d2169d94d72e6b1f4cd45c13d147ba7d6170fb41f22b08f/chardet-5.1.0-py3-none-any.whl",
    )
    version(
        "5.0.0",
        sha256="d3e64f022d254183001eccc5db4040520c0f23b1a3f33d6413e099eb7f126557",
        url="https://pypi.org/packages/4c/d1/1b96dd69fa42f20b70701b5cd42a75dd5f0c7a24dc0abfef35cc146210dc/chardet-5.0.0-py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="f864054d66fd9118f2e67044ac8981a54775ec5b67aed0441892edb553d21da5",
        url="https://pypi.org/packages/19/c7/fa589626997dd07bd87d9269342ccb74b1720384a4d739a1872bd84fbe68/chardet-4.0.0-py2.py3-none-any.whl",
    )
    version(
        "3.0.4",
        sha256="fc323ffcaeaed0e0a02bf4d117757b98aed530d9ed4531e3e15460124c106691",
        url="https://pypi.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl",
    )
    version(
        "3.0.2",
        sha256="6ebf56457934fdce01fb5ada5582762a84eed94cad43ed877964aebbdd8174c0",
        url="https://pypi.org/packages/b8/74/54fdc2fcfdd46b6c486964b64c5bb7db9a3664033ab25cf11aab06dd2a5d/chardet-3.0.2-py2.py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="aaf514bde38020b4f1e42c6a6e141f2827a8a58ccfc3b22b6ff5a1a4b50be56e",
        url="https://pypi.org/packages/7e/5c/605ca2daa5cf21c87690d8fe6ab05a6f2278c451f4ede6456dd26453f4bd/chardet-2.3.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@5.1:")

    # Historical dependencies
