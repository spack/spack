# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUvicorn(PythonPackage):
    """The lightning-fast ASGI server."""

    homepage = "https://www.uvicorn.org/"
    pypi = "uvicorn/uvicorn-0.20.0.tar.gz"

    version("0.20.0", sha256="a4e12017b940247f836bc90b72e725d7dfd0c8ed1c51eb365f5ba30d9f5127d8")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-hatchling", type="build")

    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-h11@0.8:", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
