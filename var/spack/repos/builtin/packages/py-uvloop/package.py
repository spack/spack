# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUvloop(PythonPackage):
    """uvloop is a fast, drop-in replacement of the built-in asyncio event"""

    homepage = "https://github.com/MagicStack/uvloop"
    pypi = "uvloop/uvloop-0.14.0.tar.gz"

    version("0.16.0", sha256="f74bc20c7b67d1c27c72601c78cf95be99d5c2cdd4514502b4f3eb0933ff1228")
    version("0.14.0", sha256="123ac9c0c7dd71464f58f1b4ee0bbd81285d96cdda8bc3519281b8973e3a461e")

    depends_on("python@3.7:", when="@0.15:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
