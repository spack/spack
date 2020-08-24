# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sqoop(Package):
    """Apache Sqoop is a tool designed for efficiently transferring bulk
    data between Apache Hadoop and structured datastores such as relational
    databases."""

    homepage = "http://sqoop.apache.org/"
    url      = "https://downloads.apache.org/sqoop/1.99.7/sqoop-1.99.7.tar.gz"
    list_url = "https://downloads.apache.org/sqoop/"
    list_depth = 1

    version('1.99.7', sha256='caca533554235d9e999435be59a13b5ecae514b3c914ca3b54868fca43a3b74a')

    depends_on('maven', type='build')
    depends_on('java@8', type=('build', 'run'))

    def install(self, spec, prefix):
        mvn = which('mvn')
        mvn('clean', 'install', '-DskipTests')
        install_tree('.', prefix)
