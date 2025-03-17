# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Exo(AutotoolsPackage):
    """Helper applications for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/exo/start"
    url = "https://archive.xfce.org/xfce/4.16/src/exo-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    license("GPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    maintainers("teaguesterling")

    version("4.20.0", sha256="4277f799245f1efde01cd917fd538ba6b12cf91c9f8a73fe2035fd5456ec078d")
    version("4.18.0", sha256="4f2c61d045a888cdb64297fd0ae20cc23da9b97ffb82562ed12806ed21da7d55")
    version("4.16.0", sha256="1975b00eed9a8aa1f899eab2efaea593731c19138b83fdff2f13bdca5275bacc")

    variant("introspection", default=True, description="Build with gobject-introspection support")

    # Base requirements
    with default_args(type=("build", "run")):
        depends_on("libxfce4util")
        depends_on("libxfce4ui")
        depends_on("glib@2:")
        depends_on("gtkplus@3:")
        depends_on("perl-uri")
    with when("+introspection"):
        depends_on("libxfce4util+introspection")
        depends_on("libxfce4ui+introspection")
        depends_on("gobject-introspection")
    with default_args(type="build"):
        depends_on("intltool@0.51.0:", when="@:4.18")
        depends_on("gettext", when="@4.20:")
    with default_args(type=("build", "link", "run")):
        with when("@4.20.0:"):
            depends_on("glib@2.72:")
            depends_on("gobject-introspection@1.72:", when="+introspection")
        with when("@4.18.0:"):
            depends_on("glib@2.66:")
            depends_on("gtkplus@3.24:")
            depends_on("gobject-introspection@1.66:", when="+introspection")
        with when("@4.16.0:"):
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")
            depends_on("gobject-introspection@1.60:", when="+introspection")

    def configure_args(self):
        args = []
        args += self.enable_or_disable("introspection")
        return args
