# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Lerc(CMakePackage):
    """Limited Error Raster Compression.

    LERC is an open-source image or raster format which supports rapid encoding
    and decoding for any pixel type (not just RGB or Byte). Users set the maximum
    compression error per pixel while encoding, so the precision of the original
    input image is preserved (within user defined error bounds)."""

    homepage = "https://github.com/Esri/lerc"
    url      = "https://github.com/Esri/lerc/archive/refs/tags/v3.0.tar.gz"

    version('3.0', sha256='8c0148f5c22d823eff7b2c999b0781f8095e49a7d3195f13c68c5541dd5740a1')

    depends_on('cmake@3.11:', type='build')
