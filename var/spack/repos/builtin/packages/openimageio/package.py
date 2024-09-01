# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openimageio(CMakePackage):
    """Reading, writing, and processing images in a wide variety of file formats, using
    a format-agnostic API, aimed at VFX applications."""

    homepage = "https://openimageio.readthedocs.io"
    git = "https://github.com/AcademySoftwareFoundation/OpenImageIO"
    url = "https://github.com/AcademySoftwareFoundation/OpenImageIO/archive/refs/tags/v2.5.14.0.tar.gz"

    license("Apache-2.0")

    version("2.5.14.0", sha256="0e74372c658f083820872311d126867f10d59b526a856672746de7b2c772034d")
    version("2.2.7.0", sha256="6126fb8b1a8be0106c78056652a249791e43b8741d6db3e9921a29ad823c1590")
    version("1.8.15", sha256="5cf57027597aeb3934c10739d3eeca9fb10a38606ad722da579772bab0e9cc5e")

    depends_on("cxx", type="build")  # generated

    # Core dependencies
    depends_on("cmake@3.2.2:", type="build")
    depends_on("boost+atomic+filesystem+thread@1.53:")
    depends_on("libtiff@4.0:")
    depends_on("openexr@2.3:2", when="@1")
    depends_on("openexr@3.1:", when="@2")
    depends_on("libpng@1.6:")

    # Optional dependencies
    variant("ffmpeg", default=False, description="Support video frames")
    depends_on("ffmpeg", when="+ffmpeg")

    variant("jpeg2k", default=False, description="Support for JPEG2000 format")
    depends_on("openjpeg", when="+jpeg2k")

    variant("python", default=False, description="Build python bindings")
    extends("python", when="+python")
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-pybind11", when="+python", type=("build", "run"))

    variant("qt", default=False, description="Build qt viewer")
    depends_on("qt@5.6.0:+opengl", when="+qt")

    conflicts("target=aarch64:", when="@:1.8.15")

    def url_for_version(self, version):
        if version >= Version('2'):
            return super().url_for_version(version)
        return f'https://github.com/AcademySoftwareFoundation/OpenImageIO/archive/refs/tags/Release-{version}.tar.gz'

    def cmake_args(self):
        args = ["-DUSE_FFMPEG={0}".format("ON" if "+ffmpeg" in self.spec else "OFF")]
        args += ["-DUSE_OPENJPEG={0}".format("ON" if "+jpeg2k" in self.spec else "OFF")]
        args += ["-DUSE_PYTHON={0}".format("ON" if "+python" in self.spec else "OFF")]
        args += ["-DUSE_QT={0}".format("ON" if "+qt" in self.spec else "OFF")]
        return args
