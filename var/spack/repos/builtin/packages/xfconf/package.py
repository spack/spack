# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xfconf(AutotoolsPackage):
    """xfconf - Configuration Storage System for XFCE4"""

    homepage = "https://docs.xfce.org/xfce/xfconf/start"
    url = "https://archive.xfce.org/xfce/4.16/src/xfconf-4.16.0.tar.bz2"

    maintainers("teaguesterling")

    license("LGPLv2.1", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.16.0", sha256="652a119007c67d9ba6c0bc7a740c923d33f32d03dc76dfc7ba682584e72a5425")
    variant("xfce4", default=True, description="Match XFCE4 versions")

    depends_on("intltool@0.35.0:", type="build")
    depends_on("libxfce4util+xfce4@4.16", when="+xfce4@4.16")

    with when("@4.16"):

        with default_args(type=("build", "link", "run")):
            depends_on("libxfce4util@4.16:")
            depends_on("glib@2.50:")

