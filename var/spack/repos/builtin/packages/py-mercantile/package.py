# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMercantile(PythonPackage):
    """Web mercator XYZ tile utilities."""

    homepage = "https://github.com/mapbox/mercantile"
    pypi = "mercantile/mercantile-1.1.6.tar.gz"

    maintainers("adamjstewart")

    version(
        "1.1.6",
        sha256="20895bcee8cb346f384d8a1161fde4773f5b2aa937d90a23aebde766a0d1a536",
        url="https://pypi.org/packages/b9/cd/ee6dbee0abca93edda53703fe408d2a6abdc8c1b248a3c9a4539089eafa2/mercantile-1.1.6-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-click@3:")
