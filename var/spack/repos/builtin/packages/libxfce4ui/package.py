# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxfce4ui(AutotoolsPackage):
    """Widget sharing library for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/libxfce4ui/start"
    url = "https://archive.xfce.org/xfce/4.16/src/libxfce4ui-4.16.0.tar.bz2"

    maintainers("teaguesterling")

    license("LGPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.16.0", sha256="8b06c9e94f4be88a9d87c47592411b6cbc32073e7af9cbd64c7b2924ec90ceaa")

    with when("@4.16"):
        depends_on("intltool@0.35.0:", type="build")
        with default_args(type=("build", "link", "run")):
            depends_on("libxfce4util@4.16")
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")
            depends_on("libgtop@2")

