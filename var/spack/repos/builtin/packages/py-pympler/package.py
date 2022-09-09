# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPympler(PythonPackage):
    """Development tool to measure, monitor and analyze the memory behavior
    of Python objects in a running Python application.
    """

    homepage = "https://github.com/pympler/pympler"
    pypi = "Pympler/Pympler-0.4.3.tar.gz"

    version("1.0.1", sha256="993f1a3599ca3f4fcd7160c7545ad06310c9e12f70174ae7ae8d4e25f6c5d3fa")
    version("0.4.3", sha256="430528fff6cde1bae0a305e8df647b158c3cc4930cff122bf228293829ee1e56")
    version("0.4.2", sha256="3c3f9d8eb3dddf4f29c433433ea77c9c3f2f0dcc06575c0c2a9d81b2602893b2")
    version("0.4.1", sha256="6a8bfd2972c4ec34ac8750358515950be4a4ca13dfa6a05a9a22419786745f90")
    version("0.4", sha256="b280480502df658b18cb6310d2c744fabf05d4c518f873377884b4d4b5d2992d")
    version("0.3.1", sha256="8cb170fddfe592342856590e2239e8c20ac61eacf18bc4f65a95ccaf74475e3e")

    depends_on("python@3.6:3.10", when="@1:", type=("build", "run"))
    depends_on("python@2.7,3.5:3.9", when="@0.9", type=("build", "run"))
    depends_on("python@2.7,3.4:3.8", when="@0.8", type=("build", "run"))
    depends_on("python@2.7,3.3:3.7", when="@0.6:0.7", type=("build", "run"))
    depends_on("python@2.6:2.7,3.2:3.6", when="@0.5", type=("build", "run"))
    depends_on("python@2.5:2.7,3.1:3.4", when="@0.4", type=("build", "run"))
    depends_on("python@2.4:2.7,3.1:3.3", when="@0.3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
