# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gtkplus(MesonPackage):
    """The GTK+ package contains libraries used for creating graphical user
    interfaces for applications."""

    homepage = "https://www.gtk.org/"
    url = "https://download.gnome.org/sources/gtk+/3.24/gtk+-3.24.26.tar.xz"

    version("3.24.29", sha256="f57ec4ade8f15cab0c23a80dcaee85b876e70a8823d9105f067ce335a8268caa")
    version("3.24.26", sha256="2cc1b2dc5cad15d25b6abd115c55ffd8331e8d4677745dd3ce6db725b4fff1e9")
    version(
        "3.20.10",
        sha256="e81da1af1c5c1fee87ba439770e17272fa5c06e64572939814da406859e56b70",
        deprecated=True,
    )
    version(
        "2.24.32",
        sha256="b6c8a93ddda5eabe3bfee1eb39636c9a03d2a56c7b62828b359bf197943c582e",
        deprecated=True,
    )
    version(
        "2.24.31",
        sha256="68c1922732c7efc08df4656a5366dcc3afdc8791513400dac276009b40954658",
        deprecated=True,
    )
    version(
        "2.24.25",
        sha256="38af1020cb8ff3d10dda2c8807f11e92af9d2fa4045de61c62eedb7fbc7ea5b3",
        deprecated=True,
    )

    variant("cups", default=False, description="enable cups support")

    # See meson.build for version requirements
    depends_on("meson@0.48.0:", when="@3.24:", type="build")
    depends_on("ninja", when="@3.24:", type="build")
    # Needed to build man pages:
    # depends_on('docbook-xml', when='@3.24:', type='build')
    # depends_on('docbook-xsl', when='@3.24:', type='build')
    # depends_on('libxslt', when='@3.24:', type='build')
    depends_on("pkgconfig", type="build")
    depends_on("glib@2.57.2:")
    depends_on("pango@1.41.0:+X")
    depends_on("fribidi@0.19.7:")
    depends_on("atk@2.35.1:")
    depends_on("at-spi2-atk@2.15.1:", when="@3:")
    depends_on("cairo@1.14.0:+X+pdf+gobject")
    depends_on("gdk-pixbuf@2.30.0:")
    depends_on("gobject-introspection@1.39.0:")
    depends_on("shared-mime-info")
    depends_on("libxkbcommon")
    depends_on("librsvg")
    depends_on("xrandr")
    depends_on("libepoxy+glx", when="@3:")
    depends_on("libxi", when="@3:")
    depends_on("inputproto", when="@3:")
    depends_on("fixesproto", when="@3:")
    depends_on("gettext", when="@3:")
    depends_on("cups", when="+cups")

    patch("no-demos.patch", when="@2.0:2")

    def url_for_version(self, version):
        url = "https://download.gnome.org/sources/gtk+/{0}/gtk+-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def patch(self):
        # remove disable deprecated flag.
        filter_file(
            r'CFLAGS="-DGDK_PIXBUF_DISABLE_DEPRECATED $CFLAGS"', "", "configure", string=True
        )

        # https://gitlab.gnome.org/GNOME/gtk/-/issues/3776
        if self.spec.satisfies("@3:%gcc@11:"):
            filter_file("    '-Werror=array-bounds',", "", "meson.build", string=True)

    def setup_run_environment(self, env):
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def meson_args(self):
        args = std_meson_args

        if self.spec.satisfies("platform=darwin"):
            args.extend(["-Dx11_backend=false", "-Dquartz_backend=true"])

        args.extend(
            ["-Dgtk_doc=false", "-Dman=false", "-Dintrospection=true", "-Dwayland_backend=false"]
        )

        return args

    def configure_args(self):
        true = which("true")
        args = [
            "--prefix={0}".format(self.prefix),
            # disable building of gtk-doc files following #9771
            "--disable-gtk-doc-html",
            "GTKDOC_CHECK={0}".format(true),
            "GTKDOC_CHECK_PATH={0}".format(true),
            "GTKDOC_MKPDF={0}".format(true),
            "GTKDOC_REBASE={0}".format(true),
        ]
        if "~cups" in self.spec:
            args.append("--disable-cups")
        return args

    @when("@:3.20.10")
    def meson(self, spec, prefix):
        configure(*self.configure_args())

    @when("@:3.20.10")
    def build(self, spec, prefix):
        make()

    @when("@:3.20.10")
    def install(self, spec, prefix):
        make("install")

    def check(self):
        """All build time checks open windows in the X server, don't do that"""
        pass
