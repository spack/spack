# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sjpeg(CMakePackage):
    """SimpleJPEG: simple jpeg encoder."""

    homepage = "https://github.com/webmproject/sjpeg"
    git = "https://github.com/webmproject/sjpeg.git"

    version("master", branch="master")

    depends_on("cmake@2.8.7:", type="build")
    # TODO: these dependencies seem to be optional?
    # depends_on("zlib")
    # depends_on("libpng")
    # depends_on("jpeg")
    # depends_on("gl")
    # depends_on("freeglut")
