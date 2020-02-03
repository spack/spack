# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libmng(CMakePackage):
    """THE reference library for reading, displaying, writing
       and examining Multiple-Image Network Graphics.  MNG is the animation
       extension to the popular PNG image format."""
    homepage = "http://sourceforge.net/projects/libmng/"
    url      = "http://downloads.sourceforge.net/project/libmng/libmng-devel/2.0.3/libmng-2.0.3.tar.gz"

    version('2.0.3', sha256='cf112a1fb02f5b1c0fce5cab11ea8243852c139e669c44014125874b14b7dfaa')
    version('2.0.2', sha256='4908797bb3541fb5cd8fffbe0b1513ed163509f2a4d57a78b26a96f8d1dd05a2')

    variant('shared', default=True, description="Build shared library version")

    depends_on("gzip")
    depends_on("jpeg")
    depends_on("zlib")
    depends_on("lcms")

    def patch(self):
        # jpeg requires stdio to be included before its headers.
        filter_file(r'^(\#include \<jpeglib\.h\>)',
                    '#include<stdio.h>\n\\1', 'libmng_types.h')

    def cmake_args(self):
        args = [('WITH_LCMS2', True),
                ('WITH_LCMS1', False)]

        return ['-D{0}:BOOL={1}'.format(key, 'ON' if val else 'OFF')
                for (key, val) in args]
