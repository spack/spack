# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPamela(PythonPackage):
    """Python wrapper for PAM"""

    pypi = "pamela/pamela-1.0.0.tar.gz"

    license("MIT")

    version(
        "1.0.0",
        sha256="b54be508a13bb3d983d117f7b069b31545003ae989791f467cf941376c807f20",
        url="https://pypi.org/packages/9c/b8/f7592a30aa95ffdea4f2e01aca87c15a7a315ba34f835235291eeba22779/pamela-1.0.0-py2.py3-none-any.whl",
    )
