# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArt(PythonPackage):
    """ASCII art library for Python."""

    homepage = "https://www.ascii-art.site"
    pypi = "art/art-6.1.tar.gz"

    license("MIT")

    version(
        "6.1",
        sha256="159819c418001467f8d79616fa0814277deac97c8a363d1eb3e7c0a31526bfc3",
        url="https://pypi.org/packages/fc/53/d8792ac2ebb494db0e0ba3ad3f0a9ee71144a5ced266441166f7d038a37e/art-6.1-py3-none-any.whl",
    )
