# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.autotools
import spack.build_systems.meson
from spack.package import *


class Harfbuzz(MesonPackage, AutotoolsPackage):
    """The Harfbuzz package contains an OpenType text shaping engine."""

    homepage = "https://github.com/harfbuzz/harfbuzz"
    url = "https://github.com/harfbuzz/harfbuzz/releases/download/2.9.1/harfbuzz-2.9.1.tar.xz"
    git = "https://github.com/harfbuzz/harfbuzz.git"

    build_system(
        conditional("autotools", when="@:2.9"), conditional("meson", when="@3:"), default="meson"
    )

    version("7.3.0", sha256="20770789749ac9ba846df33983dbda22db836c70d9f5d050cb9aa5347094a8fb")
    version("7.2.0", sha256="fc5560c807eae0efd5f95b5aa4c65800c7a8eed6642008a6b1e7e3ffff7873cc")
    version("6.0.0", sha256="1d1010a1751d076d5291e433c138502a794d679a7498d1268ee21e2d4a140eb4")
    version("5.3.1", sha256="4a6ce097b75a8121facc4ba83b5b083bfec657f45b003cd5a3424f2ae6b4434d")
    version("5.1.0", sha256="2edb95db668781aaa8d60959d21be2ff80085f31b12053cdd660d9a50ce84f05")
    version("4.2.1", sha256="bd17916513829aeff961359a5ccebba6de2f4bf37a91faee3ac29c120e3d7ee1")
    version("4.1.0", sha256="f7984ff4241d4d135f318a93aa902d910a170a8265b7eaf93b5d9a504eed40c8")
    version("4.0.1", sha256="98f68777272db6cd7a3d5152bac75083cd52a26176d87bc04c8b3929d33bce49")
    version("3.4.0", sha256="7158a87c4db82521fc506711f0c8864115f0292d95f7136c8812c11811cdf952")
    version("3.3.2", sha256="1c13bca136c4f66658059853e2c1253f34c88f4b5c5aba6050aba7b5e0ce2503")
    version("3.2.0", sha256="0ada50a1c199bb6f70843ab893c55867743a443b84d087d54df08ad883ebc2cd")
    version("3.1.2", sha256="4056b1541dd8bbd8ec29207fe30e568805c0705515632d7fec53a94399bc7945")
    version(
        "2.9.1",
        sha256="0edcc980f526a338452180e701d6aba6323aef457b6686976a7d17ccbddc51cf",
        deprecated=True,
    )
    version(
        "2.6.8",
        sha256="6648a571a27f186e47094121f0095e1b809e918b3037c630c7f38ffad86e3035",
        deprecated=True,
    )
    version(
        "2.3.1",
        sha256="f205699d5b91374008d6f8e36c59e419ae2d9a7bb8c5d9f34041b9a5abcae468",
        deprecated=True,
    )
    version(
        "2.1.3",
        sha256="613264460bb6814c3894e3953225c5357402915853a652d40b4230ce5faf0bee",
        deprecated=True,
    )
    version(
        "1.9.0",
        sha256="11eca62bf0ac549b8d6be55f4e130946399939cdfe7a562fdaee711190248b00",
        deprecated=True,
    )
    version(
        "1.4.6",
        sha256="21a78b81cd20cbffdb04b59ac7edfb410e42141869f637ae1d6778e74928d293",
        deprecated=True,
    )
    version(
        "0.9.37",
        sha256="255f3b3842dead16863d1d0c216643d97b80bfa087aaa8fc5926da24ac120207",
        deprecated=True,
    )

    variant("graphite2", default=False, description="enable support for graphite2 font engine")
    variant(
        "coretext",
        default=False,
        when="platform=darwin",
        description="Enable CoreText shaper backend on macOS",
    )

    depends_on("pkgconfig", type="build")
    depends_on("glib")
    depends_on("gobject-introspection")
    depends_on("icu4c")
    depends_on("freetype")
    depends_on("cairo+pdf+ft")
    depends_on("zlib-api")
    depends_on("graphite2", when="+graphite2")

    conflicts(
        "%intel", when="@2.3.1:", msg="harfbuzz-2.3.1 does not build with the Intel compiler"
    )

    def url_for_version(self, version):
        if version > Version("2.3.1"):
            url = "https://github.com/harfbuzz/harfbuzz/releases/download/{0}/harfbuzz-{0}.tar.xz"
        else:
            url = "http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-{0}.tar.bz2"

        return url.format(version)

    # Function borrowed from superlu
    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == "cxxflags":
            flags.append(self.compiler.cxx11_flag)
        if name == "cflags":
            if "%pgi" not in self.spec and self.spec.satisfies("%gcc@:5.1"):
                flags.append("-std=gnu99")
        return (None, None, flags)

    def setup_run_environment(self, env):
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def patch(self):
        change_sed_delimiter("@", ";", "src/Makefile.in")


class SetupEnvironment:
    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))


class MesonBuilder(spack.build_systems.meson.MesonBuilder, SetupEnvironment):
    def meson_args(self):
        graphite2 = "enabled" if self.pkg.spec.satisfies("+graphite2") else "disabled"
        coretext = "enabled" if self.pkg.spec.satisfies("+coretext") else "disabled"
        return [
            # disable building of gtk-doc files following #9885 and #9771
            "-Ddocs=disabled",
            "-Dgraphite2={0}".format(graphite2),
            "-Dcoretext={0}".format(coretext),
        ]


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder, SetupEnvironment):
    def configure_args(self):
        args = []

        # disable building of gtk-doc files following #9771
        args.append("--disable-gtk-doc-html")
        true = which("true")
        args.append("GTKDOC_CHECK={0}".format(true))
        args.append("GTKDOC_CHECK_PATH={0}".format(true))
        args.append("GTKDOC_MKPDF={0}".format(true))
        args.append("GTKDOC_REBASE={0}".format(true))
        args.extend(self.with_or_without("graphite2"))
        args.extend(self.with_or_without("coretext"))

        return args
