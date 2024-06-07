# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxfce4ui(AutotoolsPackage):
    """Widget sharing library for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/libxfce4ui/start"
    url = "https://archive.xfce.org/xfce/4.16/src/libxfce4ui-4.16.0.tar.bz2"

    maintainers("teaguesterling")

    license("LGPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.16.0", sha256="8b06c9e94f4be88a9d87c47592411b6cbc32073e7af9cbd64c7b2924ec90ceaa")

    variant("glibtop", default=True, description="Build with glibtop support")
    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("vala", default=True, description="Build with vala support")

    with default_args(type=("build", "link", "run")):
        depends_on("libgtop", when="+glibtop")
        depends_on("gobject-introspection", when="+introspection")
        depends_on("vala", when="+vala")

        depends_on("libxfce4util+glibtop", when="+glibtop")
        depends_on("libxfce4util+introspection", when="+introspection")
        depends_on("libxfce4util+vala", when="+vala")

    with when("@4.16"):
        depends_on("intltool@0.35.0:", type="build")
        with default_args(type=("build", "link", "run")):
            depends_on("libxfce4util@4.16")
            depends_on("xfconf@4.16")

            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")
            depends_on("libgtop@2", when="+glibtop")
            depends_on("gobject-introspection@1.60:", when="+introspection")

    def configure_args(self):
        args = []

        args += self.enable_or_disable("glibtop")
        args += self.enable_or_disable("introspection")
        args += self.enable_or_disable("vala")

        return args

    def setup_dependent_build_environment(self, env, dep_spec):
        if self.spec.satisfies("+introspection") and dep_spec.satisfies("+introspection"):
            env.append_path("XDG_DATA_DIRS", self.prefix.share)
