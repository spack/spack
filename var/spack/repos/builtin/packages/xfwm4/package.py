# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xfwm4(AutotoolsPackage):
    """xfwm4 is the window manager for Xfce"""

    homepage = "https://docs.xfce.org/xfce/xfwm4/start"
    url = "https://archive.xfce.org/xfce/4.16/src/xfwm4-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    license("GPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    maintainers("teaguesterling")

    version("4.20.0", sha256="a58b63e49397aa0d8d1dcf0636be93c8bb5926779aef5165e0852890190dcf06")
    version("4.18.0", sha256="92cd1b889bb25cb4bc06c1c6736c238d96e79c1e706b9f77fad0a89d6e5fc13f")
    version("4.16.0", sha256="1e22eae1bbb66cebfd1753b0a5606e76ecbf6b09ce4cdfd732d093c936f1feb3")

    variant("notification", default=True, description="Build with startup-notification support")

    # Base requirements
    with default_args(type="build"):
        depends_on("intltool@0.35.0:", when="@:4.18")
        depends_on("gettext", when="@4.20:")
    with default_args(type=("build", "link", "run")):
        depends_on("libxfce4util")
        depends_on("xfconf")
        depends_on("libxfce4ui")
        depends_on("dbus-glib")
        depends_on("libwnck")
        depends_on("libxinerama")  # Undocumented
        depends_on("glib@2:")
        depends_on("gtkplus@3:")
        depends_on("startup-notification", when="+notification")
        with when("@4.18.0:"):
            depends_on("glib@2.72:")
        with when("@4.18.0:"):
            depends_on("glib@2.66:")
            depends_on("gtkplus@3.24:")
        with when("@4.16.0:"):
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")
