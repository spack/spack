# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxmu(AutotoolsPackage, XorgPackage):
    """This library contains miscellaneous utilities and is not part of the
    Xlib standard.  It contains routines which only use public interfaces so
    that it may be layered on top of any proprietary implementation of Xlib
    or Xt."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXmu"
    xorg_mirror_path = "lib/libXmu-1.1.2.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.1.4", sha256="3091d711cdc1d8ea0f545a13b90d1464c3c3ab64778fd121f0d789b277a80289")
    version("1.1.2", sha256="e5fd4bacef068f9509b8226017205040e38d3fba8d2de55037200e7176c13dba")

    depends_on("libxt")
    depends_on("libxext")
    depends_on("libx11")

    depends_on("xextproto")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
