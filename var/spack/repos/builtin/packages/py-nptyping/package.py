# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNptyping(PythonPackage):
    """Type hints for numpy"""

    homepage = "https://github.com/ramonhagenaars/nptyping"
    url = "https://github.com/ramonhagenaars/nptyping/archive/v2.4.1.tar.gz"
    # avoid pypi for now: https://github.com/ramonhagenaars/nptyping/issues/98

    license("MIT")

    version(
        "2.4.1",
        sha256="23e8164b1e2c55e872f392ca7516b9b1b0cb400b03b70accaa63998b4106b0b3",
        url="https://pypi.org/packages/b2/c1/e6f8c5f28f9b3bdb5c9c1d349a51941a30f90347b82bd5594363e81cf3ff/nptyping-2.4.1-py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="5ccc9bd3d284af1ffaef32ab7f3eb71f584c8c4e71c1dfac0999054ea47beb1c",
        url="https://pypi.org/packages/ad/5b/e8c90a98b8462768ca43ad43021d404b81430fde28a6e8f93a8101fe9a8f/nptyping-1.4.1-py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="9f782826d5749fd8448c156b46b2deb84b3a09db860ac4a9881f4e5bd5181afd",
        url="https://pypi.org/packages/73/11/9e15ef1cd231182a3b568b65a612a173061d826de805481f44848fc27a32/nptyping-1.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2:")
        depends_on("py-numpy@1.21.5", when="@2.1.2: ^python@:3.7")
        depends_on("py-numpy@1.20.0:1", when="@2.1.2: ^python@3.8:")
        depends_on("py-numpy", when="@:1")
        depends_on("py-typing-extensions@4:", when="@2.1: ^python@:3.9")
        depends_on("py-typish@1.7:", when="@1.4:1")
        depends_on("py-typish@1.5.2:", when="@1:1.3")
