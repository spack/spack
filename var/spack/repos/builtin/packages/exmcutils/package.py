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

    version('develop', branch='master')
    version('0.5.7', '69bb32f364e93e8a60865c05efbf4f52')
    version('0.5.6', 'b12a8dc163e3369492ec7c1403fe86e4')

    @when('@develop')
    def configure_directory_helper(self):
        return "c-utils/code"

    @when('@0')
    def configure_directory_helper(self):
        return "."

    @property
    def configure_directory(self):
        return self.configure_directory_helper()

    depends_on('m4', when='@develop')
    depends_on('autoconf', when='@develop')
    depends_on('automake', when='@develop')
    depends_on('libtool', when='@develop')
