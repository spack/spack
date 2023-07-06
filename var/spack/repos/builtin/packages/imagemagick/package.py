# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Imagemagick(AutotoolsPackage):
    """ImageMagick is a software suite to create, edit, compose,
    or convert bitmap images."""

    homepage = "https://www.imagemagick.org"
    url = "https://github.com/ImageMagick/ImageMagick/archive/7.0.2-7.tar.gz"

    version("7.1.1-11", sha256="98bb2783da7d5b06e7543529bd07b50d034fba611ff15e8817a0f4f73957d934")
    version("7.0.8-7", sha256="fadb36b59f310e9eee5249ecb2326b323a64da6cc716dd6d08ece8ea2c780b81")
    version("7.0.5-9", sha256="b85b269e0ed1628e88e840053823f8a33c314b2271f04762f43d33e9d0b4d264")
    version("7.0.2-7", sha256="f2f18a97f861c1668befdaff0cc3aaafb2111847aab028a88b4c2cb017acfbaa")
    version("7.0.2-6", sha256="7d49ca8030f895c683cae69c52d8edfc4876de651f5b8bfdbea907e222480bd3")

    variant("ghostscript", default=False, description="Compile with Ghostscript support")

    depends_on("jpeg")
    depends_on("pango")
    depends_on("libtool", type="build")
    depends_on("libtool", when="@7.0.8:", type=("build", "link"))
    depends_on("libpng")
    depends_on("freetype")
    depends_on("fontconfig")
    depends_on("libtiff")
    depends_on("ghostscript", when="+ghostscript")
    depends_on("ghostscript-fonts", when="+ghostscript")
    depends_on("libsm")
    depends_on("pkgconfig", type="build")

    def configure_args(self):
        args = []
        spec = self.spec
        if spec.satisfies("+ghostscript"):
            args.append("--with-gslib")
            gs_font_dir = spec["ghostscript-fonts"].prefix.share.font
            args.append("--with-gs-font-dir={0}".format(gs_font_dir))
        else:
            args.append("--without-gslib")
        return args

    @property
    def libs(self):
        return find_libraries("libMagick*", root=self.prefix, recursive=True)
