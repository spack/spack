# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Tumbler(AutotoolsPackage):
    """Tumbler is a D-Bus service for applications to request thumbnails for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/tumbler/start"
    url = "https://archive.xfce.org/xfce/4.16/src/tumbler-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce"
    list_depth = 2

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.18.0", sha256="4087f3af4ef31271d3f315421a2f1fe67e4fda7ad60bbab1f073627914dfcf00")
    version("4.16.0", sha256="9b0b7fed0c64041733d490b1b307297984629d0dd85369749617a8766850af66")

    variant("freetype", default=True, description="Build with font support")
    variant("libjpeg", default=True, description="Build with jpeg thumbnail support")
    variant("ffmpeg", default=True, description="Build with ffmpg video support")
    # variant("gstreamer", default=True, description="Build with gstreamer video support")
    variant("poppler", default=True, description="Build with pdf support")
    # variant("libgsf", default=True, description="Build with odf support")
    # variant("libopenraw-gnome", default=True, description="Build with raw image support")

    conflicts("%gcc@13:", when="@:4.16", msg="GCC 13+ fails on implicit pointer casting")

    # Base requirements
    depends_on("intltool@0.35.0:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("glib@2:")
        depends_on("dbus-glib")
        depends_on("gdk-pixbuf")
        depends_on("libpng")
        depends_on("gtkplus@3:")
        depends_on("freetype", when="+freetype")
        depends_on("libjpeg", when="+libjpeg")
        depends_on("ffmpeg", when="+ffmpeg")
        depends_on("poppler+glib", when="+poppler")
        with when("@4.18.0:"):
            depends_on("glib@2.66:")
            depends_on("gtkplus@3.24:")
        with when("@4.16.0:"):
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")

    def configure_args(self):
        args = []

        args += self.enable_or_disable("freetype")
        args += self.enable_or_disable("libjpeg")
        args += self.enable_or_disable("ffmpeg")
        args += self.enable_or_disable("poppler")

        return args
