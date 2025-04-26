# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfce4Core(BundlePackage):
    """Core libraries and applications for the Xfce4 desktop environment"""

    homepage = "https://docs.xfce.org/start"

    maintainers("teaguesterling")

    version("4.20")
    version("4.18")
    version("4.16")

    has_code = False

    for xfce4_version, new_components, override in [
        ("4.20", ["libxfce4windowing"], {}),
        ("4.18", [], {}),
        ("4.16", [], {"garcon": "0.8.0"}),
    ]:
        with when(f"@{xfce4_version}"):
            for component in [
                "libxfce4util",
                "xfconf",
                "libxfce4ui",
                "garcon",
                "exo",
                "thunar",
                "xfce4-session",
                "xfce4-panel",
                "xfce4-settings",
                "xfdesktop",
                "xfwm4",
                "xfce4-appfinder",
                "tumbler",
            ] + new_components:
                depends_on(f"{component}@{override.get(component, xfce4_version)}")
