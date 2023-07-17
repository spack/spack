# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLinkifyItPy(PythonPackage):
    """Links recognition library with FULL unicode support."""

    homepage = "https://github.com/tsutsu3/linkify-it-py"
    pypi = "linkify-it-py/linkify-it-py-2.0.2.tar.gz"

    version("2.0.2", sha256="19f3060727842c254c808e99d465c80c49d2c7306788140987a1a7a29b0d6ad2")

    depends_on("python@2.X:2.Y,3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-uc-micro-py", type=("build", "run"))
