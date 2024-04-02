# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLinearOperator(PythonPackage):
    """A linear operator implementation, primarily designed for finite-dimensional
    positive definite operators (i.e. kernel matrices)."""

    homepage = "https://github.com/cornellius-gp/linear_operator/"
    pypi = "linear_operator/linear_operator-0.1.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version(
        "0.4.0",
        sha256="55f120f4e3102eaf017f04af911949536beec9009d6a35c26b775637aa4fe026",
        url="https://pypi.org/packages/4e/60/770e7e7fabbada728a47ad5d83e98a608dcbd6aa2ed361085bcfc1fc97b0/linear_operator-0.4.0-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="262b1028ed3cd1ae70d79a3a29b0210301576d9e426a68b8767acdd4abb116a6",
        url="https://pypi.org/packages/3b/c3/d8cad67ed11f8a270c318b1eae726b4c8fa17df33108811b4e79bc2f438c/linear_operator-0.3.0-py3-none-any.whl",
    )
    version(
        "0.1.1",
        sha256="55472043408959f04c8eb6153bc68a487b141b8c1f2fdb84afcdf6c2e04e01f0",
        url="https://pypi.org/packages/e6/3c/a2cbf56429c4e370cdcd76155fc1068d21a812c67655244f0776a27697c7/linear_operator-0.1.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:")
        depends_on("py-scipy")
        depends_on("py-torch@1.11:")
