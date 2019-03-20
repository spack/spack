# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Mysql(CMakePackage):
    """MySQL is an open source relational database management system."""

    homepage = "https://www.mysql.com/"
    url      = "https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.15.tar.gz"

    version('8.0.15', sha256='bb1bca2dc2f23ee9dd395cc4db93b64561d4ac20b53be5d1dae563f7be64825e')
    version('8.0.11', '38d5a5c1a1eeed1129fec3a999aa5efd')
    version('5.7.22', '269935a8b72dcba2c774d8d63a8bd1dd')

    # https://dev.mysql.com/doc/refman/8.0/en/source-installation.html

    # See CMAKE_MINIMUM_REQUIRED in CMakeLists.txt
    depends_on('cmake@3.8.0:', type='build', when='platform=win32')
    depends_on('cmake@3.9.2:', type='build', when='platform=darwin')
    depends_on('cmake@3.4.0:', type='build', when='platform=solaris')
    depends_on('cmake@2.8.12:', type='build')

    depends_on('gmake@3.75:', type='build')

    # Each version of MySQL requires a specific version of boost
    # See BOOST_PACKAGE_NAME in cmake/boost.cmake
    depends_on('boost@1.68.0', type='build', when='@8.0.15')
    depends_on('boost@1.66.0', type='build', when='@8.0.11')
    depends_on('boost@1.59.0', type='build', when='@5.7.22')

    depends_on('ncurses')
    depends_on('openssl')
    depends_on('perl', type='test')
    depends_on('bison@2.1:', type='build', when='@develop')
    depends_on('m4', type='build', when='@develop platform=solaris')
