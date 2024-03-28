# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPulp(PythonPackage):
    """PuLP is an LP modeler written in Python. PuLP can generate MPS or LP
    files and call GLPK, COIN-OR CLP/CBC, CPLEX, GUROBI, MOSEK, XPRESS, CHOCO,
    MIPCL, SCIP to solve linear problems."""

    homepage = "https://github.com/coin-or/pulp"
    pypi = "PuLP/PuLP-2.6.0.tar.gz"

    maintainers("marcusboden")

    license("MIT")

    version(
        "2.6.0",
        sha256="37ea19fde27c2a767989a40e945d7a44b8c9cf007bd433e2c0a73acbd5e92f0c",
        url="https://pypi.org/packages/37/77/fdaf479eac225c0c172a92be397dbdbc0ef35cb71767c3e8fec804b02239/PuLP-2.6.0-py3-none-any.whl",
    )
