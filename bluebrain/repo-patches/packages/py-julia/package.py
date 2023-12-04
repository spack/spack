# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJulia(PythonPackage):
    """python interface to julia"""

    homepage = "https://github.com/JuliaPy/pyjulia"
    pypi = "julia/julia-0.6.1.tar.gz"

    maintainers("tristan0x")

    version("0.6.1", sha256="dbada3b47cb14b3e1893dae8339053e014cf09f8158f408b6a129ca4dfca1f61")

    depends_on("python@3.4:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("julia", type=("build", "run"))
