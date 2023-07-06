# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyWebsocketClient(PythonPackage):
    """WebSocket client for Python. hybi13 is supported."""

    homepage = "https://github.com/websocket-client/websocket-client.git"
    pypi = "websocket-client/websocket-client-0.57.0.tar.gz"

    version("1.5.1", sha256="3f09e6d8230892547132177f575a4e3e73cfdf06526e20cc02aa1c3b47184d40")
    version("1.4.1", sha256="f9611eb65c8241a67fb373bef040b3cf8ad377a9f6546a12b620b6511e8ea9ef")
    version("1.2.1", sha256="8dfb715d8a992f5712fff8c843adae94e22b22a99b2c5e6b0ec4a1a981cc4e0d")
    version(
        "0.57.0",
        sha256="d735b91d6d1692a6a181f2a8c9e0238e5f6373356f561bb9dc4c7af36f452010",
        url="https://files.pythonhosted.org/packages/source/w/websocket_client/websocket_client-0.57.0.tar.gz",
    )
    version(
        "0.56.0",
        sha256="1fd5520878b68b84b5748bb30e592b10d0a91529d5383f74f4964e72b297fd3a",
        url="https://files.pythonhosted.org/packages/source/w/websocket_client/websocket_client-0.56.0.tar.gz",
    )
    version(
        "0.48.0",
        sha256="18f1170e6a1b5463986739d9fd45c4308b0d025c1b2f9b88788d8f69e8a5eb4a",
        url="https://files.pythonhosted.org/packages/source/w/websocket_client/websocket_client-0.48.0.tar.gz",
    )

    depends_on("python@2.6:2.8,3.4:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@1.2.1:")
    depends_on("python@3.7:", type=("build", "run"), when="@1.4.1:")
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"), when="@:1.2.0")
