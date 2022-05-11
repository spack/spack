# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil

from spack.package import *


class Sigcpp(CMakePackage):
    """libsigc++ : The Typesafe Callback Framework for C++"""

    homepage = "https://libsigcplusplus.github.io/libsigcplusplus/"
    url      = "https://github.com/libsigcplusplus/libsigcplusplus/archive/refs/tags/3.0.7.tar.gz"

    version('3.2.0', sha256='f9c36331b5d5ac7a1651477288f47eec51394c03ade8bb1a05d1c46eac5f77e7')
    version('3.0.7', sha256='063b6ab86e4d8703ea65d894d78e8482b1fc34b92be8849f82ce1c5b05cf2b8d')

    variant('doc', default=True, description='Keep man files')

    @run_after('install')
    def drop_doc(self):
        if self.spec.satisfies('~doc'):
            shutil.rmtree(prefix.share)

    @run_after('install')
    def fix_include(self):
        source = join_path(self.spec.prefix, 'lib', 'sigc++-3.0',
                           'include', 'sigc++config.h')
        target = join_path(self.spec.prefix, 'include',
                           'sigc++-3.0', 'sigc++config.h')
        shutil.copy(source, target)
