# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQsymm(PythonPackage):
    """Qsymm is a symmetry finder and symmetric Hamiltonian generator.
    It automatically generates model Hamiltonians from symmetry
    constraints and finds the full symmetry group of your Hamiltonian."""

    homepage = "https://gitlab.kwant-project.org/qt/qsymm"
    pypi = "qsymm/qsymm-1.2.7.tar.gz"
    git = "https://gitlab.kwant-project.org/qt/qsymm.git"

    # Add a list of GitHub accounts to notify when the
    # package is updated
    maintainers("payerle")

    license("BSD-2-Clause")

    version(
        "1.2.7",
        sha256="2547ceac2dd46b9874a04cdf2c9518fd4522df15fd6a0f0978f98f3475eddd9b",
        url="https://pypi.org/packages/c6/4a/648c216ce56c617789410133a9c8dd0b568408f9bc0080bebcb468164032/qsymm-1.2.7-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy@1.13.0:", when="@:1.2")
        depends_on("py-scipy@0.19:", when="@1.2.6:1.2")
        depends_on("py-sympy@1.1:", when="@1.1:1.2")
        depends_on("py-tinyarray", when="@:1.2")
