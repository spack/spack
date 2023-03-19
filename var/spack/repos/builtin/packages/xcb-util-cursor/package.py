# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbUtilCursor(AutotoolsPackage):
    """The XCB util modules provides a number of libraries which sit on top
    of libxcb, the core X protocol library, and some of the extension
    libraries. These experimental libraries provide convenience functions
    and interfaces which make the raw X protocol more usable. Some of the
    libraries also provide client-side code which is not strictly part of
    the X protocol but which have traditionally been provided by Xlib."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxcb-cursor"
    url = "https://xorg.freedesktop.org/archive/individual/lib/xcb-util-cursor-0.1.4.tar.xz"

    version("0.1.4", sha256="28dcfe90bcab7b3561abe0dd58eb6832aa9cc77cfe42fcdfa4ebe20d605231fb")
    version("0.1.3", sha256="a322332716a384c94d3cbf98f2d8fe2ce63c2fe7e2b26664b6cea1d411723df8")

    depends_on("libxcb@1.4:")
    depends_on("xcb-util-renderutil")
    depends_on("xcb-util-image")

    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    def url_for_version(self, version):
        if version >= Version("0.1.4"):
            url = "https://xorg.freedesktop.org/archive/individual/lib/xcb-util-cursor-{0}.tar.xz"
        else:
            url = "https://xcb.freedesktop.org/dist/xcb-util-cursor-{0}.tar.gz"

        return url.format(version)
