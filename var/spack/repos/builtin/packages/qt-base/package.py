# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class QtBase(CMakePackage):
    """Qt Base (Core, Gui, Widgets, Network, ...)"""

    homepage = "https://www.qt.io"
    url = "https://github.com/qt/qtbase/archive/refs/tags/v6.2.3.tar.gz"
    list_url = "https://github.com/qt/qtbase/tags"

    maintainers = ["wdconinc", "sethrj"]

    version("6.3.1", sha256="4393e8cea0c58b1e0e901735fcffad141261576a0fa414ed6309910ac3d49df9")
    version("6.3.0", sha256="c50dc73f633e6c0f6ee3f51980c698800f1a0cadb423679bcef18e446ac72138")
    version("6.2.4", sha256="657d1405b5e15afcf322cc75b881f62d6a56f16383707742a99eb87f53cb63de")
    version("6.2.3", sha256="2dd095fa82bff9e0feb7a9004c1b2fb910f79ecc6111aa64637c95a02b7a8abb")

    generator = "Ninja"

    # Changing default to Release for typical use in HPC contexts
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo", "MinSizeRel"),
        description="CMake build type",
    )

    variant("accessibility", default=True, description="Build with accessibility support.")
    variant("dbus", default=False, description="Build with D-Bus support.")
    variant("examples", default=False, description="Build examples.")
    variant("framework", default=False, description="Build as a macOS Framework package.")
    variant("gtk", default=False, description="Build with gtkplus.")
    variant("gui", default=True, description="Build the Qt GUI module and dependencies.")
    variant("opengl", default=False, description="Build with OpenGL support.", when="+gui")
    variant("shared", default=True, description="Build shared libraries.")
    variant("sql", default=True, description="Build with SQL support.")
    variant("ssl", default=True, description="Build with OpenSSL support.")
    variant("widgets", default=True, description="Build with widgets.")

    depends_on("cmake@3.16:", type="build")
    depends_on("ninja", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python", type="build")

    # Dependencies, then variant- and version-specific dependencies
    depends_on("at-spi2-core", when="+accessibility")
    depends_on("dbus", when="+dbus")
    depends_on("double-conversion")
    depends_on("fontconfig")
    depends_on("freetype")
    depends_on("gl", when="+opengl")
    depends_on("harfbuzz")
    depends_on("icu4c")
    depends_on("jpeg")
    depends_on("libdrm")
    depends_on("libjpeg")
    depends_on("libmng")
    depends_on("libproxy")
    depends_on("libtiff")
    depends_on("libxkbcommon")
    depends_on("libxml2")
    depends_on("libxrender")
    depends_on("openssl", when="+ssl")
    depends_on("pcre2+multibyte")
    depends_on("sqlite", when="+sql")
    depends_on("zlib")
    depends_on("zstd")

    def patch(self):
        import os
        import shutil

        vendor_dir = join_path(self.stage.source_path, "src", "3rdparty")
        vendor_deps_to_keep = [
            "blake2",
            "easing",
            "forkfd",
            "freebsd",
            "icc",
            "md4",
            "md4c",
            "md5",
            "rfc6234",
            "sha1",
            "sha3",
            "tinycbor",
            "VulkanMemoryAllocator",
        ]
        with working_dir(vendor_dir):
            for dep in os.listdir():
                if os.path.isdir(dep):
                    if dep not in vendor_deps_to_keep:
                        shutil.rmtree(dep)

    def cmake_args(self):
        def define_feature(variant):
            return self.define_from_variant("FEATURE_" + variant, variant)

        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("QT_BUILD_EXAMPLES", "examples"),
            self.define("QT_BUILD_TESTS", self.run_tests),
            self.define("FEATURE_optimize_size", self.spec.satisfies("build_type=MinSizeRel")),
            define_feature("accessibility"),
            define_feature("dbus"),
            define_feature("framework"),
            define_feature("gui"),
            define_feature("ssl"),
            define_feature("widgets"),
            define_feature("sql"),
        ]

        # INPUT_* arguments: link where possible
        for x in ["dbus", "openssl"]:
            args.append(self.define("INPUT_" + x, "linked"))
        # But use opengl
        args.append(self.define_from_variant("INPUT_opengl", "opengl"))

        # FEATURE_system_* arguments: use system where possible
        for x in [
            "doubleconversion",
            "freetype",
            "harfbuzz",
            "jpeg",
            "pcre2",
            "png",
            "proxies",
            "sqlite",
            "zlib",
        ]:
            args.append(self.define("FEATURE_system_" + x, True))
        # But use bundled libb2 and textmarkdownreader since not in spack
        args.append(self.define("FEATURE_system_libb2", False))
        args.append(self.define("FEATURE_system_textmarkdownreader", False))

        return args
