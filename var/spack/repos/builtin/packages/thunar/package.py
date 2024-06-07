# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Thunar(AutotoolsPackage):
    """Thunar File Manager"""

    homepage = "https://docs.xfce.org/xfce/thunar/start"
    url = "https://archive.xfce.org/xfce/4.14pre3/src/Thunar-1.8.8.tar.bz2"

    maintainers("teaguesterling")
    license("GPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("1.8.8", sha256="a03761de4a43c36b9daa6029e6e3263a23c8ce429d78a9f9156ab48efdb2800c")

    variant("xfce4", default=True, description="Match XFCE4 versions")
    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("notification", default=True, description="Build with startup-notification support")
    variant("exif", default=True, description="Build with libexif support")
    variant("gdbus", default=True, description="Build with gdbus support")
    variant("notify", default=True, description="Build with libnotify support")
    variant("jpeg", default=True, description="Build with libjpeg support")
    variant("freetype", default=True, description="Build with freetype support")

    # Base requirements
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4util")
        depends_on("xfconf")
        depends_on("libxfce4ui")
        depends_on("exo")
        depends_on("xfce4-panel")
        depends_on("libpng")
        depends_on("glib@2:")
        depends_on("gtkplus@3:")

        depends_on("libexif", when="+exif")
        depends_on("dbus-glib", when="+gdbus")
        depends_on("libnotify", when="+notify")

        depends_on("startup-notification", when="+notification")

    depends_on("libxfce4util+introspection", when="+introspection")
    depends_on("libxfce4ui+introspection", when="+introspection")
    depends_on("xfce4-panel+introspection", when="+introspection")
    depends_on("gobject-introspection", when="+introspection")
    depends_on("intltool@0.39.0:", type="build")

    depends_on("libxfce4util+xfce4@4.16", when="+xfce4")
    depends_on("xfconf+xfce4@4.16", when="+xfce4")
    depends_on("libxfce4ui+xfce4@4.16", when="+xfce4")
    depends_on("exo+xfce4@0.12.7", when="+xfce4")
    depends_on("xfce4-panel@4.13.7", when="+xfce4")

    with when("@1.8.8:"):
        with default_args(type=("build", "link", "run")):
            depends_on("libxfce4util@4.16:")
            depends_on("xfconf@4.16:")
            depends_on("libxfce4ui@4.16:")
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")
            depends_on("exo@0.12.7:")
            depends_on("xfce4-panel@4.13.7:")

            depends_on("gobject-introspection@1.60:", when="+introspection")

    def configure_args(self):
        args = []
        args += self.enable_or_disable("introspection")
        return args

