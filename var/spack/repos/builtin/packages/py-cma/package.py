# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCma(PythonPackage):
    """
    Python implementation of CMA-ES Covariance Matrix Adaptation Evolution Str
    ategy for non-linear numerical optimization in Python
    """

    homepage = "https://github.com/CMA-ES/pycma"
    pypi = "cma/cma-3.3.0.tar.gz"

    maintainers("LydDeb")

    version(
        "3.3.0",
        sha256="5cc571b1e2068fcf1c538be36f8f3a870107456fed22ce81c1345a96329e61db",
        url="https://pypi.org/packages/77/70/da60edd6a12a8b4af07e583076c8f039f2a2792a0f0d9219d84522d23493/cma-3.3.0-py3-none-any.whl",
    )

    variant(
        "constrained_solution_tracking",
        default=False,
        description="Build with moarchiving support.",
    )
    variant("plotting", default=False, description="Build with matplotlib support.")

    with default_args(type="run"):
        depends_on("py-matplotlib", when="@3:3.0,3.2:+plotting")
        depends_on("py-numpy", when="@3:3.0,3.2:")
