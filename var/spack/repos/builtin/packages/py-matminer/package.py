# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMatminer(PythonPackage):
    """Matminer is a library for performing data mining in the field of
    materials science."""

    homepage = "https://github.com/hackingmaterials/matminer"
    pypi = "matminer/matminer-0.8.0.tar.gz"

    maintainers("meyersbs")

    version(
        "0.8.0",
        sha256="7d57939c69a8b1d113c85cb5031e94d8d9f68b4a185b34ba17b22c1418abcad3",
        url="https://pypi.org/packages/bf/2c/4843a1de00ede81d7542baee6887d0ca9118a36ef1e9a5e124b42f5ae4cc/matminer-0.8.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-future", when="@0.8:0.9.0")
        depends_on("py-monty", when="@0.8:0.9.0")
        depends_on("py-numpy@1.20.1:", when="@0.8:0.9.0")
        depends_on("py-pandas", when="@0.8")
        depends_on("py-pymatgen", when="@0.8:0.9.0")
        depends_on("py-pymongo", when="@0.8:0.9.0")
        depends_on("py-requests", when="@0.8:0.9.0")
        depends_on("py-scikit-learn", when="@0.8:0.9.0")
        depends_on("py-sympy", when="@0.8:0.9.0")
        depends_on("py-tqdm", when="@0.8:0.9.0")
