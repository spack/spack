# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydeprecate(PythonPackage):
    """Simple tooling for marking deprecated functions or classes and re-routing
    to the new successors' instance."""

    homepage = "https://borda.github.io/pyDeprecate/"
    pypi = "pyDeprecate/pyDeprecate-0.3.0.tar.gz"

    license("MIT")

    version(
        "0.3.1",
        sha256="b5dd8c4c0535854b6a52936d1256883a940e3b02006fc7118b53027c0acde181",
        url="https://pypi.org/packages/a2/17/ff7ec2752f53ea245499b23ee64e76d12f45fcde7a5b1b445f9c58cd1ec0/pyDeprecate-0.3.1-py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="2497dd3a293eb62304ea28cacf5e4e58af8a773b4cefec8dc11a3121d06b8354",
        url="https://pypi.org/packages/14/52/aa227a0884df71ed1957649085adf2b8bc2a1816d037c2f18b3078854516/pyDeprecate-0.3.0-py3-none-any.whl",
    )
