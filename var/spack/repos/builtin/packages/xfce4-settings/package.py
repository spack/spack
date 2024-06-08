# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xfce4Settings(AutotoolsPackage):
    """Daemon, manager, and editor to centralize the configuration management for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/xfce4-settings/start"
    url = "https://archive.xfce.org/xfce/4.16/src/xfce4-settings-4.16.0.tar.bz2"

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("4.16.0", sha256="67a1404fc754c675c6431e22a8fe0e5d79644fdfadbfe25a4523d68e1442ddc2")

    variant("xfce4", default=True, description="Match XFCE4 versions")
    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("xcursor", default=True, description="Build with Xcursor support")
    variant("notify", default=True, description="Build with libnotify support")

    # Base requirements
    with default_args(type=("build", "link", "run")):
        depends_on("xfconf")
        depends_on("libxfce4ui")
        depends_on("garcon")
        depends_on("exo")
        #depends_on("glib@2:")
        #depends_on("gtkplus@3:")
        depends_on("dbus-glib")
        depends_on("libxi")
        depends_on("libxrandr")

        depends_on("libxcursor", when="+xcursor")
        depends_on("libnotify", when="+notify")

    depends_on("intltool@0.39.0:", type="build")
    depends_on("libxfce4util+introspection", when="+introspection")
    depends_on("libxfce4ui+introspection", when="+introspection")
    depends_on("gobject-introspection", when="+introspection")

    depends_on("xfconf+xfce4@4.16", when="+xfce4")
    depends_on("libxfce4ui+xfce4@4.16", when="+xfce4")
    depends_on("exo+xfce4@4.16.0", when="+xfce4")

    with default_args(type=("build", "link", "run")):
        with when("@4.16.0:"):
            depends_on("xfconf@4.16:")
            depends_on("libxfce4ui@4.16:")
            depends_on("exo@4.16.0:")
            depends_on("garcon@0.8.0:")
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")
            depends_on("gobject-introspection@1.60:", when="+introspection")

    def configure_args(self):
        args = []
        args += self.enable_or_disable("introspection")
        return args
