# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Exempi(AutotoolsPackage):
    """exempi is a port of Adobe XMP SDK to work on UNIX and to be build with
    GNU automake.

    It includes XMPCore and XMPFiles, libexempi, a C-based API and exempi
    a command line tool.
    """

    homepage = "https://libopenraw.freedesktop.org/wiki/Exempi"
    url      = "https://libopenraw.freedesktop.org/download/exempi-2.5.2.tar.bz2"

    version('2.5.2', sha256='52f54314aefd45945d47a6ecf4bd21f362e6467fa5d0538b0d45a06bc6eaaed5')

    depends_on('zlib')
    depends_on('iconv')
    depends_on('boost@1.48.0:')
    depends_on('pkgconfig')
    depends_on('expat')

    conflicts('%gcc@:4.5')

    def patch(self):
        # fix make check: Fix undefined reference to `boost::unit_test::unit_test_main`:
        # BOOST_TEST_DYN_LINK only works with shlib and when boost is linked after src:
        # https://bugs.launchpad.net/widelands/+bug/662908
        # https://github.com/bincrafters/community/issues/127
        filter_file('#define BOOST_TEST_DYN_LINK', '', 'exempi/tests/test-adobesdk.cpp')

    def configure_args(self):
        args = ['--with-boost={0}'.format(self.spec['boost'].prefix)]

        if self.spec.satisfies('polatform=darwin'):
            args += ['--with-darwinports', '--with-fink']

        return args
