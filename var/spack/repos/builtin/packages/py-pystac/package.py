# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPystac(PythonPackage):
    """Python library for working with Spatiotemporal Asset Catalog (STAC)."""

    homepage = "https://github.com/azavea/pystac.git"
    pypi = "pystac/pystac-0.5.4.tar.gz"

    license("Apache-2.0")

    version(
        "1.4.0",
        sha256="7f4563ff7cad512fe687ceb0b09905e15934712ac936d51766b090600580abdd",
        url="https://pypi.org/packages/83/af/559781e42676f76febc5b9dc2385c1930834123c3c63b9e004a4c8c9ee52/pystac-1.4.0-py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="8897e4621d631e85f926254837823a5c06eb8f88fea4e9201e985d727017ff49",
        url="https://pypi.org/packages/44/1d/cbe1f6f923ec60c8ac8c4cd81e82ee2d20a7a2f03a694d35c582f0bd7424/pystac-1.3.0-py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="a47039e0997216d28177dfe42f74bb9297af9b0d4eb3f2aead5c27b7ee21223b",
        url="https://pypi.org/packages/ee/ba/45b0862bd505a211c01482a46c43bd71b1c03bd1a3d9977764b35d5dddb8/pystac-1.2.0-py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="107e5e1646a5accac27771d110945afaa9b7e8105f3823451fbb89ecc29fb395",
        url="https://pypi.org/packages/c6/37/28140fa27b46285ce66751656ed07d9ae96bd12841db406900793d92bd7f/pystac-1.1.0-py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="a22575494df7ee19fc1570555f8180b7d5e2c2efa5a355a63d572f3c323e6ce9",
        url="https://pypi.org/packages/9d/73/f45629060d6456cc55e74ee3ba13d0ff1637ea78f38d0bb0ea2b993f8b29/pystac-1.0.1-py3-none-any.whl",
    )
    version(
        "0.5.4",
        sha256="d617e1eef351788fcc7b856e8492c8387e883a0b2695ee17200cb85fbe1da122",
        url="https://pypi.org/packages/69/17/86b6e1531e1295c52d400e0a7d03b2d3a4ae75d92faec6fa00265a05ef86/pystac-0.5.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.0.0-rc3:1.5")
        depends_on("py-python-dateutil@2.7:")
        depends_on("py-typing-extensions@3.7:", when="@1.0.0-beta3:1.5 ^python@:3.7")
