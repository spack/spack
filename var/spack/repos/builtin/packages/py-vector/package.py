# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVector(PythonPackage):
    """Vector classes and utilities"""

    homepage = "https://github.com/scikit-hep/vector"
    pypi = "vector/vector-0.8.4.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.8.5",
        sha256="fccc2095edc93e2356dde116f37fa239b6268901dd98e35585f74480a31c4b17",
        url="https://pypi.org/packages/e8/d0/6b0e698190a47c8dea2800c114711b6badceef3d6c4db6c50c57b8e3aa9f/vector-0.8.5-py3-none-any.whl",
    )
    version(
        "0.8.4",
        sha256="4d42865b08202850f58b21126fe8c3c884add75999985f70e7974cbed6f2e966",
        url="https://pypi.org/packages/70/f2/058cde3474ff40a866050e71e2fc47fd22e33ceb5cd0ac90b02f8e9e3f2b/vector-0.8.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-importlib-metadata@0.22:", when="@0.8.2:1.0 ^python@:3.7")
        depends_on("py-numpy@1.13.3:", when="@0.8:")
        depends_on("py-packaging@19:", when="@0.8.2:")
        depends_on("py-typing-extensions", when="@0.8:1.0 ^python@:3.7")
