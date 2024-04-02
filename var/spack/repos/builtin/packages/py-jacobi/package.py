# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJacobi(PythonPackage):
    """Fast numerical derivatives for analytic functions
    with arbitrary round-off error and error propagation."""

    homepage = "https://github.com/hdembinski/jacobi"
    pypi = "jacobi/jacobi-0.9.2.tar.gz"

    maintainers("jonas-eschle")
    license("MIT", checked_by="jonas-eschle")

    version(
        "0.9.2",
        sha256="7e57b2d9c62d47bce688ef4b3564adeb1def611cf5ed232ec39a6aa6083f7a8c",
        url="https://pypi.org/packages/b0/5c/2d6a44da539db44820b1c053958bfc4ee011e33f4f110175bfc712520440/jacobi-0.9.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.9.2:")
        depends_on("py-numpy", when="@0.9.2:")
