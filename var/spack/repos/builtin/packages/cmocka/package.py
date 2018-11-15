# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cmocka(CMakePackage):
    """Unit-testing framework in pure C"""
    homepage = "https://cmocka.org/"
    url      = "https://cmocka.org/files/1.1/cmocka-1.1.1.tar.xz"

    version('1.1.1', '6fbff4e42589566eda558db98b97623e')
    version('1.1.0', '59c9aa5735d9387fb591925ec53523ec')
    version('1.0.1', 'ed861e501a21a92b2af63e466df2015e')

    depends_on('cmake@2.6.0:', type='build')

    parallel = False
