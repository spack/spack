# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUcMicroPy(PythonPackage):
    """Micro subset of unicode data files for linkify-it-py projects."""

    homepage = "https://github.com/tsutsu3/uc.micro-py"
    pypi = "uc-micro-py/uc-micro-py-1.0.2.tar.gz"

    license("MIT")

    version(
        "1.0.2",
        sha256="8c9110c309db9d9e87302e2f4ad2c3152770930d88ab385cd544e7a7e75f3de0",
        url="https://pypi.org/packages/d1/1c/5aeb94aa980da111e4fd0c0fbe5ad95ed5bf9bd957f8e2a6178b85ff4da8/uc_micro_py-1.0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.0.2:")
