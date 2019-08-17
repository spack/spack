# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libtermkey(Package):
    """Easy keyboard entry processing for terminal programs"""
    homepage = "http://www.leonerd.org.uk/code/libtermkey/"
    url      = "http://www.leonerd.org.uk/code/libtermkey/libtermkey-0.18.tar.gz"

    version('0.18', '3be2e3e5a851a49cc5e8567ac108b520')
    version('0.17', '20edb99e0d95ec1690fe90e6a555ae6d')
    version('0.16', '7a24b675aaeb142d30db28e7554987d4')
    version('0.15b', '27689756e6c86c56ae454f2ac259bc3d')
    version('0.14', 'e08ce30f440f9715c459060e0e048978')

    depends_on('libtool', type='build')
    depends_on('ncurses')

    def install(self, spec, prefix):
        make()
        make("install", "PREFIX=" + prefix)
