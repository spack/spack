# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libpng(AutotoolsPackage):
    """libpng is the official PNG reference library."""

    homepage = "http://www.libpng.org/pub/png/libpng.html"
    url      = "http://download.sourceforge.net/libpng/libpng-1.6.34.tar.gz"
    list_url = "https://sourceforge.net/projects/libpng/files/"
    list_depth = 2

    version('1.6.34', sha256='574623a4901a9969080ab4a2df9437026c8a87150dfd5c235e28c94b212964a7')
    version('1.6.29', sha256='e30bf36cd5882e017c23a5c6a79a9aa1a744dd5841bb45ff7035ec6e3b3096b8')
    version('1.6.28', sha256='b6cec903e74e9fdd7b5bbcde0ab2415dd12f2f9e84d9e4d9ddd2ba26a41623b2')
    version('1.6.27', sha256='c9d164ec247f426a525a7b89936694aefbc91fb7a50182b198898b8fc91174b4')
    # From http://www.libpng.org/pub/png/libpng.html (2017-01-04)
    #     Virtually all libpng versions through 1.6.26, 1.5.27,
    #     1.4.19, 1.2.56, and 1.0.66, respectively, have a
    #     null-pointer-dereference bug in png_set_text_2() when an
    #     image-editing application adds, removes, and re-adds text
    #     chunks to a PNG image. (This bug does not affect pure
    #     viewers, nor are there any known editors that could trigger
    #     it without interactive user input. It has been assigned ID
    #     CVE-2016-10087.)  The vulnerability is fixed in versions
    #     1.6.27, 1.5.28, 1.4.20, 1.2.57, and 1.0.67, released on 29
    #     December 2016.

    # Required for qt@3
    version('1.2.57', sha256='09ec37869fc5b130f5eb06ffb9bf949796e8d2d78e0788f78ab1c78624c6e9da')

    depends_on('zlib@1.0.4:')  # 1.2.5 or later recommended

    def configure_args(self):
        args = [
            # not honored, see
            #   https://sourceforge.net/p/libpng/bugs/210/#33f1
            # '--with-zlib=' + self.spec['zlib'].prefix,
            'CPPFLAGS={0}'.format(self.spec['zlib'].headers.include_flags),
            'LDFLAGS={0}'.format(self.spec['zlib'].libs.search_flags)
        ]
        return args

    def check(self):
        # Libpng has both 'check' and 'test' targets that are aliases.
        # Only need to run the tests once.
        make('check')
