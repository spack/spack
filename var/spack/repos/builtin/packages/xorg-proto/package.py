# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.autotools
import spack.build_systems.meson
from spack.package import *


class XorgProto(MesonPackage, AutotoolsPackage, XorgPackage):
    """The X Window System Unified Protocol provides the headers and
    specification documents defining the core protocol the core protocol
    and (many) extensions for the X Window System. The extensions are
    those common among servers descended from X11R7. It also includes
    a number of headers that aren't purely protocol related, but are
    depended upon by many other X Window System packages to provide
    common definitions and porting layer."""

    homepage = "https://gitlab.freedesktop.org/xorg/proto/xorgproto"
    xorg_mirror_path = "proto/xorgproto-2022.2.tar.gz"

    maintainers("wdconinc")

    build_system("autotools", "meson", default="meson")

    version("2024.1", sha256="4f6b9b4faf91e5df8265b71843a91fc73dc895be6210c84117a996545df296ce")
    version("2023.2", sha256="c791aad9b5847781175388ebe2de85cb5f024f8dabf526d5d699c4f942660cc3")
    version("2023.1", sha256="c9225c6887b1cb16a762f2e14e7fb56328f53bc5d804e760dcddefc97cc52f35")
    version("2022.2", sha256="da351a403d07a7006d7bdc8dcfc14ddc1b588b38fb81adab9989a8eef605757b")
    version("2022.1", sha256="2a399e77d98fe53e9056726a1934b62cbaa6c41d7b1f41a354911b0925363343")
    version("2021.5", sha256="be6ddd6590881452fdfa170c1c9ff87209a98d36155332cbf2ccbc431add86ff")
    version("2021.4", sha256="9de0babd3d8cb16b0c1c47b8389a52f3e1326bb0bc9a9ab34a9500778448a2bd")
    version("2021.3", sha256="fa0a7d4ac45ebf0d6efd0b212dc41181ac61873d36c161e0df05d390cb1e16eb")
    version("2021.2", sha256="9c397baafd01f17152ca8ba0b502b21f21d91ce72a55843dd8c8357ffbc5680f")
    version("2020.1", sha256="6265b11b125df2f4853eec4895b14067d5621f813553fa077bebef20d7542418")
    version("2019.2", sha256="ebfcfce48b66bec25d5dff0e9510e04053ef78e51a8eabeeee4c00e399226d61")
    version("2019.1", sha256="38ad1d8316515785d53c5162b4b7022918e03c11d72a5bd9df0a176607f42bca")
    version("2018.4", sha256="8e48d851efea0e951bcb6cf0d537f84ba3803de95e488bd039fe59fc75ec8f7d")
    version("2018.3", sha256="f6e5a93e5c8b928089bc7057e3bbb2ef8f312639e7e4554fa38ee9655684ad4e")
    version("2018.2", sha256="2ea043125faad276e3529cff871e835929fe28f7e2009517ff1aae8f6fc84663")
    version("2018.1", sha256="a386126eee0cd91ccb09117144b5b207e9d067983abfd38210ae91e377c32c49")

    variant("legacy", default=False, description="Install legacy protocols")

    provides("applewmproto@1.4.2")
    provides("bigreqsproto@1.1.2")
    provides("compositeproto@0.4.2")
    provides("damageproto@1.2.1")
    provides("dmxproto@2.3.1")
    provides("dpmsproto@1.2", when="@2020.1:")
    provides("dri2proto@2.8")
    provides("dri3proto@1.3", when="@2022.2:")
    provides("fixesproto@6.0", when="@2021.4:")
    provides("fontsproto@2.1.3")
    provides("glproto@1.4.17")
    provides("inputproto@2.3.99.2", when="@2021.5:")
    provides("kbproto@1.0.7", when="@2018.2:")
    provides("presentproto@1.2", when="@2018.4:")
    provides("randrproto@1.6.0", when="@2018.3:")
    provides("recordproto@1.14.2")
    provides("renderproto@0.11.1")
    provides("resourceproto@1.2.0")
    provides("scrnsaverproto@1.2.3", when="@2019.1:")
    provides("videoproto@2.3.3")
    provides("windowswmproto@1.0.4")
    provides("xcmiscproto@1.2.2")
    provides("xextproto@7.3.0")
    provides("xf86bigfontproto@1.2.0")
    provides("xf86dgaproto@2.1")
    provides("xf86driproto@2.1.1")
    provides("xf86vidmodeproto@2.3.1")
    provides("xineramaproto@1.2.1")
    provides("xproto@7.0.33", when="@2021.2:")
    provides("xwaylandproto@1.0", when="@2022.1:")

    # Older versions
    provides("dri3proto@1.0", when="@2018.1:2018.3")
    provides("dri3proto@1.2", when="@2018.4:2022.1")
    provides("fixesproto@5.0", when="@2018.1:2021.3")
    provides("inputproto@2.3.2", when="@2018.1:2021.4")
    provides("kbproto@1.0.6", when="@2018.1")
    provides("presentproto@1.0", when="@2018.1")
    provides("presentproto@1.1", when="@2018.2:2018.3")
    provides("randrproto@1.5.0", when="@2018.1:2018.2")
    provides("scrnsaverproto@1.2.2", when="@2018.1:2018.4")
    provides("xproto@7.0.31", when="@2018.1")
    provides("xproto@7.0.32", when="@2018.2:2020.1")

    # Legacy protocols
    # - for all versions
    provides("evieproto@1.1.1", when="+legacy")
    provides("fontcacheproto@0.1.3", when="+legacy")
    provides("lg3dproto@5.0", when="+legacy")
    provides("printproto@1.0.5", when="+legacy")
    provides("xcalibrateproto@0.1.0", when="+legacy")
    provides("xf86rushproto@1.1.2", when="+legacy")
    # - turned into legacy
    provides("trapproto@3.4.3", when="@:2019")
    provides("trapproto@3.4.3", when="@2020.1: +legacy")
    provides("xf86miscproto@0.9.3", when="@:2019.2")
    provides("xf86miscproto@0.9.3", when="@2020.1: +legacy")
    provides("xproxymngproto@1.0.3", when="@:2019.2")
    provides("xproxymngproto@1.0.3", when="@2020.1: +legacy")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
        depends_on("m4", type="build")

    with when("build_system=meson"):
        depends_on("meson@0.56:")


class MesonBuilder(spack.build_systems.meson.MesonBuilder):
    def meson_args(self):
        return ["-Dlegacy=" + str(self.spec.satisfies("+legacy"))]


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        return self.enable_or_disable("legacy")
