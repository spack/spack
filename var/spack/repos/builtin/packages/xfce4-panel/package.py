# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xfce4Panel(AutotoolsPackage):
    """Panel manager for Xfce4"""

    homepage = "https://docs.xfce.org/xfce/xfce4-panel/start"
    url = "https://archive.xfce.org/xfce/4.14pre3/src/xfce4-panel-4.13.7.tar.bz2"

    maintainers("teaguesterling")

    license("GPLv2 OR LGPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.13.7", sha256="888e30417342b05d566f5ef5a85791b05117fadbbc2f00bc5f29a30d6ba42ba9")

    variant("xfce4", default=True, description="Match XFCE4 versions")
    variant("introspection", default=True, description="Build with gobject-introspection support", when="@4.14:")
    variant("notification", default=True, description="Build with startup-notification support")

    patch("fix-libxfce4util-gir.patch", when="+introspection@4.13.7")

    # Base requirements
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4ui")
        depends_on("libxfce4util")
        depends_on("exo")
        depends_on("garcon")
        depends_on("libwnck@3:")
        depends_on("glib@2:")
        depends_on("gtkplus@3:")

        depends_on("startup-notification", when="+notification")

    depends_on("libxfce4ui+introspection", when="+introspection")
    depends_on("gobject-introspection", when="+introspection")
    depends_on("intltool@0.51.0:", type="build")

    depends_on("libxfce4ui+xfce4@4.16", when="+xfce4")
    depends_on("exo+xfce4@0.12.7", when="+xfce4")
    depends_on("garcon+xfce4@0.8.0", when="+xfce4")

    with when("@4.13.7:"):
        with default_args(type=("build", "link", "run")):
            depends_on("libxfce4ui@4.16:")
            depends_on("garcon@0.8.0:")
            depends_on("exo@0.12.7:")
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")

            depends_on("gobject-introspection@1.60:", when="+introspection")

    def configure_args(self):
        args = []
        args += self.enable_or_disable("introspection")
        return args

