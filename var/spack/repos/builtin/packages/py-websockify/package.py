# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyWebsockify(PythonPackage):
    """A WebSocket to TCP proxy/bridge written in Python"""

    homepage = "https://github.com/novnc/websockify/"
    url = "https://github.com/novnc/websockify/archive/refs/tags/v0.12.0.tar.gz"

    maintainers("teaguesterling")

    license("LGPLv3", checked_by="teaguesterling")

    version("0.12.0", sha256="37448ec992ef626f29558404cf6535592d02894ec1d5f0990a8c62621b39a967")
    version("0.11.0", sha256="628dd586e80865cd775cc402b96cf75f4daa647b0fefdc31366d08b7753016be")
    version("0.10.0", sha256="7bd99b727e0be230f6f47f65fbe4bd2ae8b2aa3568350148bdf5cf440c4c6b4a")
    version("0.9.0", sha256="6ebfec791dd78be6584fb5fe3bc27f02af54501beddf8457368699f571de13ae")
    version("0.8.0", sha256="f080e40b3f429f39dc557c62c6d715a683100e7c10c557fa376b6dbde23358ce")
    version("0.7.0", sha256="8a638e90a1a6dfe0862345d069d931df1d496adb15db294bfc7077a5df2deccb")
    version("0.6.1", sha256="1c0c55f767cf4de07535abfc474347d226c896107abc3d700e37f17b45c93de5")
    version("0.6.0", sha256="aeb1bb0079696611045d2f188f38b68c8a4cc50e3c229db9156806c0078d608e")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3:")
        depends_on("py-numpy")
        depends_on("py-requests")
        depends_on("py-jwcrypto")
        depends_on("py-redis")

