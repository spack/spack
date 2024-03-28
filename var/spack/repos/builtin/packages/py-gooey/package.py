# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGooey(PythonPackage):
    """Turn (almost) any command line program into
    a full GUI application with one line"""

    homepage = "https://pypi.org/project/Gooey/"
    pypi = "Gooey/Gooey-1.0.8.1.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version(
        "1.0.8.1",
        sha256="222793cf4a5dd2f9d5c3174ad7369c3df541d91a49e54d51bbee95745ed75ae2",
        url="https://pypi.org/packages/21/03/2d0fc5f982f085ab72c56caa27238339a28419c0da716add1c5e1cf2fa99/Gooey-1.0.8.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-colored@1.3.93:", when="@1.0.3:")
        depends_on("py-pillow@4.3:", when="@1.0.1:")
        depends_on("py-psutil@5.4.2:", when="@1.0.1:")
        depends_on("py-pygtrie@2.3.3:", when="@1.0.6:")
        depends_on("py-wxpython@4.1:", when="@1.0.8.1:")
