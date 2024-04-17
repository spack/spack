# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCmaes(PythonPackage):
    """Lightweight Covariance Matrix Adaptation Evolution Strategy (CMA-ES) implementation."""

    homepage = "https://github.com/CyberAgentAILab/cmaes"
    pypi = "cmaes/cmaes-0.10.0.tar.gz"

    maintainers("eugeneswalker")

    license("MIT")

    version(
        "0.10.0",
        sha256="72cea747ad37b1780b0eb6f3c098cee33907fafbf6690c0c02db1e010cab72f6",
        url="https://pypi.org/packages/f7/46/7d9544d453346f6c0c405916c95fdb653491ea2e9976cabb810ba2fe8cd4/cmaes-0.10.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.9.1:")
        depends_on("py-numpy", when="@:0.7.0,0.8.1:")
