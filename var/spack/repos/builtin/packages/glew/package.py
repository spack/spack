# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Glew(CMakePackage):
    """The OpenGL Extension Wrangler Library."""

    homepage = "http://glew.sourceforge.net/"
    url = "https://github.com/nigels-com/glew/releases/download/glew-2.1.0/glew-2.1.0.tgz"
    root_cmakelists_dir = "build/cmake"

    version("2.2.0", sha256="d4fc82893cfb00109578d0a1a2337fb8ca335b3ceccf97b97e5cc7f08e4353e1")
    version("2.1.0", sha256="04de91e7e6763039bc11940095cd9c7f880baba82196a7765f727ac05a993c95")
    version("2.0.0", sha256="c572c30a4e64689c342ba1624130ac98936d7af90c3103f9ce12b8a0c5736764")

    variant(
        "gl",
        default="glx" if sys.platform.startswith("linux") else "other",
        values=("glx", "osmesa", "other"),
        multi=False,
        description="The OpenGL provider to use",
    )
    conflicts("osmesa", when="gl=glx")
    conflicts("osmesa", when="gl=other")
    conflicts("glx", when="gl=osmesa")
    conflicts("glx", when="gl=other")

    depends_on("gl")
    depends_on("osmesa", when="gl=osmesa")
    depends_on("glx", when="gl=glx")
    depends_on("libx11", when="gl=glx")
    depends_on("xproto", when="gl=glx")

    # glu is already forcibly disabled in the CMakeLists.txt.  This prevents
    # it from showing up in the .pc file
    patch("remove-pkgconfig-glu-dep.patch")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("BUILD_UTILS", True),
            self.define("GLEW_REGAL", False),
            self.define("GLEW_EGL", False),
            self.define("OpenGL_GL_PREFERENCE", "LEGACY"),
            self.define("OPENGL_INCLUDE_DIR", spec["gl"].headers.directories[0]),
            self.define("OPENGL_gl_LIBRARY", spec["gl"].libs[0]),
            self.define("OPENGL_opengl_LIBRARY", "IGNORE"),
            self.define("OPENGL_glx_LIBRARY", "IGNORE"),
            self.define("OPENGL_egl_LIBRARY", "IGNORE"),
            self.define("OPENGL_glu_LIBRARY", "IGNORE"),
            self.define("GLEW_OSMESA", "gl=osmesa" in spec),
            self.define("GLEW_X11", "gl=glx" in spec),
            self.define("CMAKE_DISABLE_FIND_PACKAGE_X11", "gl=glx" not in spec),
        ]

        return args
