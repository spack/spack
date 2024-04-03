# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySparse(PythonPackage):
    """This library provides multi-dimensional sparse arrays."""

    homepage = "https://sparse.pydata.org"
    url = "https://github.com/pydata/sparse/archive/0.11.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.11.2",
        sha256="08b937109203a69d1937ad7ea47a3ca4a552a48f7b5c40ba485b37ae6653b204",
        url="https://pypi.org/packages/e3/82/d58361f8107e8686196b91319edf2c26490667b8340cc229b668ee7a1582/sparse-0.11.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@:0.13")
        depends_on("py-numba@0.49:", when="@0.10:")
        depends_on("py-numpy", when="@0.8:0.11")
        depends_on("py-scipy@0.19:")
