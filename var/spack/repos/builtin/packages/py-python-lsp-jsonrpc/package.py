# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLspJsonrpc(PythonPackage):
    """A Python 3.7+ server implementation of the JSON RPC 2.0 protocol."""

    homepage = "https://github.com/python-lsp/python-lsp-jsonrpc"
    pypi = "python-lsp-jsonrpc/python-lsp-jsonrpc-1.0.0.tar.gz"

    maintainers("alecbcs")

    version("1.0.0", sha256="7bec170733db628d3506ea3a5288ff76aa33c70215ed223abdb0d95e957660bd")

    depends_on("py-setuptools", type="build")
    depends_on("py-ujson@3.0.0:", type=("build", "run"))
