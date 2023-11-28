# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack.package import *


class MesaDemos(AutotoolsPackage):
    """This package provides some demo applications for testing Mesa."""

    homepage = "https://www.mesa3d.org"
    url = "https://gitlab.freedesktop.org/mesa/demos/-/archive/mesa-demos-8.4.0/demos-mesa-demos-8.4.0.tar.gz"

    version("8.4.0", sha256="e9d235e6dad69d6b00877bf07e6d1859e368c0873e5401ec68a6ddb43375e900")
    version("8.3.0", sha256="9bc1b37f4fc7bfc3f818f2d3851ffde28e8167ef11dca87f4781e9ef6206901f")
    version("8.2.0", sha256="5a9f71b815d968d0c3b77edfcc3782d0211f8520b00da9e554ccfed80c8889f6")
    version("8.1.0", sha256="cc5826105355830208c90047fc38c5b09fa3ab0045366e7e859104935b00b76d")

    variant(
        "gl",
        default="glx" if sys.platform.startswith("linux") else "osmesa",
        values=("glx", "osmesa", "other"),
        multi=False,
        description="The OpenGL provider to use",
    )
    conflicts("^osmesa", when="gl=glx")
    conflicts("^osmesa", when="gl=other")
    conflicts("^glx", when="gl=osmesa")
    conflicts("^glx", when="gl=other")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("gl")
    depends_on("osmesa", when="gl=osmesa")
    depends_on("glx", when="gl=glx")
    depends_on("libx11", when="gl=glx")
    depends_on("libxext", when="gl=glx")

    depends_on("glu")
    depends_on("glew@1.5.4:")

    # OSMesa demos don't actually use glut
    patch("osmesa-glut.patch")

    def configure_args(self):
        spec = self.spec
        args = [
            "--disable-egl",
            "--disable-gles1",
            "--disable-gles2",
            "--disable-vg",
            "--disable-libdrm",
            "--disable-wayland",
            "--disable-gbm",
            "--disable-freetype2",
            "--disable-rbug",
            "--without-glut",
        ]
        if "gl=glx" in spec:
            args.append("--enable-x11")
        else:
            args.append("--disable-x11")
        if "gl=osmesa" in spec:
            args.append("--enable-osmesa")
        else:
            args.append("--disable-osmesa")

        return args
