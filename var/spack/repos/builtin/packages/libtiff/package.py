# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libtiff(AutotoolsPackage):
    """LibTIFF - Tag Image File Format (TIFF) Library and Utilities."""

    homepage = "http://www.simplesystems.org/libtiff/"
    url      = "http://download.osgeo.org/libtiff/tiff-4.0.10.tar.gz"

    version('4.0.10', sha256='2c52d11ccaf767457db0c46795d9c7d1a8d8f76f68b0b800a3dfe45786b996e4')
    version('4.0.9', '54bad211279cc93eb4fca31ba9bfdc79')
    version('4.0.8', '2a7d1c1318416ddf36d5f6fa4600069b')
    version('4.0.7', '77ae928d2c6b7fb46a21c3a29325157b')
    version('4.0.6', 'd1d2e940dea0b5ad435f21f03d96dd72')
    version('4.0.3', '051c1068e6a0627f461948c365290410')
    version('3.9.7', '626102f448ba441d42e3212538ad67d2')

    depends_on('jpeg')
    depends_on('zlib')
    depends_on('xz')
