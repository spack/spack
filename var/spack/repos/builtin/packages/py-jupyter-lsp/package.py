# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterLsp(PythonPackage):
    """Multi-Language Server WebSocket proxy for Jupyter Notebook/Lab server."""

    homepage = "https://github.com/jupyter-lsp/jupyterlab-lsp"
    pypi = "jupyter-lsp/jupyter-lsp-2.2.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.2.0",
        sha256="9e06b8b4f7dd50300b70dd1a78c0c3b0c3d8fa68e0f2d8a5d1fbab62072aca3f",
        url="https://pypi.org/packages/8f/b6/a1571e48550855a79898f851f57e5858b00eb36b09ea3b1a8bb65c53a290/jupyter_lsp-2.2.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@2:")
        depends_on("py-importlib-metadata@4.8.3:", when="@2: ^python@:3.9")
        depends_on("py-jupyter-server@1.1.2:")
