# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbUtilErrors(AutotoolsPackage):
    """The XCB util modules provides a number of libraries which sit on top
    of libxcb, the core X protocol library, and some of the extension
    libraries. These experimental libraries provide convenience functions
    and interfaces which make the raw X protocol more usable. Some of the
    libraries also provide client-side code which is not strictly part of
    the X protocol but which have traditionally been provided by Xlib."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxcb-errors"
    url = "https://xorg.freedesktop.org/archive/individual/lib/xcb-util-errors-1.0.1.tar.xz"

    version("1.0.1", sha256="5628c87b984259ad927bacd8a42958319c36bdf4b065887803c9d820fb80f357")
    version("1.0", sha256="7752a722e580efdbada30632cb23aed35c18757399ac3b547b59fd7257cf5e33")

    depends_on("libxcb@1.4:")

    depends_on("xcb-proto")
    depends_on("pkgconfig", type="build")

    def url_for_version(self, version):
        if version >= Version("1.0.1"):
            url = "https://xorg.freedesktop.org/archive/individual/lib/xcb-util-errors-{0}.tar.xz"
        else:
            url = "https://xcb.freedesktop.org/dist/xcb-util-errors-{0}.tar.gz"

        return url.format(version)
