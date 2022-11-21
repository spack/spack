# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyThrottler(PythonPackage):
    """Zero dependency Python package for easy throttling with asyncio support."""

    homepage = "https://github.com/uburuntu/throttler"
    pypi = "throttler/throttler-1.2.1.tar.gz"

    maintainers = ["charmoniumQ"]

    version("1.2.1", sha256="8b23d3485a96d98484024a850c1887ccc685bead17e86c8a9e4b0335e7d74778")

    depends_on("py-setuptools", type="build")

    patch("setup.patch")
