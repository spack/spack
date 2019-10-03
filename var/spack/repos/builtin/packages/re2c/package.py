# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Re2c(AutotoolsPackage):
    """re2c: a free and open-source lexer generator for C and C++"""

    homepage = "http://re2c.org/index.html"
    url      = "https://github.com/skvadrik/re2c/releases/download/1.2.1/re2c-1.2.1.tar.xz"

    version('1.2.1', '8b5d7dfc5a709c7220714889fa24ed32')
    version('1.0.3', '8f575e2bf2efd3c685c87042f279ae4f')

    def configure_args(self):
        args = ['--disable-dependency-tracking']
        return args
