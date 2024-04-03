# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPortend(PythonPackage):
    """TCP port monitoring and discovery"""

    homepage = "https://github.com/jaraco/portend"
    pypi = "portend/portend-2.5.tar.gz"

    license("MIT")

    version(
        "2.5",
        sha256="d2dca12e585ce29fc357b31ce424a27c16e2d485029252bbf8ddcc9696207976",
        url="https://pypi.org/packages/0a/f5/0e5fe0bba1450034f023519aed3ca326bc42981475a93e3645ab868f351c/portend-2.5-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-tempora@1.8:", when="@2:")
