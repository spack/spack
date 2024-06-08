# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Exo(AutotoolsPackage):
    """Helper applications for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/exo/start"
    url = "https://archive.xfce.org/xfce/4.16/src/exo-4.16.0.tar.bz2"

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.16.0", sha256="1975b00eed9a8aa1f899eab2efaea593731c19138b83fdff2f13bdca5275bacc")
    version("0.12.7", sha256="78d10943b52eb50ce76224ae27c025fb174d39895b31723db90a869d6eeaf1da")

    variant("xfce4", default=True, description="Match XFCE4 versions")
    variant("introspection", default=True, description="Build with gobject-introspection support")

    # Base requirements
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4util")
        depends_on("libxfce4ui")
        depends_on("glib@2:")
        depends_on("gtkplus@3:")
        depends_on("perl-uri")

    depends_on("libxfce4util+introspection", when="+introspection")
    depends_on("libxfce4ui+introspection", when="+introspection")
    depends_on("gobject-introspection", when="+introspection")

    depends_on("intltool@0.51.0:", type="build")

    depends_on("libxfce4util+xfce4@4.16", when="+xfce4")
    depends_on("libxfce4ui+xfce4@4.16", when="+xfce4")
    with when("@0.12.7:"):
        with default_args(type=("build", "link", "run")):
            depends_on("libxfce4util@4.16:")
            depends_on("libxfce4ui@4.16:")
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")

            depends_on("gobject-introspection@1.60:", when="+introspection")

    def configure_args(self):
        args = []
        args += self.enable_or_disable("introspection")
        return args
