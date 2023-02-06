# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.qt_base import QtBase, QtPackage


class QtQuicktimeline(QtPackage):
    """Module for keyframe-based timeline construction."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    version("6.4.2", sha256="af7449bf5954d2309081d6d65af7fd31cb11a5f8dc5f414163120d582f82353f")
    version("6.4.1", sha256="20450687941e6e12e1adf428114776c304d14447d61a4e8b08050c7c18463ee7")
    version("6.4.0", sha256="b5f88beaa726032141fab91b84bc3b268f6213518301c4ddcfa7d116fd08bdab")
    version("6.3.2", sha256="ca6e53a92b022b49098c15f2cc5897953644de8477310696542a03bbbe5666aa")
    version("6.3.1", sha256="ba1e808d4c0fce899c235942df34ae5d349632f61a302d14feeae7465cf1f197")
    version("6.3.0", sha256="09e27bbdefbbf50d15525d26119a00d86eba76d2d1bc9421557d1ed86edcacdf")
    version("6.2.4", sha256="d73cb33e33f0b7a1825b863c22e6b552ae86aa841bcb805a41aca02526a4e8bc")
    version("6.2.3", sha256="bbb913398d8fb6b5b20993b5e02317de5c1e4b23a5357dd5d08a237ada6cc7e2")

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)
        depends_on("qt-declarative@" + v, when="@" + v)
