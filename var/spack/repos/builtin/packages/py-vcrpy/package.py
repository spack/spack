# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVcrpy(PythonPackage):
    """Automatically mock your HTTP interactions to simplify and speed up testing."""

    homepage = "https://github.com/kevin1024/vcrpy"
    pypi = "vcrpy/vcrpy-4.1.1.tar.gz"

    license("MIT")

    version(
        "5.1.0",
        sha256="605e7b7a63dcd940db1df3ab2697ca7faf0e835c0852882142bafb19649d599e",
        url="https://pypi.org/packages/2a/5b/3f70bcb279ad30026cc4f1df0a0491a0205a24dddd88301f396c485de9e7/vcrpy-5.1.0-py2.py3-none-any.whl",
    )
    version(
        "4.2.1",
        sha256="efac3e2e0b2af7686f83a266518180af7a048619b2f696e7bad9520f5e2eac09",
        url="https://pypi.org/packages/8b/c5/f9efe3fea61a844ef1c47c800139d02984442a3a61ab4608fb2a682bc78d/vcrpy-4.2.1-py2.py3-none-any.whl",
    )
    version(
        "4.1.1",
        sha256="12c3fcdae7b88ecf11fc0d3e6d77586549d4575a2ceee18e82eee75c1f626162",
        url="https://pypi.org/packages/6e/62/571e9fa5c2a2c986c001d1be99403a5e800d2e72b905e6b1e951148c75c9/vcrpy-4.1.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@5:")
        depends_on("python@3.7:", when="@4.2:4")
        depends_on("py-pyyaml", when="@:5")
        depends_on("py-six@1.5:", when="@:5.0")
        depends_on("py-urllib3@:1", when="@4.3.1:5 ^python@:3.9")
        depends_on("py-wrapt", when="@:5")
        depends_on("py-yarl", when="@:5")

    # Historical dependencies
