# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColoredlogs(PythonPackage):
    """Colored terminal output for Python's logging module"""

    homepage = "https://coloredlogs.readthedocs.io"
    pypi = "coloredlogs/coloredlogs-10.0.tar.gz"
    git = "https://github.com/xolox/python-coloredlogs.git"

    license("MIT")

    version(
        "15.0.1",
        sha256="612ee75c546f53e92e70049c9dbfcc18c935a2b9a53b66085ce9ef6a6e5c0934",
        url="https://pypi.org/packages/a7/06/3d6badcf13db419e25b07041d9c7b4a2c331d3f4e7134445ec5df57714cd/coloredlogs-15.0.1-py2.py3-none-any.whl",
    )
    version(
        "14.0",
        sha256="346f58aad6afd48444c2468618623638dadab76e4e70d5e10822676f2d32226a",
        url="https://pypi.org/packages/5c/2f/12747be360d6dea432e7b5dfae3419132cb008535cfe614af73b9ce2643b/coloredlogs-14.0-py2.py3-none-any.whl",
    )
    version(
        "10.0",
        sha256="34fad2e342d5a559c31b6c889e8d14f97cb62c47d9a2ae7b5ed14ea10a79eff8",
        url="https://pypi.org/packages/08/0f/7877fc42fff0b9d70b6442df62d53b3868d3a6ad1b876bdb54335b30ff23/coloredlogs-10.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-colorama", when="@:12 platform=windows")
        depends_on("py-humanfriendly@9.1:", when="@15:")
        depends_on("py-humanfriendly@7.1:", when="@14")
        depends_on("py-humanfriendly@4.7:", when="@9:10")
