# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XorgSgmlDoctools(AutotoolsPackage, XorgPackage):
    """This package provides a common set of SGML entities and XML/CSS style
    sheets used in building/formatting the documentation provided in other
    X.Org packages."""

    homepage = "https://cgit.freedesktop.org/xorg/doc/xorg-sgml-doctools"
    xorg_mirror_path = "doc/xorg-sgml-doctools-1.11.tar.gz"

    maintainers("wdconinc")

    version("1.12", sha256="985a0329e6a6dadd6ad517f8d54f8766ab4b52bb8da7b07d02ec466bec444bdb")
    version("1.11", sha256="986326d7b4dd2ad298f61d8d41fe3929ac6191c6000d6d7e47a8ffc0c34e7426")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
