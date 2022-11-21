# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class QtQuicktimeline(CMakePackage):
    """Module for keyframe-based timeline construction."""

    homepage = "https://www.qt.io"
    url = "https://github.com/qt/qtquicktimeline/archive/refs/tags/v6.2.3.tar.gz"
    list_url = "https://github.com/qt/qtquicktimeline/tags"

    maintainers = ["wdconinc", "sethrj"]

    version("6.3.2", sha256="ca6e53a92b022b49098c15f2cc5897953644de8477310696542a03bbbe5666aa")
    version("6.3.1", sha256="ba1e808d4c0fce899c235942df34ae5d349632f61a302d14feeae7465cf1f197")
    version("6.3.0", sha256="09e27bbdefbbf50d15525d26119a00d86eba76d2d1bc9421557d1ed86edcacdf")
    version("6.2.4", sha256="d73cb33e33f0b7a1825b863c22e6b552ae86aa841bcb805a41aca02526a4e8bc")
    version("6.2.3", sha256="bbb913398d8fb6b5b20993b5e02317de5c1e4b23a5357dd5d08a237ada6cc7e2")

    generator = "Ninja"

    depends_on("cmake@3.16:", type="build")
    depends_on("ninja", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python", when="@5.7.0:", type="build")

    _versions = ["6.3.2", "6.3.1", "6.3.0", "6.2.4", "6.2.3"]
    for v in _versions:
        depends_on("qt-base@" + v, when="@" + v)
        depends_on("qt-declarative@" + v, when="@" + v)

    def cmake_args(self):
        args = [
            # Qt components typically install cmake config files in a single prefix
            self.define("QT_ADDITIONAL_PACKAGES_PREFIX_PATH", self.spec["qt-declarative"].prefix)
        ]
        return args
