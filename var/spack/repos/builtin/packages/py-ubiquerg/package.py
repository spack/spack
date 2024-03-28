# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUbiquerg(PythonPackage):
    """Tools for work (erg) everywhere (ubique)."""

    homepage = "https://github.com/pepkit/ubiquerg"
    pypi = "ubiquerg/ubiquerg-0.6.2.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.6.2",
        sha256="6336c4dc2c64fd759585265ad0a307eb48944368de531fb686447d2a93a5779d",
        url="https://pypi.org/packages/51/cd/e2d4c7c4ddc2cb61765d5eeb0484ac2cfe16f6c57d6785e965f0127d7b88/ubiquerg-0.6.2-py2.py3-none-any.whl",
    )
