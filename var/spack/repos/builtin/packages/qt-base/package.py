# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys

from spack.operating_systems.mac_os import macos_version
from spack.package import *

MACOS_VERSION = macos_version() if sys.platform == "darwin" else None


class QtBase(CMakePackage):
    """Qt Base (Core, Gui, Widgets, Network, ...)"""

    homepage = "https://www.qt.io"
    url = "https://github.com/qt/qtbase/archive/refs/tags/v6.3.1.tar.gz"
    list_url = "https://github.com/qt/qtbase/tags"

    maintainers = ["wdconinc", "sethrj"]

    version("6.4.1", sha256="0ef6db6b3e1074e03dcae7e689144af66fd51b95a6efe949d40281cc43e6fecf")
    version("6.4.0", sha256="fbc462816bf5b87d521e9f69cebe0ce331de2258396e0932fa580283f07fce0c")
    version("6.3.2", sha256="95b78830a99f417ff34ee784ab78f5eeb7bb12adb16d137c3026434c44a904dd")
    version("6.3.1", sha256="4393e8cea0c58b1e0e901735fcffad141261576a0fa414ed6309910ac3d49df9")
    version("6.3.0", sha256="c50dc73f633e6c0f6ee3f51980c698800f1a0cadb423679bcef18e446ac72138")
    version("6.2.4", sha256="657d1405b5e15afcf322cc75b881f62d6a56f16383707742a99eb87f53cb63de")
    version("6.2.3", sha256="2dd095fa82bff9e0feb7a9004c1b2fb910f79ecc6111aa64637c95a02b7a8abb")

    variant("dbus", default=False, description="Build with D-Bus support.")
    variant(
        "framework", default=bool(MACOS_VERSION), description="Build as a macOS Framework package."
    )
    variant("gui", default=True, description="Build the Qt GUI module and dependencies.")
    variant("shared", default=True, description="Build shared libraries.")
    variant("sql", default=True, description="Build with SQL support.")
    variant("network", default=False, description="Build with SSL support.")

    # GUI-only dependencies
    variant(
        "accessibility", default=True, when="+gui", description="Build with accessibility support."
    )
    variant("gtk", default=False, when="+gui", description="Build with gtkplus.")
    variant("opengl", default=False, when="+gui", description="Build with OpenGL support.")
    variant("widgets", default=True, when="+gui", description="Build with widgets.")

    generator = "Ninja"

    depends_on("cmake@3.16:", type="build")
    depends_on("ninja", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python", type="build")

    # Dependencies, then variant- and version-specific dependencies
    depends_on("double-conversion")
    depends_on("icu4c")
    depends_on("libxml2")
    depends_on("pcre2+multibyte")
    depends_on("zlib")
    depends_on("zstd")
    with when("platform=linux"):
        depends_on("libdrm")

    depends_on("at-spi2-core", when="+accessibility")
    depends_on("dbus", when="+dbus")
    depends_on("gl", when="+opengl")
    depends_on("sqlite", when="+sql")

    with when("+gui"):
        depends_on("fontconfig")
        depends_on("freetype")
        depends_on("harfbuzz")
        depends_on("jpeg")
        depends_on("libpng")
        with when("platform=linux"):
            depends_on("libxkbcommon")
            depends_on("libxcb@1.13:")  # requires xinput
            depends_on("libxrender")

    with when("+network"):
        depends_on("libproxy")
        depends_on("openssl")

    # Qt6 requires newer compilers: see https://github.com/spack/spack/issues/34418
    conflicts("%gcc@:7")

    @property
    def archive_files(self):
        """Save both the CMakeCache and the config summary."""
        return [
            join_path(self.build_directory, filename)
            for filename in ["CMakeCache.txt", "config.summary"]
        ]

    def patch(self):
        vendor_dir = join_path(self.stage.source_path, "src", "3rdparty")
        vendor_deps_to_keep = [
            "blake2",
            "easing",
            "forkfd",
            "freebsd",
            "icc",
            "libpsl",
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
        spec = self.spec
        args = []

        def define(cmake_var, value):
            args.append(self.define(cmake_var, value))

        def define_from_variant(cmake_var, variant=None):
            result = self.define_from_variant(cmake_var, variant)
            if result:
                # Not a conditional variant
                args.append(result)

        def define_feature(key, variant=None):
            if variant is None:
                variant = key
            define_from_variant("FEATURE_" + key, variant)

        define_from_variant("BUILD_SHARED_LIBS", "shared")
        define("FEATURE_optimize_size", spec.satisfies("build_type=MinSizeRel"))

        # Top-level features
        define_feature("accessibility")
        # concurrent: default to on
        define_feature("dbus")
        define_feature("framework")
        define_feature("gui")
        define_feature("network")  # note: private feature
        # testlib: default to on
        # thread: default to on
        define_feature("widgets")  # note: private feature
        define_feature("sql")  # note: private feature
        # xml: default to on

        # Extra FEATURE_ toggles
        features = []
        if "+dbus" in spec:
            features.append("dbus_linked")
        if "+network" in spec:
            features += ["openssl_linked", "openssl", "libproxy"]
        for k in features:
            define("FEATURE_" + k, True)

        # INPUT_* arguments: undefined/no/qt/system
        sys_inputs = ["doubleconversion"]
        if "+sql" in spec:
            sys_inputs.append("sqlite")
        for k in sys_inputs:
            define("INPUT_" + k, "system")

        # FEATURE_system_* arguments: on/off
        sys_features = [
            ("doubleconversion", True),
            ("pcre2", True),
            ("zlib", True),
            ("libb2", False),
        ]
        if "+gui" in spec:
            sys_features += [
                ("jpeg", True),
                ("png", True),
                ("sqlite", True),
                ("freetype", True),
                ("harfbuzz", True),
                ("textmarkdownreader", False),
            ]
            with when("platform=linux"):
                sys_features += [
                    ("xcb_xinput", True),
                ]
        if "+network" in spec:
            sys_features += [
                ("proxies", True),
            ]
        for k, v in sys_features:
            define("FEATURE_system_" + k, v)

        return args
