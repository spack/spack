# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPluggy(PythonPackage):
    """Plugin and hook calling mechanisms for python."""

    homepage = "https://github.com/pytest-dev/pluggy"
    pypi = "pluggy/pluggy-0.13.0.tar.gz"

    license("MIT")

    version(
        "1.4.0",
        sha256="7db9f7b503d67d1c5b95f59773ebb58a8c1c288129a88665838012cfb07b8981",
        url="https://pypi.org/packages/a5/5b/0cc789b59e8cc1bf288b38111d002d8c5917123194d45b29dcdac64723cc/pluggy-1.4.0-py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="74134bbf457f031a36d68416e1509f34bd5ccc019f0bcc952c7b909d06b37bd3",
        url="https://pypi.org/packages/9e/01/f38e2ff29715251cf25532b9082a1589ab7e4f571ced434f98d0139336dc/pluggy-1.0.0-py2.py3-none-any.whl",
    )
    version(
        "0.13.0",
        sha256="0db4b7601aae1d35b4a033282da476845aa19185c1e6964b25cf324b5e4ec3e6",
        url="https://pypi.org/packages/92/c7/48439f7d5fd6bddb4c04b850bb862b42e3e2b98570040dfaf68aedd8114b/pluggy-0.13.0-py2.py3-none-any.whl",
    )
    version(
        "0.12.0",
        sha256="b9817417e95936bf75d85d3f8767f7df6cdde751fc40aed3bb3074cbcb77757c",
        url="https://pypi.org/packages/06/ee/de89e0582276e3551df3110088bf20844de2b0e7df2748406876cc78e021/pluggy-0.12.0-py2.py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="84d306a647cc805219916e62aab89caa97a33a1dd8c342e87a37f91073cd4746",
        url="https://pypi.org/packages/84/e8/4ddac125b5a0e84ea6ffc93cfccf1e7ee1924e88f53c64e98227f0af2a5f/pluggy-0.9.0-py2.py3-none-any.whl",
    )
    version(
        "0.8.1",
        sha256="980710797ff6a041e9a73a5787804f848996ecaa6f8a1b1e08224a5894f2074a",
        url="https://pypi.org/packages/2d/60/f58d9e8197f911f9405bf7e02227b43a2acc2c2f1a8cbb1be5ecf6bfd0b8/pluggy-0.8.1-py2.py3-none-any.whl",
    )
    version(
        "0.7.1",
        sha256="6e3836e39f4d36ae72840833db137f7b7d35105079aee6ec4a62d9f80d594dd1",
        url="https://pypi.org/packages/f5/f1/5a93c118663896d83f7bcbfb7f657ce1d0c0d617e6b4a443a53abcc658ca/pluggy-0.7.1-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="e160a7fcf25762bb60efc7e171d4497ff1d8d2d75a3d0df7a21b76821ecbf5c5",
        url="https://pypi.org/packages/ba/65/ded3bc40bbf8d887f262f150fbe1ae6637765b5c9534bd55690ed2c0b0f7/pluggy-0.6.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.3:")
        depends_on("py-importlib-metadata@0.12:", when="@0.13:1.2 ^python@:3.7")
        depends_on("py-importlib-metadata@0.12:", when="@0.12")
