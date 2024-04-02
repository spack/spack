# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpgl1(PythonPackage):
    """SPGL1 is a solver for large-scale one-norm regularized least squares.  It is
    designed to solve any of the following three problems: Basis pursuit denoise
    (BPDN): minimize ||x||_1 subject to ||Ax - b||_2 <= sigma, Basis pursuit (BP):
    minimize ||x||_1 subject to Ax = b Lasso: minimize ||Ax - b||_2 subject to
    ||x||_1 <= tau, The matrix A can be defined explicitly, or as an operator that
    returns both both Ax and A'b.  SPGL1 can solve these three problems in both
    the real and complex domains."""

    pypi = "spgl1/spgl1-0.0.2.tar.gz"
    git = "https://github.com/drrelyea/spgl1.git"

    maintainers("archxlith")

    license("LGPL-2.1-or-later")

    version(
        "0.0.2",
        sha256="16ddc94a46a574855c605af13f0702b6bc5ccae1208c0685a83226324467226d",
        url="https://pypi.org/packages/17/8e/143c7c424c8c9e8e1ce5f080430b8ec875143dcb00ec9d6edfc1e03efb1c/spgl1-0.0.2-py3-none-any.whl",
    )
    version(
        "0.0.1",
        sha256="5b848cd7ab744a50f367587cf001aa50ce3ea255406cb0f85ad6cd570160ed06",
        url="https://pypi.org/packages/31/be/cd07d566e2e4ea4634c78e40aed9e69ae3fbf2010df6ba0d59307174db9c/spgl1-0.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy@1.15.0:")
        depends_on("py-scipy")
