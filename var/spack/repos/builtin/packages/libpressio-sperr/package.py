# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioSperr(CMakePackage):
    """A LibPressio plugin for Sperr"""

    homepage = "https://github.com/robertu94"
    url = "https://github.com/robertu94/libpressio-sperr/archive/refs/tags/0.0.1.tar.gz"
    git = url

    maintainers = ["robertu94"]

    depends_on("libpressio")
    depends_on("sperr")
    depends_on("pkgconfig", type="build")

    version("master", branch="master")
    version("0.0.2", sha256="61995d687f9e7e798e17ec7238d19d917890dc0ff5dec18293b840c4d6f8c115")
    version("0.0.1", sha256="e2c164822708624b97654046b42abff704594cba6537d6d0646d485bdf2d03ca")
