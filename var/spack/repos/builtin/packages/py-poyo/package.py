# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoyo(PythonPackage):
    """A lightweight YAML Parser for Python"""

    homepage = "https://github.com/hackebrot/poyo"
    url = "https://github.com/hackebrot/poyo/archive/0.4.1.tar.gz"

    license("MIT")

    version(
        "0.4.1",
        sha256="230ec11c2f35a23410c1f0e474f09fa4e203686f40ab3adca7b039c845d8c325",
        url="https://pypi.org/packages/ea/6c/62c76c12015f6a1849446fb73da59be1229312c54d6d05068275e52bf29f/poyo-0.4.1-py2.py3-none-any.whl",
    )
