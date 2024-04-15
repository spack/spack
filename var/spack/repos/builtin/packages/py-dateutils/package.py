# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDateutils(PythonPackage):
    """Various utilities for working with date and datetime objects."""

    homepage = "https://github.com/jmcantrell/python-dateutils"
    pypi = "dateutils/dateutils-0.6.12.tar.gz"

    license("0BSD")

    version(
        "0.6.12",
        sha256="f33b6ab430fa4166e7e9cb8b21ee9f6c9843c48df1a964466f52c79b2a8d53b3",
        url="https://pypi.org/packages/1e/23/cbac954194e5132448cfec0148be1318baac99e68ed597b3d7ff4ae5c182/dateutils-0.6.12-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-python-dateutil", when="@0.6.9:")
        depends_on("py-pytz", when="@0.6.9:")
