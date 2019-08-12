# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Exmcutils(AutotoolsPackage):
    """ExM C-Utils: Generic C utility library for ADLB/X and Swift/T"""

    homepage = 'http://swift-lang.org/Swift-T'
    url      = 'http://swift-lang.github.io/swift-t-downloads/spack/exmcutils-0.0.0.tar.gz'
    git      = "https://github.com/swift-lang/swift-t.git"

    version('master', branch='master')
    version('0.5.7', '69bb32f364e93e8a60865c05efbf4f52')
    version('0.5.6', 'b12a8dc163e3369492ec7c1403fe86e4')

    @property
    def configure_directory(self):
        if self.version == Version('master'):
            return 'c-utils/code'
        else:
            return '.'

    depends_on('m4', when='@master')
    depends_on('autoconf', when='@master')
    depends_on('automake', when='@master')
    depends_on('libtool', when='@master')
