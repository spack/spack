# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxcb(AutotoolsPackage):
    """The X protocol C-language Binding (XCB) is a replacement
    for Xlib featuring a small footprint, latency hiding, direct
    access to the protocol, improved threading support, and
    extensibility."""

    homepage = "https://xcb.freedesktop.org/"
    url = "https://xorg.freedesktop.org/archive/individual/lib/libxcb-1.14.tar.xz"

    version("1.14", sha256="a55ed6db98d43469801262d81dc2572ed124edc3db31059d4e9916eb9f844c34")
    version("1.13", sha256="0bb3cfd46dbd90066bf4d7de3cad73ec1024c7325a4a0cbf5f4a0d4fa91155fb")

    depends_on("libpthread-stubs")
    depends_on("libxau@0.99.2:")
    depends_on("libxdmcp")

    # libxcb 1.X requires xcb-proto >= 1.X
    depends_on("xcb-proto")
    depends_on("xcb-proto@1.14:", when="@1.14")
    depends_on("xcb-proto@1.13:", when="@1.13")

    depends_on("python", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    def url_for_version(self, version):
        if version >= Version("1.14"):
            url = "https://xorg.freedesktop.org/archive/individual/lib/libxcb-{0}.tar.xz"
        else:
            url = "https://xcb.freedesktop.org/dist/libxcb-{0}.tar.gz"

        return url.format(version)

    def configure_args(self):
        config_args = []

        # -Werror flags are not properly interpreted by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc@:20.11"):
            config_args.append("--disable-selective-werror")

        return config_args

    def patch(self):
        filter_file("typedef struct xcb_auth_info_t {", "typedef struct {", "src/xcb.h")
