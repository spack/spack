# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class WaylandProtocols(MesonPackage, AutotoolsPackage):
    """wayland-protocols contains Wayland protocols that add functionality not
    available in the Wayland core protocol. Such protocols either add
    completely new functionality, or extend the functionality of some other
    protocol either in Wayland core, or some other protocol i
    n wayland-protocols."""

    homepage = "https://wayland.freedesktop.org/"
    url = "https://gitlab.freedesktop.org/wayland/wayland-protocols/-/archive/1.20/wayland-protocols-1.20.tar.gz"
    list_url = "https://gitlab.freedesktop.org/wayland/wayland-protocols/-/tags"
    git = "https://gitlab.freedesktop.org/wayland/wayland-protocols"

    maintainers("wdconinc")

    build_system(
        conditional("autotools", when="@:1.23"),
        conditional("meson", when="@1.21:"),
        default="meson",
    )

    license("MIT")

    version("1.31", sha256="04d3f66eca99d638ec8dbfdfdf79334290e22028f7d0b04c7034d9ef18a3248a")
    version("1.30", sha256="1c02ce27d5267c904f2f0d31039265f3e4112f15bf274b1c72bdacd5322f243d")
    version("1.29", sha256="4a85786ae69cd6d53bbe9278572f3c3d6ea342875ea444960edb6089237c3a18")
    version("1.28", sha256="914dfa09e7e866e913b27d2d9bda0e20e728c7b1c831fd3db71538d9f99a4869")
    version("1.27", sha256="6dd6ee86478adf4347f3b8b4f3da62dbe9e44912c9cef21cf99abfe692313df4")
    version("1.26", sha256="fe56386f436a84e97c3b6a61b76306f205a64425900f247ad0048174b9c32d4d")
    version("1.25", sha256="4326e2b5e04e459ab4522e83e19bff101a3faf9b085bcf46b6cabbd392cc4458")
    version("1.24", sha256="71a171f964e4fe25cede281a2939ac5298ddaba9a5dd8a217db66843a532d064")
    version("1.23", sha256="1ffd6f90eb247ff79de50ac10490ed03100572fb571cebef4df9ec74a271b2af")
    version("1.22", sha256="92f3d88192bf5377300dee654a78e296aca20e2f8e1ed95024f0f91513760a94")
    version("1.20", sha256="b59cf0949aeb1f71f7db46b63b1c5a6705ffde8cb5bd194f843fbd9b41308dda")

    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
        depends_on("m4", type="build")

    with when("build_system=meson"):
        depends_on("meson@0.55:")

    depends_on("pkgconfig", type="build")
    depends_on("doxygen", type="build")
    depends_on("xmlto", type="build")
    depends_on("libxslt", type="build")
    depends_on("wayland")
