# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxfce4windowing(AutotoolsPackage):
    """
    An abstraction library that attempts to present windowing concepts
    (screens, toplevel windows, workspaces, etc.) in a windowing-system-independent manner.
    """

    homepage = "https://docs.xfce.org/xfce/libxfce4windowing/start"
    url = (
        "https://archive.xfce.org/src/xfce/libxfce4windowing/4.20/libxfce4windowing-4.20.2.tar.bz2"
    )

    maintainers("teaguesterling")

    license("LGPLv2", checked_by="teaguesterling")

    version("4.20.2", sha256="0b9b95aee8b868a2953920c2feafc026672ad19584976f19e89119e93ab1abc8")

    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("x11", default=True, description="Build with X11 support")
    variant("wayland", default=False, description="Build with (limited) Wayland support")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    # Undocumented requirement for xfce4-dev-tools which shouldn't be required
    # unless building from the git repo
    depends_on("xfce4-dev-tools", type="build")  # build requires xdt-gen-visibility

    depends_on("gettext", when="@4.20:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4util")
        # depends_on("xfconf")
        # depends_on("glib@2:")
        with when("+introspection"):
            depends_on("gobject-introspection")
            depends_on("libxfce4util+introspection")
        with when("+x11"):
            depends_on("libwnck")
            depends_on("libdisplay-info")
        with when("+wayland"):
            depends_on("wayland")
            depends_on("wayland-protocols")
        with when("@4.20"):
            depends_on("glib@2.72:")
            depends_on("gobject-introspection@1.72:", when="+introspection")

    conflicts("~x11~wayland", msg="Either X11 or Wayland must be selected")

    def configure_args(self):
        args = []

        args += self.enable_or_disable("introspection")
        args += self.enable_or_disable("x11")
        args += self.enable_or_disable("wayland")

        return args
