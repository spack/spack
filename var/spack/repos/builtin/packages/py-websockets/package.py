# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyWebsockets(PythonPackage):
    """websockets is a library for building WebSocket servers and
    clients in Python with a focus on correctness and simplicity."""

    homepage = "https://github.com/aaugustin/websockets"
    url = "https://github.com/aaugustin/websockets/archive/8.1.tar.gz"

    version("10.3", sha256="f13384865a14e0beff240b8f835b5b6a105b32928854841f167d920b4be8e75e")
    version("10.1", sha256="181d2b25de5a437b36aefedaf006ecb6fa3aa1328ec0236cdde15f32f9d3ff6d")
    version("8.1", sha256="c19ce96ad5f7606127d3915364144df93fb865a215784b06048fae3d39364f14")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.6.1:", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"), when="@10.1:")
