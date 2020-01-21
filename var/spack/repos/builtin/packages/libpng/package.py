# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libpng(AutotoolsPackage):
    """libpng is the official PNG reference library."""

    homepage = "http://www.libpng.org/pub/png/libpng.html"
    url      = "http://download.sourceforge.net/libpng/libpng-1.6.37.tar.gz"
    list_url = "https://sourceforge.net/projects/libpng/files/"
    list_depth = 2

    version('1.6.37', sha256='daeb2620d829575513e35fecc83f0d3791a620b9b93d800b763542ece9390fb4')
    # From http://www.libpng.org/pub/png/libpng.html (2019-04-15)
    #     libpng versions 1.6.36 and earlier have a use-after-free bug in the
    #     simplified libpng API png_image_free(). It has been assigned ID
    #     CVE-2019-7317. The vulnerability is fixed in version 1.6.37,
    #     released on 15 April 2019.

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
