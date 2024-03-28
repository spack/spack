# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyThrottler(PythonPackage):
    """Zero dependency Python package for easy throttling with asyncio support."""

    homepage = "https://github.com/uburuntu/throttler"
    pypi = "throttler/throttler-1.2.1.tar.gz"

    maintainers("charmoniumQ")

    license("MIT")

    version(
        "1.2.2",
        sha256="fc6ae612a2529e01110b32335af40375258b98e3b81232ec77cd07f51bf71392",
        url="https://pypi.org/packages/df/d4/36bf6010b184286000b2334622bfb3446a40c22c1d2a9776bff025cb0fe5/throttler-1.2.2-py3-none-any.whl",
    )
