# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCachecontrol(PythonPackage):
    """CacheControl is a port of the caching algorithms in httplib2
    for use with requests session object."""

    homepage = "https://github.com/ionrock/cachecontrol"
    pypi = "CacheControl/CacheControl-0.12.10.tar.gz"

    license("Apache-2.0")

    version(
        "0.13.1",
        sha256="95dedbec849f46dda3137866dc28b9d133fc9af55f5b805ab1291833e4457aa4",
        url="https://pypi.org/packages/1d/e3/a22348e6226dcd585d5a4b5f0175b3a16dabfd3912cbeb02f321d00e56c7/cachecontrol-0.13.1-py3-none-any.whl",
    )
    version(
        "0.13.0",
        sha256="4544a012a25cf0a73c53cd986f68b4f9c9f6b1df01d741c2923c3d56c66c7bda",
        url="https://pypi.org/packages/65/03/9ed07561cc4b428204fc59fa090ae6652b6fe0a6506c2b05adfcb09085b9/CacheControl-0.13.0-py3-none-any.whl",
    )
    version(
        "0.12.11",
        sha256="2c75d6a8938cb1933c75c50184549ad42728a27e9f6b92fd677c3151aa72555b",
        url="https://pypi.org/packages/83/63/15ce47ede5b03657e920f3f006e56ca9a16f7873978146f2f77e297bdd22/CacheControl-0.12.11-py2.py3-none-any.whl",
    )
    version(
        "0.12.10",
        sha256="b0d43d8f71948ef5ebdee5fe236b86c6ffc7799370453dccb0e894c20dfa487c",
        url="https://pypi.org/packages/d3/39/b7cd9ef1be03ac33e71f76837a23d59842b016e5159cf5aff30c0b340907/CacheControl-0.12.10-py2.py3-none-any.whl",
    )

    variant("filecache", default=False, description="Add lockfile dependency")
    variant("redis", default=False, description="Add redis dependency")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.13.1-rc0:")
        depends_on("py-filelock@3.8:", when="@0.12.12:0.12.13,0.13:+filecache")
        depends_on("py-lockfile@0.9:", when="@0.12.6:0.12.11,0.12.14:0.12+filecache")
        depends_on("py-msgpack@0.5.2:", when="@0.12.6:0.13")
        depends_on("py-redis@2.10.5:", when="@0.12.6:+redis")
        depends_on("py-requests@2.16:", when="@0.13:")
        depends_on("py-requests", when="@0.12.6:0.12")
