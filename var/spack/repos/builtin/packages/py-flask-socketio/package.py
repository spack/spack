# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskSocketio(PythonPackage):
    """Flask-SocketIO gives Flask applications access to low latency
    bi-directional communications between the clients and the server.
    The client-side application can use any of the SocketIO official clients
    libraries in Javascript, C++, Java and Swift, or any compatible client to
    establish a permanent connection to the server.
    """

    homepage = "https://flask-socketio.readthedocs.io"
    pypi = "Flask-SocketIO/Flask-SocketIO-2.9.6.tar.gz"

    version(
        "2.9.6",
        sha256="be85842328f7847f511cf8cd828739884403b86ab5b0d576dae4241dd920b415",
        url="https://pypi.org/packages/cd/70/ae4a055477ecad475eec4990eb3474b152ff525ed10690afdcf180aee06c/Flask_SocketIO-2.9.6-py2.py3-none-any.whl",
    )
