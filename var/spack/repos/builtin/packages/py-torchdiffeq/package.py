# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchdiffeq(PythonPackage):
    """ODE solvers and adjoint sensitivity analysis in PyTorch."""

    homepage = "https://github.com/rtqichen/torchdiffeq"
    pypi = "torchdiffeq/torchdiffeq-0.2.3.tar.gz"

    license("MIT")

    version(
        "0.2.3",
        sha256="b5b01ec1294a2d8d5f77e567bf17c5de1237c0573cb94deefa88326f0e18c338",
        url="https://pypi.org/packages/2c/9b/b9c3e17f261e30f630511390e0dd33fc529073f1f2db222a1f09dc49a1ae/torchdiffeq-0.2.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@0.1:")
        depends_on("py-scipy@1.4.0:", when="@0.2.2:")
        depends_on("py-torch@1.3:", when="@0.1:")
