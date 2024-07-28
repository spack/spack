# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openslide(AutotoolsPackage, MesonPackage):
    """OpenSlide reads whole slide image files."""

    homepage = "https://openslide.org/"
    url = "https://github.com/openslide/openslide/releases/download/v3.4.1/openslide-3.4.1.tar.xz"

    license("LGPL-2.1-only")

    version("4.0.0", sha256="cc227c44316abb65fb28f1c967706eb7254f91dbfab31e9ae6a48db6cf4ae562")
    version("3.4.1", sha256="9938034dba7f48fadc90a2cdf8cfe94c5613b04098d1348a5ff19da95b990564")
    
    build_system(
        conditional("meson", when="@4:"), conditional("autotools", when="@3.4.1"), default="meson"
    )

    with when("build_system=meson"):
        depends_on("meson@0.53:", type="build")

    depends_on("c", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("cairo+pdf@1.2:")
    depends_on("cmake", when="@4:", type="build")
    depends_on("libdicom", when="@4:")
    depends_on("gdk-pixbuf")
    depends_on("glib@2.56:", when="@4:")
    depends_on("glib@2.16:", when="@3.4.1")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff@4.0:")
    depends_on("libxml2")
    depends_on("openjpeg@1,2.1:")
    depends_on("sqlite@3.14:", when="@4:")
    depends_on("sqlite@3.6:", when="@3.4.1")
    depends_on("zlib-api")
