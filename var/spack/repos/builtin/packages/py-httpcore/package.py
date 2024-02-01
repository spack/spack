# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpcore(PythonPackage):
    """The HTTP Core package provides a minimal low-level HTTP client,
    which does one thing only. Sending HTTP requests."""

    homepage = "https://github.com/encode/httpcore"
    pypi = "httpcore/httpcore-0.11.0.tar.gz"

    license("BSD-3-Clause")

    version("0.16.3", sha256="c5d6f04e2fc530f39e0c077e6a30caa53f1451096120f1f38b954afd0b17c0cb")
    version("0.14.7", sha256="7503ec1c0f559066e7e39bc4003fd2ce023d01cf51793e3c173b864eb456ead1")
    version("0.11.0", sha256="35ffc735d746b83f8fc6d36f82600e56117b9e8adc65d0c0423264b6ebfef7bf")

    depends_on("py-setuptools", type="build")
    depends_on("py-h11@0.13:0.14", when="@0.16.3", type=("build", "run"))
    depends_on("py-h11@0.11:0.12", type=("build", "run"), when="@0.14.7")
    depends_on("py-h11@0.8:0.9", type=("build", "run"), when="@0.11.0")
    depends_on("py-sniffio@1", type=("build", "run"))
    depends_on("py-anyio@3:4", when="@0.16.3", type=("build", "run"))
    depends_on("py-anyio@3", type=("build", "run"), when="@0.14.7")
    depends_on("py-certifi", type=("build", "run"), when="@0.14.7:")
