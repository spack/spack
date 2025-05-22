# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Virtualgl(CMakePackage):
    """VirtualGL redirects 3D commands from a Unix/Linux OpenGL application
    onto a server-side GPU and converts the rendered 3D images into a video
    stream with which remote clients can interact to view and control the
    3D application in real time."""

    homepage = "https://www.virtualgl.org/Main/HomePage"
    url = "https://github.com/VirtualGL/virtualgl/archive/refs/tags/3.1.2.tar.gz"

    license("LGPL-2.1-or-later")

    version("3.1.2", sha256="1e7f1e37e173af972ac34cdd207e856f613da44f474d19b85fe4795b0a16df38")
    version("2.5.2", sha256="e6105f579f25a77a4a190a80f9b239a9f70e007e5e9f4a5a69c9e7cce168d166")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # This package will only work with libjpeg-turbo, not other jpeg providers
    depends_on("libjpeg-turbo")
    depends_on("libxtst")
    depends_on("libxext")
    depends_on("libx11")
    depends_on("gl")
    depends_on("glu")
    depends_on("libxcb", when="@3:")
    depends_on("xcb-util-keysyms", when="@3:")
    depends_on("opencl-headers", when="@3:", type="build")
    depends_on("opencl-icd-loader", when="@3:")
    depends_on("egl", when="@3:")

    @when("@3:")
    def patch(self):
        with working_dir("server"):
            filter_file(
                r"string\(REGEX REPLACE.*XCB_XCB_LIB.*\)",
                f"set(XCB_XCB_LIB {join_path(self.spec['libxcb'].prefix.lib, 'libxcb.so')})",
                "CMakeLists.txt",
            )
            filter_file(
                r"string\(REGEX REPLACE.*XCB_GLX_LIB.*\)",
                f"set(XCB_GLX_LIB {join_path(self.spec['libxcb'].prefix.lib, 'libxcb-glx.so')})",
                "CMakeLists.txt",
            )
