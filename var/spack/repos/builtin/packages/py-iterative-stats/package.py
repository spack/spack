# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIterativeStats(PythonPackage):
    """Bacis iterative statistics implementation."""

    pypi = "iterative-stats/iterative_stats-0.1.0.tar.gz"
    git = "https://github.com/IterativeStatistics/BasicIterativeStatistics.git"
    maintainers("robcaulk")

    license("BSD-3-Clause")

    version(
        "0.1.0",
        sha256="104cd3cdb9bda7f3cb48a8df538ce4f673f7a7327ab1a2b64d31b3190fe80157",
        url="https://pypi.org/packages/3d/e8/7266f17ae002ccd06cda9a6fac2fe8d1de7b1db2160b6d7f226d9a9773fe/iterative_stats-0.1.0-py3-none-any.whl",
    )
    version(
        "0.0.4",
        sha256="97e08023fed9988142e4bd98ba9d19521ac3e2e2bbe0c3bf80fb77f3ea023bec",
        url="https://pypi.org/packages/c7/66/cbc52f9d7f17524abe306e0408a3797378932c3cdaa822a24c7ec51dece6/iterative_stats-0.0.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:3.10", when="@0.0.2:")
        depends_on("py-numpy@1.19.0:1")
        depends_on("py-pyyaml@6.0:6.0.0")

    # main dependencies

    # dev dependencies
