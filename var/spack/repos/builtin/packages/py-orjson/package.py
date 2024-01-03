# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOrjson(PythonPackage):
    """Fast, correct Python JSON library supporting dataclasses, datetimes, and numpy."""

    homepage = "https://github.com/ijl/orjson"
    pypi = "orjson/orjson-3.8.7.tar.gz"

    license("Apache-2.0")

    version("3.8.7", sha256="8460c8810652dba59c38c80d27c325b5092d189308d8d4f3e688dbd8d4f3b2dc")

    depends_on("py-maturin@0.13:0.14", type="build")
