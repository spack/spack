# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDiffeqpy(PythonPackage):
    """Solving differential equations in Python using DifferentialEquations.jl
    and the SciML Scientific Machine Learning organization"""

    homepage = "https://github.com/SciML/diffeqpy"
    pypi = "diffeqpy/diffeqpy-2.3.0.tar.gz"

    maintainers("tristan0x")

    version("2.3.0", sha256="14d31321a5463a706733cc137d04e5bcf5cc22d44b6a44958ecd9972752041a1")
    version("1.1.0", sha256="0ff315bf3d4345a83dc623b614e39c8365302df1cc9d36dcb8ce782d926f255b")

    depends_on("py-setuptools", type="build")

    depends_on("py-jill", when="@2:", type=("build", "run"))
    depends_on("py-juliacall", when="@2:", type=("build", "run"))
    depends_on("py-julia", when="@:2", type=("build", "run"))
