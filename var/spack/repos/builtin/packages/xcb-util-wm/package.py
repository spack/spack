# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbUtilWm(AutotoolsPackage):
    """The XCB util modules provides a number of libraries which sit on top
    of libxcb, the core X protocol library, and some of the extension
    libraries. These experimental libraries provide convenience functions
    and interfaces which make the raw X protocol more usable. Some of the
    libraries also provide client-side code which is not strictly part of
    the X protocol but which have traditionally been provided by Xlib."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxcb-wm"
    url = "https://xorg.freedesktop.org/archive/individual/lib/xcb-util-wm-0.4.2.tar.xz"

    version("0.4.2", sha256="62c34e21d06264687faea7edbf63632c9f04d55e72114aa4a57bb95e4f888a0b")
    version("0.4.1", sha256="038b39c4bdc04a792d62d163ba7908f4bb3373057208c07110be73c1b04b8334")

    depends_on("m4", type="build")

    depends_on("libxcb@1.4:")

    depends_on("pkgconfig", type="build")

    def url_for_version(self, version):
        if version >= Version("0.4.2"):
            url = "https://xorg.freedesktop.org/archive/individual/lib/xcb-util-wm-{0}.tar.xz"
        else:
            url = "https://xcb.freedesktop.org/dist/xcb-util-wm-{0}.tar.gz"

        return url.format(version)
