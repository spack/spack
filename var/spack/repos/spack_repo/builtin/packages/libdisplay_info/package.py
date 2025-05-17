# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.meson import MesonPackage

from spack.package import *


class LibdisplayInfo(MesonPackage):
    """EDID and DisplayID library"""

    homepage = "https://emersion.pages.freedesktop.org/libdisplay-info/"
    url = "https://gitlab.freedesktop.org/emersion/libdisplay-info/-/archive/0.2.0/libdisplay-info-0.2.0.tar.bz2"

    maintainers("teaguesterling")

    license("MIT", checked_by="teaguesterling")

    version("0.2.0", sha256="f6cf2ddbba3753ae38de5113d1fcb8fab977dfaf5fb07b38cd68d8482765e208")

    depends_on("c", type="build")
    with default_args(type="build"):
        depends_on("hwdata@0.392:")
        depends_on("python")
