# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xfce4Session(AutotoolsPackage):
    """Session manager for Xfce4"""

    homepage = "https://docs.xfce.org/xfce/xfce4-session/start"
    url = "https://archive.xfce.org/xfce/4.16/src/xfce4-session-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.18.0", sha256="38badb500b272012f494543a60a9c0563c381647cc95bed73b68aec0b0b89a7f")
    version("4.16.0", sha256="22f273f212481d71e0b5618c62710cd85f69aea74f5ea5c0093f7918b07d17b7")

    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4ui")
        depends_on("libwnck@3.10:")
        depends_on("dbus-glib")
        depends_on("iceauth")
        depends_on("perl-xml-parser")

    depends_on("intltool@0.39.0:", type="build")
    with default_args(type=("build", "link", "run")):
        with when("@4.18.0:"):
            depends_on("glib@2.66:")
        with when("@4.16.0:"):
            depends_on("glib@2.50:")

    def configure_args(self):
        args = []
        args += [f"--with-xsession-prefix={self.home}"]
        return args
