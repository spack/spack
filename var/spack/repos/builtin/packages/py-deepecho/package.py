# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeepecho(PythonPackage):
    """DeepEcho is a Synthetic Data Generation Python library
    for mixed-type, multivariate time series."""

    homepage = "https://github.com/sdv-dev/DeepEcho"
    pypi = "deepecho/deepecho-0.3.0.post1.tar.gz"

    license("MIT")

    version(
        "0.3.0.post1",
        sha256="a0fc284e330fd65acdba49c46399a2d3019ed9caaf85eb1d05bb44abae3d618f",
        url="https://pypi.org/packages/a8/68/ef5ff2f4767003ce9999d2400904b81d842d7b155168a80c767507a384e8/deepecho-0.3.0.post1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.9", when="@0.3")
        depends_on("py-numpy@1.18.0:1.19", when="@0.3 ^python@:3.6")
        depends_on("py-numpy@1.20.0:1", when="@0.3 ^python@3.7:")
        depends_on("py-pandas@1.1.3:1", when="@0.3")
        depends_on("py-torch@1.8:1", when="@0.3")
        depends_on("py-tqdm@4.15:", when="@0.3:")
