# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsixel(AutotoolsPackage):
    """
    This package provides encoder/decoder implementation for DEC SIXEL graphics, and some converter programs.
    """

    homepage = "https://github.com/saitoha/libsixel"
    url = "https://github.com/saitoha/libsixel/archive/refs/tags/v1.8.6.tar.gz"

    maintainers("taliaferro")

    version("1.8.6", sha256="37611d60c7dbcee701346967336dbf135fdd5041024d5f650d52fae14c731ab9")

    variant("curl", default=False, description="build with libcurl")
    variant("gd", default=False, description="build with libgd")
    variant("gdk-pixbuf2", default=False, description="build with gdk-pixbuf2")
    variant("jpeg", default=True, description="build with libjpeg")
    variant("png", default=True, description="build with libpng")

    depends_on("curl", when="+curl")
    depends_on("libgd", when="+gd")
    depends_on("gdk-pixbuf", when="+gdk-pixbuf2")
    depends_on("libjpeg", when="+jpeg")
    depends_on("libpng", when="+png")

    # there's one more flag for adding the Python interface to libsixel
    # must run configure with --with-python
    # but arguably should that be a separate py-libsixel?

    def configure_args(self):
        args_map = {
            "--with-libcurl": "+curl",
            "--with-gd": "+gd",
            "--with-gdk-pixbuf2": "+gdk-pixbuf2",
            "--with-png": "+png",
            "--with-jpeg": "+jpeg",
        }
        args = []
        for flag, variant in args_map.items():
            flag_value = "yes" if variant in self.spec else "no"
            args.append("{}={}".format(flag, flag_value))
        return args
