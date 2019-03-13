# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Mysql(CMakePackage):
    homepage = "http://dev.mysql.com"
    url      = "https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.11.tar.gz"

    version('8.0.11', '38d5a5c1a1eeed1129fec3a999aa5efd')
    version('5.7.22', '269935a8b72dcba2c774d8d63a8bd1dd')

    depends_on('boost@1.66.0', when='@8.0.11')
    depends_on('boost@1.59.0', when='@5.7.22')
