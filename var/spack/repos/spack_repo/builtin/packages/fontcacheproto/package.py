# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

from ...build_systems.autotools import AutotoolsPackage
from ...build_systems.xorg import XorgPackage


class Fontcacheproto(AutotoolsPackage, XorgPackage):
    """X.org FontcacheProto protocol headers."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/fontcacheproto"
    xorg_mirror_path = "proto/fontcacheproto-0.1.3.tar.gz"

    license("BSD-2-Clause")

    version("0.1.3", sha256="759b4863b55a25bfc8f977d8ed969da0b99b3c823f33c674d6da5825f9df9a79")
