# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLspServer(PythonPackage):
    """A Python 3.7+ implementation of the Language Server Protocol."""

    homepage = "https://github.com/python-lsp/python-lsp-server"
    pypi = "python-lsp-server/python-lsp-server-1.6.0.tar.gz"

    maintainers("alecbcs")

    license("MIT")

    version(
        "1.10.0",
        sha256="1a9f338bd7cf3cdde5ae85a2bd93fd5be9e55249f6482d88f99fb6227215424a",
        url="https://pypi.org/packages/91/f7/3b9c3a588e46bbdc2671d8fd07ecee118a672db50d72656b5726fbeffbcd/python_lsp_server-1.10.0-py3-none-any.whl",
    )
    version(
        "1.7.1",
        sha256="8f8b382868b161199aa385659b28427890be628d86f54810463a4d0ee0d6d091",
        url="https://pypi.org/packages/ef/9e/19bf0ede5cf6d052482a9aa02bc0bdea8a019aafd589efc2db0124a0af1d/python_lsp_server-1.7.1-py3-none-any.whl",
    )
    version(
        "1.7.0",
        sha256="9468a34e56b840baa52bdf560e04f3e025ee9419aa5dba1f0b3941e86191a1b9",
        url="https://pypi.org/packages/4f/af/8b0fe34d0827f23d949f842780e40236aaf8a2ab67c9bb460c99697a2c00/python_lsp_server-1.7.0-py3-none-any.whl",
    )
    version(
        "1.6.0",
        sha256="7ea502b1d392888efb841cbfdabb33e6ec96e44ab4cb81dd38aacefe657b1abf",
        url="https://pypi.org/packages/ca/bb/1b0df050aaf10e6aacdb15dc0f3ed58b32cb0fa0661d278e1cf57bdb1b65/python_lsp_server-1.6.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.8:")
        depends_on("python@3.7:", when="@1.4:1.7")
        depends_on("py-docstring-to-markdown", when="@1.6:")
        depends_on("py-importlib-metadata@4.8.3:", when="@1.8: ^python@:3.9")
        depends_on("py-jedi@0.17.2:", when="@1.8:")
        depends_on("py-jedi@0.17.2:0.18", when="@:1.7")
        depends_on("py-pluggy@1:1.0.0.0,1.1:", when="@1.4:")
        depends_on("py-python-lsp-jsonrpc@1.1:", when="@1.8:")
        depends_on("py-python-lsp-jsonrpc", when="@:1.7")
        depends_on("py-setuptools@39:", when="@:1.7")
        depends_on("py-ujson@3:")
