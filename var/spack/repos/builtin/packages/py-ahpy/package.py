# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAhpy(PythonPackage):
    """AHPy is an implementation of the Analytic Hierarchy Process (AHP), a
    method used to structure, synthesize and evaluate the elements of a
    decision problem."""

    homepage = "https://github.com/PhilipGriffith/AHPy"
    pypi = "ahpy/ahpy-2.0.tar.gz"

    license("MIT")

    version(
        "2.0",
        sha256="266d6a9c8669f9950188e83620bae47dc9083e41592a91d6890c4e497f13cc44",
        url="https://pypi.org/packages/ab/50/c0af318811c4dee0e72c04110f0d5d6a97df7a5cbd8dcec727d22d3456e4/ahpy-2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3")
        depends_on("py-numpy")
        depends_on("py-scipy")
