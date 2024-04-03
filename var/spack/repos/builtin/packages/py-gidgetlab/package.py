# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGidgetlab(PythonPackage):
    """An asynchronous GitLab API library."""

    homepage = "https://gitlab.com/beenje/gidgetlab"
    pypi = "gidgetlab/gidgetlab-1.1.0.tar.gz"
    git = "https://gitlab.com/beenje/gidgetlab.git"

    maintainers("alecbcs")

    license("Apache-2.0")

    version(
        "1.1.0",
        sha256="56f23d7cc8241bfc2b3703aaf5783877f5b6c101db623c6fbfb0e7c6f006ad1a",
        url="https://pypi.org/packages/d3/5b/ba74da3bfd3b52ea3c8b2b1015025cf4684992d79d1295e186e35bebe82e/gidgetlab-1.1.0-py3-none-any.whl",
    )

    variant(
        "aiohttp", default=False, description="Enable aiohttp functionality through dependency."
    )

    with default_args(type="run"):
        depends_on("py-aiohttp", when="+aiohttp")
        depends_on("py-cachetools", when="@0.3:+aiohttp")
