# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPastedeploy(PythonPackage):
    """Load, configure, and compose WSGI applications and servers"""

    homepage = "https://docs.pylonsproject.org/projects/pastedeploy"
    pypi = "PasteDeploy/PasteDeploy-3.0.1.tar.gz"

    license("MIT")

    version(
        "3.0.1",
        sha256="6195c921b1c3ed9722e4e3e6aa29b70deebb2429b4ca3ff3d49185c8e80003bb",
        url="https://pypi.org/packages/ab/8a/1ed1b777d0105bfbf82d83b0a93e4e41d35ed459ab37aaf39f46bc0e9a63/PasteDeploy-3.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@3.0.1:")
        depends_on("py-importlib-metadata", when="@3: ^python@:3.7")
