# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyWebsocketClient(PythonPackage):
    """WebSocket client for Python. hybi13 is supported."""

    homepage = "https://github.com/websocket-client/websocket-client.git"
    pypi = "websocket-client/websocket-client-0.57.0.tar.gz"

    license("Apache-2.0")

    version(
        "1.6.3",
        sha256="6cfc30d051ebabb73a5fa246efdcc14c8fbebbd0330f8984ac3bb6d9edd2ad03",
        url="https://pypi.org/packages/0b/50/49e0d7342e5d441d43b525d6c84656ea40aea3e58d530004d07b22bc9b04/websocket_client-1.6.3-py3-none-any.whl",
    )
    version(
        "1.5.1",
        sha256="cdf5877568b7e83aa7cf2244ab56a3213de587bbe0ce9d8b9600fc77b455d89e",
        url="https://pypi.org/packages/6d/9a/6c793729c9d48fcca155ce55e4dfafacffb7fb52a62e3ae2198846c31af6/websocket_client-1.5.1-py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="398909eb7e261f44b8f4bd474785b6ec5f5b499d4953342fe9755e01ef624090",
        url="https://pypi.org/packages/83/b8/95c2512818d6ddb9b97f4163e915b2afe2db42b620270aa59c5ee0b47245/websocket_client-1.4.1-py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="0133d2f784858e59959ce82ddac316634229da55b498aac311f1620567a710ec",
        url="https://pypi.org/packages/55/44/030ea47390896c8d6dc9995c8e9a4c5df3a161cd45416d88119036c73eda/websocket_client-1.2.1-py2.py3-none-any.whl",
    )
    version(
        "0.57.0",
        sha256="0fc45c961324d79c781bab301359d5a1b00b13ad1b10415a4780229ef71a5549",
        url="https://pypi.org/packages/4c/5f/f61b420143ed1c8dc69f9eaec5ff1ac36109d52c80de49d66e0c36c3dfdf/websocket_client-0.57.0-py2.py3-none-any.whl",
    )
    version(
        "0.56.0",
        sha256="1151d5fb3a62dc129164292e1227655e4bbc5dd5340a5165dfae61128ec50aa9",
        url="https://pypi.org/packages/29/19/44753eab1fdb50770ac69605527e8859468f3c0fd7dc5a76dd9c4dbd7906/websocket_client-0.56.0-py2.py3-none-any.whl",
    )
    version(
        "0.48.0",
        sha256="db70953ae4a064698b27ae56dcad84d0ee68b7b43cb40940f537738f38f510c1",
        url="https://pypi.org/packages/8a/a1/72ef9aa26cfe1a75cee09fc1957e4723add9de098c15719416a1ee89386b/websocket_client-0.48.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.6.2:")
        depends_on("python@3.7:", when="@1.3.2:1.6.1")

    # Historical dependencies
