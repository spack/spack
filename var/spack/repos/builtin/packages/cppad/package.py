# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cppad(CMakePackage):
    """A Package for Differentiation of C++ Algorithms."""

    homepage = "https://www.coin-or.org/CppAD/"
    url      = "http://www.coin-or.org/download/source/CppAD/cppad-20170114.gpl.tgz"
    git      = "https://github.com/coin-or/CppAD.git"

    version('develop', branch='master')
    version('20170114', '565a534dc813fa1289764222cd8c11ea')

    def cmake_args(self):
        # This package does not obey CMAKE_INSTALL_PREFIX
        args = [
            "-Dcppad_prefix=%s" % (self.prefix),
            "-Dcmake_install_docdir=share/cppad/doc"
        ]
        return args
