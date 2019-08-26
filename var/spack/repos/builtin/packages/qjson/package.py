# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qjson(CMakePackage):
    """QJson is a Qt-based library that maps JSON data to QVariant
       objects and vice versa."""

    homepage = "http://qjson.sourceforge.net/"
    url      = "https://github.com/flavio/qjson/archive/0.9.0.tar.gz"

    version('0.9.0', '2846278bb5fc9aeacab80ac14b8ed48d')

    depends_on('qt')

    def cmake_args(self):
        args = []
        if self.spec['qt'].version.up_to(1) == Version(4):
            args.append('-DQT4_BUILD=ON')
        return args
