# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxrandr(AutotoolsPackage, XorgPackage):
    """libXrandr - X Resize, Rotate and Reflection extension library."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXrandr"
    xorg_mirror_path = "lib/libXrandr-1.5.0.tar.gz"

    version("1.5.3", sha256="3ad316c1781fe2fe22574b819e81f0eff087a8560377f521ba932238b41b251f")
    version("1.5.0", sha256="1b594a149e6b124aab7149446f2fd886461e2935eca8dca43fe83a70cf8ec451")

    depends_on("libx11@1.6:")
    depends_on("libxext")
    depends_on("libxrender")

    depends_on("randrproto@1.5:")
    depends_on("xextproto")
    depends_on("renderproto")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    @property
    def libs(self):
        return find_libraries("libXrandr", self.prefix, shared=True, recursive=True)
