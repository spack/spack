# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cairo(MesonPackage, AutotoolsPackage):
    """Cairo is a 2D graphics library with support for multiple output
    devices."""

    homepage = "https://www.cairographics.org/"
    url = "https://www.cairographics.org/releases/cairo-1.16.0.tar.xz"
    git = "https://gitlab.freedesktop.org/cairo/cairo.git"

    license("LGPL-2.1-or-later OR MPL-1.1", checked_by="tgamblin")

    # Cairo has meson.build @1.17.4:, but we only support @1.17.8: here
    build_system(
        conditional("autotools", when="@:1.17.6"),
        conditional("meson", when="@1.17.8:"),
        default="meson",
    )

    version("1.18.0", sha256="243a0736b978a33dee29f9cca7521733b78a65b5418206fef7bd1c3d4cf10b64")
    # 1.17.8: https://gitlab.freedesktop.org/cairo/cairo/-/issues/646 (we enable tee by default)
    version(
        "1.17.6",
        sha256="4eebc4c2bad0402bc3f501db184417094657d111fb6c06f076a82ea191fe1faf",
        url="https://cairographics.org/snapshots/cairo-1.17.6.tar.xz",
    )
    version(
        "1.17.4",
        sha256="74b24c1ed436bbe87499179a3b27c43f4143b8676d8ad237a6fa787401959705",
        url="https://cairographics.org/snapshots/cairo-1.17.4.tar.xz",
    )
    version(
        "1.17.2",
        sha256="6b70d4655e2a47a22b101c666f4b29ba746eda4aa8a0f7255b32b2e9408801df",
        url="https://cairographics.org/snapshots/cairo-1.17.2.tar.xz",
    )
    version("1.16.0", sha256="5e7b29b3f113ef870d1e3ecf8adf21f923396401604bda16d44be45e66052331")
    version("1.14.12", sha256="8c90f00c500b2299c0a323dd9beead2a00353752b2092ead558139bd67f7bf16")
    version("1.14.8", sha256="d1f2d98ae9a4111564f6de4e013d639cf77155baf2556582295a0f00a9bc5e20")
    version("1.14.0", sha256="2cf5f81432e77ea4359af9dcd0f4faf37d015934501391c311bfd2d19a0134b7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("X", default=False, description="Build with X11 support")
    variant("pdf", default=False, description="Enable cairo's PDF surface backend feature")
    variant("gobject", default=False, description="Enable cairo's gobject functions feature")
    variant("ft", default=False, description="Enable cairo's FreeType font backend feature")
    variant("fc", default=False, description="Enable cairo's Fontconfig font backend feature")
    variant("png", default=False, description="Enable cairo's PNG functions feature")
    variant("svg", default=False, description="Enable cairo's SVG functions feature")
    variant("shared", default=True, description="Build shared libraries")
    variant("pic", default=True, description="Enable position-independent code (PIC)")

    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
        depends_on("m4", type="build")

    with when("build_system=meson"):
        depends_on("meson@0.59:")

    depends_on("libx11", when="+X")
    depends_on("libxext", when="+X")
    depends_on("libxrender", when="+X")
    depends_on("libxcb", when="+X")
    depends_on("python", when="+X", type="build")
    depends_on("libpng", when="+png")
    depends_on("glib")
    depends_on("pixman@0.36.0:", when="@1.17.2:")
    depends_on("pixman")
    depends_on("freetype build_system=autotools", when="+ft")
    # Require freetype with FT_Color
    # https://gitlab.freedesktop.org/cairo/cairo/-/issues/792
    depends_on("freetype@2.10:", when="@1.18.0: +ft")
    depends_on("pkgconfig", type="build")
    depends_on("fontconfig@2.10.91:", when="+fc")  # Require newer version of fontconfig.
    depends_on("which", type="build")
    depends_on("zlib", when="+pdf")
    # lzo is not strictly required, but cannot be disabled and may be pulled in accidentally
    # https://github.com/mesonbuild/meson/issues/8224
    # https://github.com/microsoft/vcpkg/pull/38313
    depends_on("lzo", when="@1.18: build_system=meson")

    conflicts("+png", when="platform=darwin")
    conflicts("+svg", when="platform=darwin")
    conflicts("+shared~pic")

    # patch from https://gitlab.freedesktop.org/cairo/cairo/issues/346
    patch("fontconfig.patch", when="@1.16.0:1.17.2")
    # Patch autogen.sh to not regenerate docs to avoid a dependency on gtk-doc
    patch("disable-gtk-docs.patch", when="build_system=autotools ^autoconf@2.70:")

    def check(self):
        """The checks are only for the cairo devs: They write others shouldn't bother"""
        pass


class MesonBuilder(spack.build_systems.meson.MesonBuilder):
    def meson_args(self):
        args = ["-Dtee=enabled"]

        if "+X" in self.spec:
            args.extend(["-Dxlib=enabled", "-Dxcb=enabled"])
        else:
            args.extend(["-Dxlib=disabled", "-Dxcb=disabled"])

        args.append("-Dzlib=" + ("enabled" if "+pdf" in self.spec else "disabled"))
        args.append(
            "-Dpng=" + ("enabled" if ("+png" in self.spec or "+svg" in self.spec) else "disabled")
        )
        args.append("-Dfreetype=" + ("enabled" if "+ft" in self.spec else "disabled"))
        args.append("-Dfontconfig=" + ("enabled" if "+fc" in self.spec else "disabled"))
        args.append("-Ddefault_library=" + ("shared" if "+shared" in self.spec else "static"))
        args.append("-Db_staticpic=" + ("true" if "+pic" in self.spec else "false"))

        return args


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def autoreconf(self, pkg, spec, prefix):
        # Regenerate, directing the script *not* to call configure before Spack
        # does
        which("sh")("./autogen.sh", extra_env={"NOCONFIGURE": "1"})

    def configure_args(self):
        args = ["--disable-trace", "--enable-tee"]  # can cause problems with libiberty

        if self.spec.satisfies("+X"):
            args.extend(["--enable-xlib", "--enable-xcb"])
        else:
            args.extend(["--disable-xlib", "--disable-xcb"])

        args.extend(self.enable_or_disable("pdf"))
        args.extend(self.enable_or_disable("gobject"))
        args.extend(self.enable_or_disable("ft"))
        args.extend(self.enable_or_disable("fc"))
        args.extend(self.enable_or_disable("shared"))
        args.extend(self.with_or_without("pic"))

        if self.spec.satisfies("+ft ^freetype~shared"):
            pkgconf = which("pkg-config")
            ldflags = pkgconf("--libs-only-L", "--static", "freetype2", output=str)
            libs = pkgconf("--libs-only-l", "--static", "freetype2", output=str)
            args.append(f"LDFLAGS={ldflags}")
            args.append(f"LIBS={libs}")

        return args
