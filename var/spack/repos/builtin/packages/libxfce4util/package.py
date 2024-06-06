# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libxfce4util(AutotoolsPackage):
    """Libxfce4util is used to share commonly used non-GTK+ utilities among the Xfce applications."""

    homepage = "https://docs.xfce.org/xfce/libxfce4util/start"
    url = "https://archive.xfce.org/xfce/4.16/src/libxfce4util-4.16.0.tar.bz2"

    maintainers("teaguesterling")

    license("LGPLv2", checked_by="teague")  # https://wiki.xfce.org/licenses/audit

    version("4.16.0", sha256="60598d745d1fc81ff5ad3cecc3a8d1b85990dd22023e7743f55abd87d8b55b83")

    depends_on("glib@2.50:")
