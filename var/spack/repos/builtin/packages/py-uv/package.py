# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUv(PythonPackage):
    """An extremely fast Python package and project manager, written in Rust."""

    homepage = "https://github.com/astral-sh/uv"
    url = "https://pypi.org/project/uv/"
    pypi = "uv/0.4.15.tar.gz"

    license("APACHE 2.0 or MIT")

    version("0.4.15", md5="bd21c6ca7c53f36fa514a9e7232acae0")

    depends_on("rust@1.81:", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-maturin@1:1", type=("build"))

    executables = ["^uv$"]
