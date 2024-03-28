# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFindLibpython(PythonPackage):
    """Finds the libpython associated with your environment, wherever it may be hiding"""

    homepage = "https://github.com/ktbarrett/find_libpython"
    pypi = "find_libpython/find_libpython-0.3.0.tar.gz"

    license("MIT")

    version(
        "0.3.1",
        sha256="f63c2c05b9c6077bfafa5c7b283547b918a54c17fd930ceead487d1f220ff9cb",
        url="https://pypi.org/packages/98/e3/db6c6be0863e0e81c7596f47b5f41449b78d7285de6f17bd8c5f40b6de37/find_libpython-0.3.1-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="93fa14c8d007a7f9e6b650a486e249b49f01fd8d45b83ecf080a78b1a7011214",
        url="https://pypi.org/packages/7a/13/4a99ff41ae6a47ccc45675bd312a238b9606b118a9317c79a4277cd2a00a/find_libpython-0.3.0-py3-none-any.whl",
    )
